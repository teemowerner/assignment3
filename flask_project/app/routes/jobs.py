from flask import Blueprint, jsonify
from app.extensions import db
from app.models.job import Job  # Job 모델 불러오기

bp = Blueprint("jobs", __name__)

@bp.route("/", methods=["GET"])
def list_jobs():
    jobs = Job.query.all()  # 데이터베이스에서 모든 Job 가져오기
    jobs_list = [{"id": job.id, "title": job.title, "company": job.company} for job in jobs]
    return jsonify({"jobs": jobs_list})
