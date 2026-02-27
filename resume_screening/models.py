from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class JobDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    candidate_name = db.Column(db.String(200))
    raw_text = db.Column(db.Text)
    processed_text = db.Column(db.Text)
    similarity_score = db.Column(db.Float)
    ai_analysis = db.Column(db.JSON)  # Store the full 10-step analysis
    job_id = db.Column(db.Integer, db.ForeignKey('job_description.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    job = db.relationship('JobDescription', backref=db.backref('resumes', lazy=True))
