import sys
import os

# Add the app directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'resume_screening'))

from resume_screening.app import app
from resume_screening.models import db, JobDescription, Resume

with app.app_context():
    jobs = JobDescription.query.all()
    print(f"Total Jobs: {len(jobs)}")
    for j in jobs:
        print(f"Job ID: {j.id}, Title: {j.title}")
        print(f"Description (snippet): {j.description[:200]}...")
        
        resumes = Resume.query.filter_by(job_id=j.id).all()
        print(f"  Total Resumes: {len(resumes)}")
        for r in resumes:
            print(f"    Resume ID: {r.id}, File: {r.filename}, Score: {r.similarity_score}")
            print(f"    Raw Text Length: {len(r.raw_text) if r.raw_text else 0}")
            print(f"    Processed Text Length: {len(r.processed_text) if r.processed_text else 0}")
            print(f"    Processed Text Snippet: {r.processed_text[:100] if r.processed_text else 'EMPTY'}")
