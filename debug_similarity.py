import sys
import os

# Add the app directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'resume_screening'))

from resume_screening.utils import preprocess_text, calculate_similarity

jd = "Python developer with Flask and SQLAlchemy experience. Knowledge of Machine Learning and NLP is a plus."
resumes = [
    "I am a Python developer. I have experience with Flask and SQLAlchemy. I also know Machine Learning and NLP.",
    "This is a random text about cooking pasta with tomatoes and cheese.",
    "Experienced software engineer working with Java and Spring Boot. Familiar with AWS and Docker."
]

p_jd = preprocess_text(jd)
p_resumes = [preprocess_text(r) for r in resumes]

print(f"Processed JD: {p_jd}")
for i, r in enumerate(p_resumes):
    print(f"Processed Resume {i}: {r}")

scores = calculate_similarity(p_jd, p_resumes)
print(f"Scores: {scores}")
