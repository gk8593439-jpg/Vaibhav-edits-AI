import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# 1. API KEY
API_KEY = "AIzaSyAXOZ2Ew7YCcqXe3qnoQRQ4-yCWGltSbwA"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="VaibhavEdits AI", page_icon="🎬", layout="centered")

# Custom CSS for Gemini-like Input Bar
custom_css = """
<style>
.stApp { background-color: #0a0a0a; color: #ffffff; }
h1 { color: #ffffff !important; font-family: 'Helvetica', sans-serif !important; text-align: center; font-weight: bold; }
.highlight-red { color: #ff3333; }

/* Plus button styling */
.streamlit-expanderHeader {
    background-color: transparent !important;
    border: none !important;
    color: #888 !important;
    font-size: 20px !important;
}
.streamlit-expanderContent {
    border: 1px solid #333 !important;
    border-radius: 15px;
    background-color: #1a1a1a !important;
    margin-bottom: 20px;
}

/* Main Input Area Style */
.stTextInput > div > div > input {
    background-color: #1a1a1a;
    color: #ffffff;
    border: 1px solid #333;
    border-radius: 25px;
    padding: 15px 25px;
}
.stTextInput > div > div > input:focus {
    border-color: #ff3333;
}

/* Send Button Style */
.stButton > button {
    background-color: #ff3333;
    color: white;
    border-radius: 20px;
    border: none;
    padding: 10px 30px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<h1><span class='highlight-red'>VAIBHAVEDITS</span> AI ASSISTANT</h1>", unsafe_allow_html=True)

# 2. THE "+" SECTION (Expander)
# Isme user link daal kar knowledge add kar sakta hai
yt_knowledge = ""
with st.expander("➕ Click to link a YouTube Tutorial"):
    st.info("Yahan link daalne se AI is video ko bhi samjh lega.")
    yt_link = st.text_input("YouTube URL...")
    if yt_link:
        try:
            video_id = yt_link.split("v=")[1].split("&")[0] if "v=" in yt_link else yt_link.split("/")[-1]
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en'])
            yt_knowledge = " ".join([t['text'] for t in transcript])
            st.success("✅ Video Knowledge Added!")
        except:
            st.error("Is video ke subtitles nahi mil rahe.")

# 3. MAIN INTERFACE (Question & Button)
user_question = st.text_input("", placeholder="Ask Gemini... (VaibhavEdits Edition)")

col1, col2, col3 = st.columns([4,1,4])
with col2:
    submit = st.button("Sawal Puchiye")

if submit and user_question:
    with st.spinner("Processing..."):
        try:
            with open("knowledge.txt", "r", encoding="utf-8") as f:
                saved_k = f.read()
        except:
            saved_k = ""

        prompt = f"Saved Knowledge: {saved_k}\nVideo Knowledge: {yt_knowledge}\nUser: {user_question}\n(Expert Video Editor ki tarah Hinglish mein jawab do)"
        
        response = model.generate_content(prompt)
        st.markdown("---")
        st.markdown(f"**VaibhavEdits AI:** {response.text}")
