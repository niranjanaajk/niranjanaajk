"""Small testable contextual Q&A service core with an injectable LLM client.

No external API calls or keys are required to run the demo/tests.
"""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Answer:
    text: str
    evidence: tuple[str, ...]
    fallback: bool


def tokenize(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def retrieve(question, documents, top_k=2):
    if not question.strip():
        raise ValueError("Question is required")
    if top_k < 1:
        raise ValueError("top_k must be positive")
    words = tokenize(question)
    results = []
    for document in documents:
        score = len(words & tokenize(document))
        if score:
            results.append((score, document))
    return [d for _, d in sorted(results, key=lambda item: -item[0])[:top_k]]


def answer_question(question, documents, model=None):
    evidence = retrieve(question, documents)
    if not evidence:
        return Answer("I do not have enough information in the provided documents.",
                      (), True)
    if model is None:
        # Local deterministic answer, easy to test without API cost.
        return Answer(evidence[0], tuple(evidence), False)
    instruction = ("Answer only using the context. If evidence is insufficient, say so.\n"
                   "Question: " + question + "\nContext:\n" + "\n".join(evidence))
    output = model(instruction)
    if not isinstance(output, str) or not output.strip():
        raise ValueError("Model returned an invalid response")
    return Answer(output.strip(), tuple(evidence), False)


if __name__ == "__main__":
    kb = [
        "Our prototype tracks evaluation outcomes and interaction quality.",
        "The application presents educational resources and collects usability feedback.",
        "No automated medical recommendations are provided."
    ]
    print(answer_question("How does it collect usability feedback?", kb).text)
