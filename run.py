import os
import subprocess
import sys

# Force pure python for 3.14 compatibility before any imports
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

def setup():
    print("Setting up Resume Screening System...")
    
    # Install required packages
    # Use binary wheels for scikit-learn and others to avoid compilation issues on Python 3.14
    # Install required packages
    # Use binary wheels for scikit-learn and others to avoid compilation issues on Python 3.14
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "--only-binary", ":all:", 
                          "Flask==3.0.0", "Flask-SQLAlchemy==3.1.1", "pdfminer.six==20221105", 
                          "python-docx==1.1.0", "nltk==3.9.1", "scikit-learn==1.8.0", 
                          "pandas==3.0.1", "werkzeug==3.1.1", "numpy==2.4.2", "scipy==1.17.1",
                          "python-dotenv==1.0.0", "requests"])

if __name__ == "__main__":
    # Ensure base dependencies are met
    try:
        import nltk
        import docx
    except ImportError:
        setup()

    # Launch Flask using the module path
    # We stay in the root directory so the reloader can find this script
    print("Starting Flask server...")
    try:
        env = os.environ.copy()
        env['FLASK_APP'] = os.path.join('resume_screening', 'app.py')
        env['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'  # Force pure python for 3.14 compatibility
        subprocess.check_call([sys.executable, "-m", "flask", "run", "--debug"], env=env)
    except KeyboardInterrupt:
        print("\nStopping server...")
