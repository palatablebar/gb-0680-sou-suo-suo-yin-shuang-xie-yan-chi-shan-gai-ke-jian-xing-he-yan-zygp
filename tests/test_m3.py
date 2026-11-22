from app.modules.m3_versions.rules import evaluate
def event(id,ver,op="upsert",document=None):return {"event_id":str(id),"doc_id":"01","side":"index","version":str(ver),"op":op,"document":document or {"a":1},"_sources":[id]}
def test_tombstone_beats_late_old_write():
    "TRAP-13"
    r=evaluate([event(1,5,"delete"),event(2,4)],{})["rows"][0];assert r["version"]=="5" and r["tombstone"] is True
def test_same_version_content_conflict():
    "TRAP-14"
    r=evaluate([event(1,5,document={"a":1}),event(2,5,document={"a":2})],{})
    assert len(r["quarantine"])==2 and r["rows"]==[]
def test_order_independent():
    rows=[event(1,4),event(2,5,"delete")];assert evaluate(rows,{})==evaluate(list(reversed(rows)),{})
def test_same_version_same_content_merged():
    r=evaluate([event(1,5),event(2,5)],{})["rows"][0];assert r["_sources"]==[1,2]
def test_real_tombstones(result): assert result["stages"][2]["metrics"]["tombstones"]==16
def test_real_same_version_conflict_rows(result): assert result["stages"][2]["metrics"]["conflict_rows"]==2
def test_large_versions_compared_exactly(): assert evaluate([event(1,"9007199254740992"),event(2,"9007199254740993")],{})["rows"][0]["version"]=="9007199254740993"

def test_conflicting_latest_not_fallback_to_old_state():
    rows=[event(1,4),event(2,5,document={"a":1}),event(3,5,document={"a":2})]
    result=evaluate(rows,{})
    assert result["rows"]==[] and len(result["quarantine"])==3
