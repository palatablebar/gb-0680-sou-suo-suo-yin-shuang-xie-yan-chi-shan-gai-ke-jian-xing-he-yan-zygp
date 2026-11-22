from app.modules.m4_visibility.rules import evaluate
def state(side,version="5",op="delete",doc="01",document=None):return {"doc_id":doc,"side":side,"version":version,"op":op,"document":document,"source_at":"2026-11-16T10:00:00Z","visible_at":"2026-11-16T10:00:30Z","_sources":[1 if side=="source" else 2]}
def test_real_consistent_deleted_docs(result): assert result["stages"][3]["metrics"]["consistent"]==9
def test_missing_separate(): assert evaluate([state("source",op="upsert")],{})["rows"][0]["visibility_state"]=="MISSING_INDEX"
def test_delete_without_tombstone_confirmation(): assert evaluate([state("source")],{})["rows"][0]["visibility_state"]=="DELETE_NOT_CONFIRMED"
def test_stale_target(): assert evaluate([state("source"),state("index","4","upsert")],{})["rows"][0]["visibility_state"]=="STALE_INDEX"
def test_same_version_content_mismatch(): assert evaluate([state("source",op="upsert",document={"a":1}),state("index",op="upsert",document={"a":2})],{})["rows"][0]["visibility_state"]=="CONTENT_MISMATCH"
def test_orphan_target(): assert evaluate([state("index")],{})["rows"][0]["visibility_state"]=="ORPHAN_INDEX"
def test_real_deleted_op_not_resurrected(result): assert result["stages"][3]["rows"][0]["index_op"]=="delete"
