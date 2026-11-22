from app.modules.m2_schema.rules import evaluate
from app.values import number
from decimal import Decimal
def test_real_versions_preserved(result): assert result["stages"][1]["rows"][0]["version"]=="4"
def test_real_delete_document_empty(result): assert result["stages"][1]["rows"][1]["document"] is None
def test_real_sentinel_isolated(result):
    "TRAP-07"
    assert any(r["reason"]=="EMPTY_VALUE" for r in result["stages"][1]["quarantine"])
def test_real_bad_json_isolated(result): assert any(r["reason"]=="BAD_PAYLOAD" for r in result["stages"][1]["quarantine"])
def test_large_version_precise():
    "TRAP-09"
    assert str(number("9007199254740993"))=="9007199254740993"
def test_fullwidth_version():
    "TRAP-06"
    assert number("１２")==Decimal(12)
def test_negative_latency_rejected():
    row={"version":"1","op":"delete","side":"index","source_time":"2026-11-16T10:00:00Z","visible_time":"2026-11-16T09:59:00Z","reported":"1"}
    assert evaluate([row],{})["quarantine"][0]["reason"]=="NEGATIVE_LATENCY"

def test_integral_version_spelling_canonicalized():
    row={"event_id":"a","doc_id":"1","version":"1.0","op":"delete","side":"source","source_time":"2026-11-16T10:00:00Z","visible_time":"-","reported":"1"}
    assert evaluate([row],{})["rows"][0]["version"]=="1"
