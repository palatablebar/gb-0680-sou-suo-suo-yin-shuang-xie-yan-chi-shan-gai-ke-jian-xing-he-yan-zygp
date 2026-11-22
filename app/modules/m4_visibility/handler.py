from flask import Blueprint,request,jsonify
from app.errors import DomainError
from app.pipeline import stage_preview
bp=Blueprint("visibility",__name__)
@bp.route("/api/visibility",methods=["GET","POST"])
def preview():
    payload=request.get_json(silent=True) if request.method=="POST" else {}
    if payload is None or not isinstance(payload,dict): raise DomainError("BAD_BODY","请求需要对象")
    return jsonify(stage_preview(3,payload))
