import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# YAHAN APNI API KEY DAALEIN
API_KEY = "AIzaSyAXOZ2Ew7YCcqXe3qnoQRQ4-yCWGltSbwA"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="VaibhavEdits AI", page_icon="🎬", layout="centered")

custom_css = """
<style>
.stApp { background-color: #0a0a0a; color: #ffffff; }
h1, h2, h3 { color: #ffffff !important; font-family: 'Helvetica', sans-serif !important; letter-spacing: 1px; }
.highlight-red { color: #ff3333; }
.stTextInput > div > div > input { background-color: #1a1a1a; color: #ffffff; border: 1px solid #333333; border-radius: 8px; }
.stTextInput > div > div > input:focus { border-color: #ff3333; box-shadow: none; }
.stButton > button { background-color: transparent; color: #ff3333; border: 1px solid #ff3333; border-radius: 8px; font-weight: bold; width: 100%; }
.stButton > button:hover { background-color: #ff3333; color: #ffffff; border: 1px solid #ff3333; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<h1><span class='highlight-red'>VAIBHAVEDITS</span> AI ASSISTANT</h1>", unsafe_allow_html=True)
st.write("CapCut, Alight Motion, aur editing techniques ke baare mein puchiye. Ya phir kisi YouTube tutorial ka link daalkar uske baare mein sawal karein!")

# 1. YOUTUBE LINK WALA BOX (User chahe toh use kare)
yt_link = st.text_input("🎥 YouTube Video ka Link yahan daalein (Optional)...")
yt_knowledge = ""

if yt_link:
    with st.spinner("Video ki script nikali ja rahi hai..."):
        try:
            # Link se Video ID nikalna
            video_id = ""
            if "youtu.be" in yt_link:
                video_id = yt_link.split("/")[-1].split("?")[0]
            elif "watch?v=" in yt_link:
                video_id = yt_link.split("v=")[1].split("&")[0]
            
            # YouTube se text nikalna
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en', 'en-IN'])
            yt_knowledge = " ".join([i['text'] for i in transcript_list])
            st.success("✅ AI ne is nayi video ki script padh li hai! Ab sawal puchiye.")
        except Exception as e:
            st.error("Error: Is video ke subtitles available nahi hain.")

# 2. SAWAL POOCHNE WALA BOX
user_question = st.text_input("Apna doubt yahan type karo...")

if st.button("Sawal Puchiye"):
    if user_question:
        with st.spinner("AI jawab dhoondh raha hai..."):
            try:
                # AI ki pehle se saved knowledge (jo aapne brain_maker se daali hogi)
                with open("knowledge.txt", "r", encoding="utf-8") as file:
                    file_data = file.read()
            except:
                file_data = "Koi saved data nahi mila."

            # AI KO COMMAND DENA (Saved Knowledge + Naya YouTube Link)
            prompt = f"""Tum ek expert video editor ho jiska naam VaibhavEdits AI hai.
            Neeche di gayi knowledge ko dhyan mein rakh kar user ke sawal ka ekdum aasaan Hindi/Hinglish mein jawab do.

            VAIBHAV KI SECRET KNOWLEDGE (Pehle se saved videos/tips):
            {file_data}

            USER KE DIYE GAYE YOUTUBE VIDEO KI SCRIPT (Agar koi link diya hai):
            {yt_knowledge}

            USER KA SAWAL:
            {user_question}
            """
            
            try:
                response = model.generate_content(prompt)
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Bhai, pehle koi sawal toh type karo!")
