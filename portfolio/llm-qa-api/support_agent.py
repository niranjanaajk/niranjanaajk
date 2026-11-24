"""Run an offline document-support agent with bounded, read-only tool calls."""
import argparse
import json

from qa import tokenize

DOCUMENTS = {
    "KB-01": "Password resets require identity verification through the account portal.",
    "KB-02": "Billing disputes should include an invoice number and disputed amount.",
    "KB-03": "Outage reports should include the service name and the time symptoms started.",
}


def search_documents(query, documents):
    terms = tokenize(query)
    ranked = sorted(
        ((len(terms & tokenize(body)), ref) for ref, body in documents.items()),
        key=lambda match: (-match[0], match[1]),
    )
    return [ref for score, ref in ranked if score > 0][:2]


def offline_planner(question, trace):
    if not trace:
        return {"tool": "search_documents", "query": question}
    if trace[-1]["tool"] == "search_documents" and trace[-1]["result"]:
        return {"tool": "read_document", "ref": trace[-1]["result"][0]}
    return {"tool": "finish"}


def run_agent(question, planner=offline_planner, documents=None):
    if not question.strip():
        raise ValueError("Question is required.")
    documents = DOCUMENTS if documents is None else documents
    trace = []
    allowed_refs = set()
    evidence = {}
    for _ in range(3):
        action = planner(question, trace)
        tool = action.get("tool")
        if tool == "finish":
            break
        if tool == "search_documents" and isinstance(action.get("query"), str):
            result = search_documents(action["query"], documents)
            allowed_refs.update(result)
        elif tool == "read_document" and isinstance(action.get("ref"), str) and action["ref"] in allowed_refs:
            ref = action["ref"]
            evidence[ref] = documents[ref]
            result = ref
        else:
            break
        trace.append({"tool": tool, "result": result})
    if not evidence:
        return {"answer": "Insufficient evidence. Send for manual review.", "citations": [],
                "manual_review": True, "trace": trace}
    return {"answer": " ".join(f"{body} [{ref}]" for ref, body in evidence.items()),
            "citations": list(evidence), "manual_review": False, "trace": trace}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question")
    args = parser.parse_args()
    print(json.dumps(run_agent(args.question), indent=2))
