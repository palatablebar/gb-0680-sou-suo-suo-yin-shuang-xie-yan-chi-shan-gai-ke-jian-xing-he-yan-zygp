import json
from app.values import number,instant
from app.reasons import reject
from app.errors import DomainError
ALIASES={"新增":"upsert","修改":"upsert","upsert":"upsert","删除":"delete","delete":"delete"}
def evaluate(rows,context):
    good=[];bad=[]
    for row in rows:
        try:
            version=number(row["version"]);op=ALIASES.get(row["op"])
            if version<1 or version!=version.to_integral_value():raise DomainError("BAD_VERSION","版本必须为正整数")
            if op is None or row["side"] not in {"source","index"}:raise DomainError("BAD_OPERATION","操作或数据端无效")
            source=instant(row["source_time"]);visible=instant(row["visible_time"]) if row["visible_time"] not in {"","-","NULL"} else None
            if visible and visible<source:raise DomainError("NEGATIVE_LATENCY","可见时间早于源事件")
            payload=json.loads(row["payload"]) if op=="upsert" else None
            if op=="upsert" and not isinstance(payload,dict):raise DomainError("BAD_PAYLOAD","文档需要JSON对象")
            good.append({**row,"version":format(version.to_integral_value(),"f"),"op":op,"source_at":source.isoformat(),"visible_at":visible.isoformat() if visible else None,"document":payload,"reported":str(number(row["reported"]))})
        except (DomainError,KeyError,ValueError) as e:bad.append(reject(row,getattr(e,"code","BAD_PAYLOAD"),str(e)))
    return {"rows":good,"quarantine":bad,"metrics":{"accepted":len(good),"deletes":sum(r["op"]=="delete" for r in good)}}
