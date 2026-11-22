from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from datetime import datetime, timezone
import unicodedata
from app.errors import DomainError
SENTINELS={"","-","N/A","NULL","未知"}
def number(value):
    text=unicodedata.normalize("NFKC",str(value)).strip().replace(",","")
    if text.upper() in SENTINELS: raise DomainError("EMPTY_VALUE","数字不能为空")
    try:
        result=Decimal(text)
        if not result.is_finite(): raise InvalidOperation()
        return result
    except InvalidOperation: raise DomainError("INVALID_NUMBER","数字格式错误")
def money(value): return str(number(value).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP))
def instant(value):
    try:
        result=datetime.fromisoformat(str(value).replace("Z","+00:00"))
        if result.tzinfo is None: raise ValueError()
        return result.astimezone(timezone.utc)
    except (TypeError, ValueError): raise DomainError("INVALID_TIME","时间需要明确偏移")
def scalar(value):
    if isinstance(value,Decimal): return str(value)
    if isinstance(value,datetime): return value.isoformat()
    if isinstance(value,dict): return {k:scalar(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [scalar(v) for v in value]
    return value
