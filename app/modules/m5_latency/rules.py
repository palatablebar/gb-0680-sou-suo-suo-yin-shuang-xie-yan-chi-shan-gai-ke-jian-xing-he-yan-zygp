from decimal import Decimal
from app.values import number,instant
from app.errors import DomainError
def evaluate(rows,context):
    p=context.get("parameters",{});threshold=number(p.get("max_delay_seconds","120"));as_of=instant(p.get("as_of","2026-11-16T10:10:00Z"))
    if threshold<0:raise DomainError("BAD_THRESHOLD","延迟阈值不能为负")
    out=[]
    for row in rows:
        source=instant(row["source_at"]);visible=instant(row["visible_at"]) if row.get("visible_at") else None
        delay=max(Decimal(0),Decimal(str(((visible or as_of)-source).total_seconds())))
        state=row["visibility_state"]
        if state in {"MISSING_INDEX","DELETE_NOT_CONFIRMED"}:gate="缺失" if delay>threshold else "等待"
        elif state!="CONSISTENT":gate="内容差异"
        elif delay>threshold:gate="延迟"
        else:gate="通过"
        out.append({**row,"delay_seconds":str(delay),"gate":gate,"threshold_seconds":str(threshold),"expected":"1","reported":"1" if gate=="通过" else "0"})
    return {"rows":out,"quarantine":[],"metrics":{"pass":sum(r["gate"]=="通过" for r in out),"delayed":sum(r["gate"]=="延迟" for r in out),"missing":sum(r["gate"]=="缺失" for r in out),"waiting":sum(r["gate"]=="等待" for r in out),"mismatch":sum(r["gate"]=="内容差异" for r in out)}}
