from collections import defaultdict
import json
from app.reasons import reject,sources
from app.values import number
def signature(row):return json.dumps([row["op"],row.get("document")],sort_keys=True,ensure_ascii=False)
def evaluate(rows,context):
    grouped=defaultdict(list);good=[];bad=[]
    for row in rows:grouped[(row["doc_id"],row["side"],row["version"])].append(row)
    by_doc=defaultdict(list);blocked=set()
    for key,events in sorted(grouped.items()):
        if len(set(signature(e) for e in events))>1:
            bad.extend(reject(e,"SAME_VERSION_CONFLICT","同文档同版本内容冲突") for e in events);blocked.add((key[0],key[1]));continue
        first=sorted(events,key=lambda e:e["event_id"])[0]
        by_doc[(key[0],key[1])].append({**first,"_sources":[n for e in events for n in sources(e)],"version_duplicate_count":len(events)-1})
    for (doc,side),events in sorted(by_doc.items()):
        if (doc,side) in blocked:
            bad.extend(reject(e,"UNRESOLVED_VERSION","当前文档存在版本冲突") for e in events);continue
        winner=max(events,key=lambda e:number(e["version"]))
        good.append({**winner,"_sources":[n for e in events for n in sources(e)],"superseded_versions":sorted([e["version"] for e in events if e is not winner],key=number),"tombstone":winner["op"]=="delete"})
    return {"rows":good,"quarantine":bad,"metrics":{"states":len(good),"tombstones":sum(r["tombstone"] for r in good),"conflict_rows":len(bad)}}
