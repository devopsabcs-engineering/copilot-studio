"""Verify actual retrieval membership and render source text without generation."""

import ast
import hashlib
import json
import re
from dataclasses import dataclass
from urllib.parse import parse_qs, unquote, urlsplit


class EvidenceError(ValueError):
    """Evidence cannot be delivered safely."""


SOURCES = {
    "fraud_patterns_data": ("fraud-patterns", "fraud-patterns-ks", "Fraud indicators"),
    "regulatory_compliance_data": (
        "regulatory-compliance", "regulatory-compliance-ks", "Conditional compliance evidence"
    ),
    "investigation_procedures_data": (
        "investigation-procedures", "investigation-procedures-ks",
        "Evidence-preserving investigation steps",
    ),
}
PUBLISHER_REVISION = "e9ecd00dba2c25dbc8306b5be6818d22645607a3"
NOTEBOOK_URL = (
    "https://raw.githubusercontent.com/Azure/Copilot-Studio-and-Azure/"
    + PUBLISHER_REVISION
    + "/labs/2.4-microsoft-foundry-agentic-retrieval/notebooks/foundry-IQ-agents.ipynb"
)
NOTEBOOK_SHA256 = "45664948b2e915eebe667816cbc957c89e6b7c34fa61f6b1365d0267ad8e69f2"


@dataclass(frozen=True)
class Record:
    record_id: str
    source: str
    index: str
    title: str
    content: str


def load_corpus(raw: bytes) -> dict[str, Record]:
    if hashlib.sha256(raw).hexdigest() != NOTEBOOK_SHA256:
        raise EvidenceError("Publisher notebook digest does not match the approved pin")
    notebook = json.loads(raw)
    records: dict[str, Record] = {}
    found_groups: set[str] = set()
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        text = "".join(cell["source"])
        if not any(re.search(rf"(?m)^\s*{name}\s*=", text) for name in SOURCES):
            continue
        for node in ast.parse(text).body:
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if not isinstance(target, ast.Name) or target.id not in SOURCES:
                    continue
                if target.id in found_groups:
                    raise EvidenceError("Duplicate publisher data assignment")
                found_groups.add(target.id)
                index, source, _ = SOURCES[target.id]
                documents = ast.literal_eval(node.value)
                if not isinstance(documents, list) or len(documents) != 8:
                    raise EvidenceError("Expected eight records per publisher source")
                for document in documents:
                    if (not isinstance(document, dict)
                            or set(document) != {"id", "title", "content"}
                            or not all(isinstance(value, str) and value.strip()
                                       for value in document.values())
                            or document["id"] in records):
                        raise EvidenceError("Invalid or duplicate publisher record")
                    records[document["id"]] = Record(
                        document["id"], source, index, document["title"], document["content"]
                    )
    if found_groups != set(SOURCES) or len(records) != 24:
        raise EvidenceError("Expected all three publisher sources and 24 records")
    return records


def retrieved_records(
    response: dict, corpus: dict[str, Record], search_endpoint: str
) -> dict[str, Record]:
    if response.get("status") != "completed" or response.get("error"):
        raise EvidenceError("Retrieval response did not complete successfully")
    expected_url = urlsplit(search_endpoint)
    if (expected_url.scheme != "https" or not expected_url.hostname
            or expected_url.username or expected_url.password
            or expected_url.port not in (None, 443)):
        raise EvidenceError("Expected an HTTPS Search endpoint")
    verified: dict[str, Record] = {}
    calls = 0
    for item in response.get("output", []):
        if item.get("type") != "mcp_call":
            continue
        if (item.get("name") != "knowledge_base_retrieve"
                or item.get("server_label") != "fraud-kb"
                or item.get("status") != "completed" or item.get("error")):
            raise EvidenceError("Unexpected or unsuccessful retrieval tool call")
        calls += 1
        output = item.get("output")
        if not isinstance(output, str):
            raise EvidenceError("Retrieval tool output must be text")
        if not output.strip():
            continue
        try:
            payload = json.loads(output)
        except json.JSONDecodeError as error:
            raise EvidenceError("Retrieval tool output is not valid JSON") from error
        if not isinstance(payload, dict) or not isinstance(payload.get("documents"), list):
            raise EvidenceError("Retrieval documents are missing")
        for document in payload["documents"]:
            if not isinstance(document, dict):
                raise EvidenceError("Invalid retrieved document")
            record = json.loads(document["content"])
            if not isinstance(record, dict) or not isinstance(record.get("id"), str):
                raise EvidenceError("Retrieved record ID is missing")
            original = corpus.get(record["id"])
            if original is None:
                raise EvidenceError("Retrieved record is outside the approved corpus")
            reference = urlsplit(document["url"])
            query = parse_qs(reference.query, keep_blank_values=True)
            path = [unquote(part) for part in reference.path.split("/") if part]
            if (reference.scheme != "https"
                    or reference.hostname != expected_url.hostname
                    or reference.port not in (None, 443)
                    or reference.username or reference.password
                    or set(query) - {"$select", "api-version", "allowUnsafeKeys"}
                    or reference.fragment
                    or path != ["indexes", original.index, "docs", original.record_id]):
                raise EvidenceError("Retrieved reference does not identify its actual source")
            expected = {"id": original.record_id, "content": original.content}
            if "title" in record:
                expected["title"] = original.title
            if "source_name" in record:
                expected["source_name"] = original.source
            if record != expected:
                raise EvidenceError("Retrieved record differs from the pinned publisher record")
            verified[original.record_id] = original
    if not calls:
        raise EvidenceError("No completed knowledge-base retrieval call was observed")
    return verified


def selection_schema(records: dict[str, Record]) -> dict:
    if not records:
        raise EvidenceError("Cannot select from an empty retrieval")
    return {
        "type": "json_schema",
        "name": "retrieved_record_selection",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "record_ids": {
                    "type": "array", "maxItems": 9,
                    "items": {"type": "string", "enum": sorted(records)},
                }
            },
            "required": ["record_ids"],
            "additionalProperties": False,
        },
    }


def render_evidence(selection: dict, records: dict[str, Record]) -> str:
    if not isinstance(selection, dict) or set(selection) != {"record_ids"}:
        raise EvidenceError("Selection must contain only record_ids")
    ids = selection["record_ids"]
    if (not isinstance(ids, list) or len(ids) > 9
            or any(not isinstance(value, str) or value not in records for value in ids)
            or len(set(ids)) != len(ids)):
        raise EvidenceError("Selection contains duplicate, unknown or invalid record IDs")
    if not ids:
        return "Cannot determine from configured sources."
    lines = ["Workshop source evidence - not legal advice."]
    for _, source, heading in SOURCES.values():
        selected = [records[value] for value in ids if records[value].source == source]
        if selected:
            lines.extend(("", f"## {heading}", ""))
            lines.extend(f'- "{record.content}" \u3010{source}\u3011' for record in selected)
            if source == "regulatory-compliance-ks":
                lines.extend(("", "Cannot determine applicability from configured sources."))
    return "\n".join(lines)
