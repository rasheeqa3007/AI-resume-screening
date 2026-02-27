import os
import re
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import docx
from pdfminer.high_level import extract_text as extract_pdf_text
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Download necessary NLTK data
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except Exception as e:
    print(f"Error downloading NLTK data: {e}")

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

class AdvancedAIScreener:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def analyze_resume(self, job_description, resume_text):
        if not self.api_key or self.api_key == "your_api_key_here":
            return self._get_mock_response(error="Missing Groq API Key. Please add GROQ_API_KEY to your .env file.")

        full_prompt = f"""
        You are a professional HR AI assistant. Perform a detailed 10-step analysis of the following resume against the provided job description. Ensure complete bias control by ignoring personal attributes like name, gender, age, religion, address, marital status, or photo.

        JOB DESCRIPTION:
        {job_description}

        RESUME TEXT:
        {resume_text}

        ---------------------------
        ANALYSIS STEPS:
        ---------------------------
        STEP 1: RESUME STRUCTURED EXTRACTION
        Extract Name, Total Years of Experience (estimate if not explicit), Education, Technical Skills, Soft Skills, Tools, Certifications, Projects (with domain), Work Experience, Leadership indicators, Collaboration indicators, and Research/Innovation indicators.

        STEP 2: JOB DESCRIPTION ANALYSIS
        Extract Job Role Category, Mandatory Skills, Preferred Skills, Required Experience Level, Key Responsibilities, and Industry Domain.

        STEP 3: SEMANTIC SKILL MATCHING
        Perform contextual matching (e.g., REST API = Backend). Compute Skill Match %, Experience Match Level, Project Relevance, and Certification Relevance.

        STEP 4: SCORING MODEL (Weighted 0-100%)
        Calculate Score using: 50% Skill Match, 25% Experience Match, 15% Project Relevance, 10% Certification & Tools Relevance.

        STEP 5: SKILL GAP ANALYSIS
        Identify missing required/preferred skills and weak experience areas. Suggest certifications, courses, and project ideas.

        STEP 6: RESUME QUALITY ANALYSIS
        Evaluate grammar, action verbs, ATS compatibility, structure, and length. Provide specific improvement tips.

        STEP 7: PERSONALITY & PROFESSIONAL TRAITS
        Predict Leadership Orientation, Team Collaboration, Technical Depth, Innovation Mindset, and Communication Strength.

        STEP 8: BIAS CONTROL
        Explicitly ensure non-merit factors (name, age, etc.) are excluded from scoring.

        STEP 9: EXPLAINABLE AI OUTPUT
        Provide a clear explanation for the score, highlighting strong and weak areas.

        STEP 10: HIRING RECOMMENDATION
        Categorize as Strong Hire, Consider, Reject, or Upskill & Reapply.

        ---------------------------
        OUTPUT FORMAT (STRICT JSON ONLY):
        ---------------------------
        RETURN ONLY VALID STRICT JSON.

        {{
          "candidate_summary": {{
            "name": "",
            "experience_years": "",
            "education": "",
            "primary_skills": [],
            "secondary_skills": [],
            "certifications": [],
            "project_domains": []
          }},
          "job_analysis": {{
            "job_role": "",
            "required_skills": [],
            "preferred_skills": [],
            "required_experience": "",
            "industry_domain": ""
          }},
          "matching_scores": {{
            "overall_score": 0.0,
            "skill_match_percentage": 0.0,
            "experience_match_level": "Low/Medium/High",
            "project_relevance_score": 0.0,
            "certification_relevance_score": 0.0
          }},
          "strong_matches": [],
          "missing_skills": [],
          "skill_gap_recommendations": {{
            "recommended_certifications": [],
            "recommended_courses": [],
            "project_suggestions": []
          }},
          "resume_quality_feedback": {{
            "grammar_feedback": "",
            "action_verb_feedback": "",
            "ats_compatibility": "",
            "length_feedback": ""
          }},
          "personality_insights": {{
            "leadership_level": "Low/Medium/High",
            "teamwork_level": "Low/Medium/High",
            "technical_depth": "Low/Medium/High",
            "innovation_mindset": "Low/Medium/High",
            "communication_strength": "Low/Medium/High"
          }},
          "final_explanation": "",
          "hiring_recommendation": "Strong Hire / Consider / Reject / Upskill & Reapply"
        }}
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are an expert HR analyst. Always respond in valid JSON format."},
                {"role": "user", "content": full_prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            ai_text = data['choices'][0]['message']['content']
            
            # Find and parse JSON
            match = re.search(r'\{.*\}', ai_text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return self._get_mock_response(error="Could not parse Groq response")
        except Exception as e:
            print(f"Groq API Error: {e}")
            return self._get_mock_response(error=str(e))


    def _get_mock_response(self, error=None):
        return {
            "candidate_summary": {
                "name": "N/A (Mock Mode)",
                "experience_years": "N/A",
                "education": "N/A",
                "primary_skills": ["Mocking"],
                "secondary_skills": [],
                "certifications": [],
                "project_domains": []
            },
            "job_analysis": {
                "job_role": "N/A",
                "required_skills": [],
                "preferred_skills": [],
                "required_experience": "N/A",
                "industry_domain": "N/A"
            },
            "matching_scores": {
                "overall_score": 0.0 if error else 50.0,
                "skill_match_percentage": 0.0,
                "experience_match_level": "Medium",
                "project_relevance_score": 0.0,
                "certification_relevance_score": 0.0
            },
            "strong_matches": [],
            "missing_skills": ["Gemini API Key Missing or Error"],
            "skill_gap_recommendations": {
                "recommended_certifications": [],
                "recommended_courses": [],
                "project_suggestions": []
            },
            "resume_quality_feedback": {
                "grammar_feedback": "N/A",
                "action_verb_feedback": "N/A",
                "ats_compatibility": "N/A",
                "length_feedback": "N/A"
            },
            "personality_insights": {
                "leadership_level": "Medium",
                "teamwork_level": "Medium",
                "technical_depth": "Medium",
                "innovation_mindset": "Medium",
                "communication_strength": "Medium"
            },
            "final_explanation": f"MOCK MODE: {error or 'Please provide a valid Gemini API key in the .env file to enable full AI screening.'}",
            "hiring_recommendation": "Upskill & Reapply"
        }


def extract_text_from_pdf(pdf_path):
    try:
        return extract_pdf_text(pdf_path)
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return ""

def preprocess_text(text):
    if not text: return ""
    # Clean text
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    # Tokenization
    tokens = word_tokenize(text)
    # Lemmatize and filter stopwords
    return " ".join([lemmatizer.lemmatize(t) for t in tokens if t not in stop_words])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx'}
