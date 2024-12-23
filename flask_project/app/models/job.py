from app.extensions import db  # db 가져오기

class Job(db.Model):  # Job 모델 정의
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Job {self.title} at {self.company}>"
