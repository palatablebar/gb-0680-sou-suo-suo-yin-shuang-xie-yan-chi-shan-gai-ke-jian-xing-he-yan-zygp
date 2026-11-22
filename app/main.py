from flask import Flask,jsonify,request,send_from_directory
from app.config import ROOT,DATA_DIR,MODULES
from app.errors import DomainError
from app import pipeline,store
from app.web import register_pages
import importlib
def create_app():
    application=Flask(__name__,template_folder="templates",static_folder="static")
    application.config["MAX_CONTENT_LENGTH"]=4*1024*1024
    @application.errorhandler(DomainError)
    def domain_error(error): return jsonify({"code":error.code,"message":error.message}),error.status
    @application.errorhandler(KeyError)
    @application.errorhandler(TypeError)
    @application.errorhandler(ValueError)
    def invalid_shape(error): return jsonify({"code":"INVALID_INPUT","message":"字段或参数无效，请核对输入"}),422
    @application.errorhandler(413)
    def too_large(error): return jsonify({"code":"TOO_LARGE","message":"文件超过4MB"}),413
    @application.get("/healthz")
    def health(): return {"status":"ok"}
    @application.post("/api/runs")
    def runs():
        payload=request.get_json(silent=True)
        if not isinstance(payload,dict): raise DomainError("BAD_BODY","请求需要对象")
        params=payload.get("parameters",{})
        if not isinstance(params,dict): raise DomainError("BAD_PARAMETERS","参数需要对象")
        raw=payload.get("csv")
        if raw is not None and not isinstance(raw,str): raise DomainError("BAD_CSV","CSV需要文本")
        return pipeline.execute(raw.encode() if raw is not None else pipeline.load_sample(payload.get("sample","dirty.csv")),params)
    @application.post("/api/upload")
    def upload():
        file=request.files.get("file")
        if not file: raise DomainError("NO_FILE","请选择CSV文件")
        return pipeline.execute(file.read())
    @application.get("/api/runs")
    def history(): return {"runs":store.history()}
    @application.get("/api/runs/<run_id>")
    def run_detail(run_id): return store.get(run_id)
    @application.post("/api/runs/<run_id>/review")
    def review(run_id):
        p=request.get_json(silent=True) or {}
        if not isinstance(p.get("version"),int): raise DomainError("BAD_VERSION","请提供版本号")
        return store.review(run_id,p["version"],p.get("decision"))
    @application.get("/api/runs/<run_id>/archive")
    def archive(run_id):
        from app.archive import build_archive
        run=store.get(run_id)
        return application.response_class(build_archive(run),mimetype="text/csv",headers={"Content-Disposition":'attachment; filename="evidence.csv"'})
    for index,(slug,title) in enumerate(MODULES,1):
        module=importlib.import_module(f"app.modules.m{index}_{slug}.handler")
        application.register_blueprint(module.bp)
    register_pages(application)
    return application
app=create_app()
if __name__=="__main__": app.run(host="0.0.0.0",port=8000,threaded=True)
