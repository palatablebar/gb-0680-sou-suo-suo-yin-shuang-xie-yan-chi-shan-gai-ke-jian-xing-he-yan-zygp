import hashlib,json,time
from datetime import datetime,timezone
from app.config import RULE_VERSION
def digest(raw,params=None):
    return hashlib.sha256(raw+json.dumps(params or {},sort_keys=True,ensure_ascii=False).encode()+RULE_VERSION.encode()).hexdigest()
def manifest(raw,params,started):
    return {"input_sha256":hashlib.sha256(raw).hexdigest(),"rule_version":RULE_VERSION,"parameters":params,"generated_at":datetime.now(timezone.utc).isoformat(),"elapsed_ms":round((time.monotonic()-started)*1000,2)}
