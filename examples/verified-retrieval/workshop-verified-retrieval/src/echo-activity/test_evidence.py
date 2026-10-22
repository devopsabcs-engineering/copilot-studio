import json
import hashlib
import unittest
from unittest.mock import patch

from evidence import (
    EvidenceError, Record, load_corpus, render_evidence, retrieved_records, selection_schema,
)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.record = Record(
            "fp-test", "fraud-patterns-ks", "fraud-patterns", "Synthetic fixture",
            'Use the full sentence - including "conditions", $12,345 and exceptions.',
        )
        self.corpus = {self.record.record_id: self.record}
        self.projection = {
            "id": self.record.record_id, "title": self.record.title,
            "content": self.record.content, "source_name": self.record.source,
        }
        self.document = {
            "id": "retrieval-document",
            "url": "https://owned.search.windows.net/indexes/fraud-patterns/docs/fp-test",
            "content": json.dumps(self.projection),
        }

    def response(self, **changes):
        call = {
            "type": "mcp_call", "name": "knowledge_base_retrieve", "server_label": "fraud-kb",
            "status": "completed", "error": None,
            "output": json.dumps({"documents": [self.document]}),
        }
        call.update(changes)
        return {"status": "completed", "error": None, "output": [call]}

    def verified(self, response=None):
        return retrieved_records(
            response or self.response(), self.corpus, "https://owned.search.windows.net"
        )

    def test_exact_record_and_actual_retrieval_are_required(self):
        self.assertEqual(self.verified(), self.corpus)

    def test_actual_search_reference_projection_parameters_are_accepted(self):
        self.document["url"] += (
            "?$select=title%2Ccontent%2Cid&api-version=2026-08-01-preview&allowUnsafeKeys=true"
        )
        self.assertEqual(self.verified(), self.corpus)

    def test_nonliteral_quote_cannot_reach_renderer(self):
        self.projection["content"] = "Shortened paraphrase."
        self.document["content"] = json.dumps(self.projection)
        with self.assertRaises(EvidenceError):
            self.verified()

    def test_wrong_source_field_is_rejected(self):
        self.projection["source_name"] = "regulatory-compliance-ks"
        self.document["content"] = json.dumps(self.projection)
        with self.assertRaises(EvidenceError):
            self.verified()

    def test_wrong_reference_host_path_scheme_or_credentials_is_rejected(self):
        for url in (
            "https://other.search.windows.net/indexes/fraud-patterns/docs/fp-test",
            "https://owned.search.windows.net/indexes/regulatory-compliance/docs/fp-test",
            "http://owned.search.windows.net/indexes/fraud-patterns/docs/fp-test",
            "https://user@owned.search.windows.net/indexes/fraud-patterns/docs/fp-test",
            "https://owned.search.windows.net:444/indexes/fraud-patterns/docs/fp-test",
            "https://owned.search.windows.net/indexes/fraud-patterns/docs/fp-test?other=1",
        ):
            with self.subTest(url=url):
                self.document["url"] = url
                with self.assertRaises(EvidenceError):
                    self.verified()

    def test_unknown_record_is_rejected(self):
        self.projection["id"] = "invented"
        self.document["content"] = json.dumps(self.projection)
        with self.assertRaises(EvidenceError):
            self.verified()

    def test_malformed_or_unfinished_retrieval_is_rejected(self):
        for changes in (
            {"status": "failed"}, {"error": {"code": "denied"}},
            {"name": "different_tool"}, {"server_label": "untrusted"},
            {"output": '{"documents":null}'},
        ):
            with self.subTest(changes=changes), self.assertRaises(EvidenceError):
                self.verified(self.response(**changes))
        with self.assertRaises(EvidenceError):
            self.verified({"status": "incomplete", "output": []})
        with self.assertRaises(EvidenceError):
            self.verified({"status": "completed", "output": []})

    def test_no_partial_delivery_when_a_later_document_is_invalid(self):
        bad = dict(self.document, url="https://other.example/record")
        response = self.response(output=json.dumps({"documents": [self.document, bad]}))
        with self.assertRaises(EvidenceError):
            self.verified(response)

    def test_source_metadata_may_be_absent_but_not_wrong(self):
        del self.projection["source_name"]
        del self.projection["title"]
        self.document["content"] = json.dumps(self.projection)
        self.assertEqual(self.verified(), self.corpus)

    def test_renderer_copies_whole_text_and_adds_individual_marker(self):
        rendered = render_evidence({"record_ids": ["fp-test"]}, self.verified())
        self.assertIn(f'- "{self.record.content}" \u3010fraud-patterns-ks\u3011', rendered)
        self.assertNotIn("fp-test", rendered)
        self.assertNotIn("https://", rendered)

    def test_every_bullet_has_its_own_marker(self):
        second = Record("second", self.record.source, self.record.index, "Second", "Second passage.")
        records = {**self.corpus, second.record_id: second}
        rendered = render_evidence({"record_ids": list(records)}, records)
        self.assertEqual(rendered.count("\u3010fraud-patterns-ks\u3011"), 2)

    def test_selection_cannot_supply_quotes_or_unknown_duplicate_or_invalid_ids(self):
        for selection in (
            {"record_ids": ["invented"]}, {"record_ids": ["fp-test", "fp-test"]},
            {"record_ids": "fp-test"}, {"record_ids": [None]},
            {"record_ids": ["fp-test"], "answer": "Invented quotation"},
            {"record_ids": ["fp-test"] * 10}, [],
        ):
            with self.subTest(selection=selection), self.assertRaises(EvidenceError):
                render_evidence(selection, self.corpus)

    def test_regulation_retains_whole_context_and_applicability_boundary(self):
        regulation = Record(
            "rc-test", "regulatory-compliance-ks", "regulatory-compliance", "Scope",
            "If the condition applies, use this deadline. Otherwise use the exception.",
        )
        rendered = render_evidence({"record_ids": ["rc-test"]}, {"rc-test": regulation})
        self.assertIn(regulation.content, rendered)
        self.assertIn("Cannot determine applicability from configured sources.", rendered)

    def test_valid_empty_selection_is_explicit_abstention(self):
        self.assertEqual(
            render_evidence({"record_ids": []}, self.corpus),
            "Cannot determine from configured sources.",
        )

    def test_schema_only_allows_actual_retrieval_ids(self):
        schema = selection_schema(self.corpus)["schema"]
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["record_ids"]["items"]["enum"], ["fp-test"])
        with self.assertRaises(EvidenceError):
            selection_schema({})

    def test_publisher_pin_rejects_changed_bytes_without_executing_code(self):
        with self.assertRaises(EvidenceError):
            load_corpus(b'{"cells":[]}')

    def test_load_only_literal_data_assignments_not_unrelated_notebook_fragments(self):
        from evidence import SOURCES
        cells = [{"cell_type": "code", "source": ["invalid keyword=fragment, input=test"]}]
        for name in SOURCES:
            documents = [
                {"id": f"{name}-{number}", "title": "Fixture", "content": "Source."}
                for number in range(8)
            ]
            cells.append({"cell_type": "code", "source": [f"{name} = {documents!r}"]})
        raw = json.dumps({"cells": cells}).encode()
        with patch("evidence.NOTEBOOK_SHA256", hashlib.sha256(raw).hexdigest()):
            self.assertEqual(len(load_corpus(raw)), 24)

    def test_data_assignment_cannot_execute_code(self):
        raw = json.dumps({"cells": [{
            "cell_type": "code", "source": ["fraud_patterns_data = list(range(8))"]
        }]}).encode()
        with patch("evidence.NOTEBOOK_SHA256", hashlib.sha256(raw).hexdigest()):
            with self.assertRaises(ValueError):
                load_corpus(raw)


if __name__ == "__main__":
    unittest.main()
