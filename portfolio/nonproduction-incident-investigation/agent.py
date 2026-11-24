"""Optional LLM orchestration over a fixed set of read-only investigation tools."""
import argparse
import json
import os
import re
import sqlite3
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from runbook_assistant import recommend

TOOLS = [
    {"type": "function", "function": {
        "name": "investigate_service",
        "description": "Retrieve recurring signatures, counts and cited SQLite runbook guidance.",
        "parameters": {"type": "object", "properties": {"service": {"type": "string"}},
                       "required": ["service"], "additionalProperties": False},
    }}
]


def investigate(service, port=8080):
    query = urlencode({"service": service})
    with urlopen(f"http://127.0.0.1:{port}/incidents?" + query, timeout=5) as response:
        evidence = json.load(response)
    with sqlite3.connect(":memory:") as database:
        return recommend(evidence["failures"], database)


def grounded_summary(evidence):
    lines = []
    for row in evidence:
        source = f" [{row['citation']}]" if row["citation"] else ""
        lines.append(f"{row['signature']}: {row['count']} events. {row['next_check']}{source}")
    return "\n".join(lines)


def completion(messages, tools, key, model):
    payload = {"model": model, "messages": messages}
    if tools:
        payload.update(tools=tools, tool_choice="required", parallel_tool_calls=False)
    request = Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)["choices"][0]["message"]


def run_agent(question, complete, investigate_service=investigate):
    messages = [
        {"role": "system", "content": (
            "Investigate synthetic nonproduction incidents. Use the tool for a service named by "
            "the user. Ground claims in tool evidence, cite runbook IDs, distinguish suggested "
            "checks from causes, and report missing evidence. Never propose running commands."
        )},
        {"role": "user", "content": question},
    ]
    plan = complete(messages, TOOLS)
    calls = plan.get("tool_calls", [])
    if len(calls) != 1 or calls[0]["function"]["name"] != "investigate_service":
        raise ValueError("Expected one supported investigation tool call")
    call = calls[0]
    args = json.loads(call["function"]["arguments"])
    service = args.get("service")
    if not isinstance(service, str) or not service.strip() or len(service) > 80:
        raise ValueError("Expected a service name of 1 to 80 characters")
    evidence = investigate_service(service.strip())
    if not evidence:
        return {"answer": "No incident evidence found for the selected service.", "evidence": []}
    messages.extend([
        {"role": "assistant", "content": plan.get("content"), "tool_calls": calls},
        {"role": "tool", "tool_call_id": call["id"], "content": json.dumps(evidence)},
    ])
    try:
        answer = complete(messages, None).get("content")
    except (OSError, ValueError, KeyError, IndexError):
        answer = None
    expected = {row["citation"] for row in evidence if row["citation"]}
    cited = set(re.findall(r"\bRB-\d+\b", answer)) if isinstance(answer, str) else set()
    use_model = bool(isinstance(answer, str) and answer.strip() and expected and cited == expected)
    return {"answer": answer if use_model else grounded_summary(evidence),
            "summary_source": "model" if use_model else "evidence",
            "evidence": evidence}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question")
    parser.add_argument("--model", default="gpt-4.1-mini")
    args = parser.parse_args()
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        parser.error("Set OPENAI_API_KEY or use runbook_assistant.py for offline retrieval.")
    print(json.dumps(run_agent(
        args.question, lambda messages, tools: completion(messages, tools, key, args.model)
    ), indent=2))
