import streamlit as st
import PyPDF2
import requests

# 🔑 OpenRouter API Key
API_KEY = "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"

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get AI feedback")

# 📄 Upload
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

# 📥 Extract text
def extract_text(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# 🤖 AI FUNCTION
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
                You are a resume expert.

                Analyze this resume and give:
                - qualification details
                - family background
                - skills
                - experience
                - job role he can get
                - misiing skills
                - qualities
                - archeivements
                - overall view of resume

                Resume:
                {text}
                """
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"

# 🚀 MAIN FLOW
if uploaded_file:

    st.success("Resume uploaded successfully ✅")

    resume_text = extract_text(uploaded_file)

    if st.button("Analyze Resume"):

        with st.spinner("Analyzing with AI... 🤖"):

            ai_output = analyze_resume(resume_text)

            st.subheader("🤖 AI Response")
            st.write(ai_output)
