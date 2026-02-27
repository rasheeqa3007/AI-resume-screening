import os
# Force pure python for 3.14 compatibility before any imports
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models import db, JobDescription, Resume
from utils import (
    extract_text_from_pdf, 
    extract_text_from_docx, 
    preprocess_text, 
    allowed_file,
    AdvancedAIScreener
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume_screening.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'secret-key-for-session'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Initialize DB
db.init_app(app)

# Ensure upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize Database tables
with app.app_context():
    db.create_all()

# Initialize AI Screener
screener = AdvancedAIScreener()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('job_title')
        description = request.form.get('job_description')
        files = request.files.getlist('resumes')

        if not title or not description or not files:
            flash("Please provide all required fields.")
            return redirect(request.url)

        # 1. Store Job Description
        job = JobDescription(title=title, description=description)
        db.session.add(job)
        db.session.commit()
        
        # 2. Process each resume
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Extract Text
                if filename.endswith('.pdf'):
                    raw_text = extract_text_from_pdf(file_path)
                else:
                    raw_text = extract_text_from_docx(file_path)

                # Advanced AI Analysis (10 steps)
                analysis = screener.analyze_resume(description, raw_text)
                
                # Create Resume object with full AI JSON
                resume = Resume(
                    filename=filename,
                    raw_text=raw_text,
                    ai_analysis=analysis,
                    similarity_score=analysis.get('matching_scores', {}).get('overall_score', 0.0),
                    job_id=job.id
                )
                db.session.add(resume)

        db.session.commit()
        return redirect(url_for('results', job_id=job.id))

    return render_template('index.html')

@app.route('/results/<int:job_id>')
def results(job_id):
    job = JobDescription.query.get_or_404(job_id)
    ranked_resumes = Resume.query.filter_by(job_id=job_id).order_by(Resume.similarity_score.desc()).all()
    return render_template('results.html', job=job, resumes=ranked_resumes)

if __name__ == '__main__':
    app.run(debug=True)
