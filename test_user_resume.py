import sys
import os

# Add the app directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'resume_screening'))

from resume_screening.utils import extract_text_from_pdf, preprocess_text

pdf_path = r"c:\Users\Admin\resume-screening\uploads\Kayalvizhi_Resume_Professional_Bordered.pdf"

if os.path.exists(pdf_path):
    print(f"File exists: {pdf_path}")
    raw_text = extract_text_from_pdf(pdf_path)
    print(f"Raw Text Length: {len(raw_text)}")
    print(f"Raw Text (first 500 chars): {repr(raw_text[:500])}")
    
    p_text = preprocess_text(raw_text)
    print(f"Processed Text Length: {len(p_text)}")
    print(f"Processed Text (first 500 chars): {repr(p_text[:500])}")
else:
    print(f"File NOT found: {pdf_path}")
