import streamlit as st
import PyPDF2
import requests

# ✅ Streamlit page config
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume (PDF) and get AI feedback using AI.")

# 🔑 Load API Key from Streamlit secrets
API_KEY = st.secrets["API_KEY"]

# 📄 Upload Resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

# 📥 Extract text from PDF
def extract_text(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# 🤖 Call AI API
def analyze_resume(text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": f"""
You are a resume expert. Analyze this resume and give a structured response:

1. Qualification details
2. Family background
3. Skills
4. Experience
5. Recommended job roles
6. Missing skills
7. Qualities
8. Achievements
9. Overall view of the resume

Resume:
{text}
                """
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# 🚀 Main Flow
if uploaded_file:
    st.success("Resume uploaded successfully ✅")

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing resume with AI... 🤖"):
            resume_text = extract_text(uploaded_file)
            if not resume_text.strip():
                st.error("Could not extract text from PDF. Please check the file.")
            else:
                ai_output = analyze_resume(resume_text)
                st.subheader("🤖 AI Response")
                st.text(ai_output)
