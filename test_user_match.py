import sys
import os

# Add the app directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'resume_screening'))

from resume_screening.utils import preprocess_text, calculate_similarity

# User's JD from error message
jd = """Backend: Python Flask
- Frontend: HTML, CSS (Bootstrap optional)
- Database: SQLite (or MySQL optional)
- Resume Parsing: Extract text from PDF and DOCX files
- NLP Processing: Use spaCy or NLTK
- Machine Learning: Match resume with job description using TF-IDF or cosine similarity
- File Upload: Allow users to upload resumes
- Admin Panel: HR can input job description
- Scoring System: Calculate matching score (0–100%)
- Display Results: Show ranked candidates"""

# User's Resume (extracted earlier)
resume_text = """Kayalvizhi

Email: ms.kayalmayakrishnan1225@gmail.com
GitHub: https://github.com/kayal-254
LinkedIn: https://linkedin.com/in/kayal-mayakrishnan

PROFESSIONAL SUMMARY

Prefinal Year B.Tech student in Artificial Intelligence and Data Science with strong foundation in
Machine Learning, Python, and Data Analysis. Passionate about building intelligent systems and
solving real-world problems using AI-driven solutions.

EDUCATION

B.Tech  Artificial Intelligence and Data Science
Acharya College of Engineering and Technology
Technical Skills: Programming: Java, Python, C, C++, Web Technology: HTML, CSS"""

p_jd = preprocess_text(jd)
p_resume = preprocess_text(resume_text)

print(f"P_JD: {repr(p_jd)}")
print(f"P_Resume: {repr(p_resume)}")

overlap = set(p_jd.split()) & set(p_resume.split())
print(f"Common Words: {overlap}")

score = calculate_similarity(p_jd, [p_resume])
print(f"Calculated Score: {score}")
