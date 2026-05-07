import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# 1. API KEY
API_KEY = "AIzaSyAXOZ2Ew7YCcqXe3qnoQRQ4-yCWGltSbwA"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="VaibhavEdits AI", page_icon="🎬", layout="centered")

# Custom CSS for Modern Inline Design
custom_css = """
<style>
.stApp { background-color: #0a0a0a; color: #ffffff; }
h1 { color: #ffffff !important; font-family: 'Helvetica', sans-serif !important; text-align: center; }
.highlight-red { color: #ff3333; }

/* Expander (Plus Section) */
.streamlit-expanderHeader {
    background-color: #1a1a1a !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
    color: #ff3333 !important;
}

/* Input Bar & Button in One Row */
.stTextInput > div > div > input {
    background-color: #1a1a1a;
    color: #ffffff;
    border: 1px solid #333;
    border-radius: 15px;
    padding: 10px 20px;
}

/* Button Fixed */
.stButton > button {
    background-color: #ff3333;
    color: white;
    border-radius: 12px;
    border: none;
    height: 45px;
    width: 100%;
    font-weight: bold;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<h1><span class='highlight-red'>VAIBHAVEDITS</span> AI ASSISTANT</h1>", unsafe_allow_html=True)

# Plus Section - Ise upar hi rakhte hain taaki link add ho sake
yt_knowledge = ""
with st.expander("➕ Link YouTube Video for Reference"):
    yt_link = st.text_input("Paste URL here...")
    if yt_link:
        try:
            video_id = yt_link.split("v=")[1].split("&")[0] if "v=" in yt_link else yt_link.split("/")[-1]
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en'])
            yt_knowledge = " ".join([t['text'] for t in transcript])
            st.success("✅ Linked!")
        except:
            st.error("Error linking video.")

st.write("") # Thoda space

# MAIN INPUT & BUTTON (Ek sath)
col1, col2 = st.columns([5, 1]) # Column system se dono ko ek hi line mein laya

with col1:
    user_question = st.text_input("", placeholder="Ask Gemini... (VaibhavEdits Edition)", label_visibility="collapsed")

with col2:
    submit = st.button("Puchiye")

if submit and user_question:
    with st.spinner("Processing..."):
        try:
            with open("knowledge.txt", "r", encoding="utf-8") as f:
                saved_k = f.read()
        except:
            saved_k = ""

        prompt = f"Knowledge: {saved_k}\nVideo: {yt_knowledge}\nUser: {user_question}\n(Expert response in Hinglish)"
        response = model.generate_content(prompt)
        
        st.markdown("---")
        st.markdown(f"### 🎬 VaibhavEdits AI:\n{response.text}")
