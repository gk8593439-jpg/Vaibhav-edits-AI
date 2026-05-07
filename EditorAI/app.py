import streamlit as st
import google.generativeai as genai

# 1. YAHAN APNI API KEY DAALEIN (Inverted commas "" ke andar)
API_KEY = "AIzaSyAXOZ2Ew7YCcqXe3qnoQRQ4-yCWGltSbwA"

# AI ko setup karna (Model ka naam 'gemini-pro' kar diya hai taaki error na aaye)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Website ka Title aur Design Setup
st.set_page_config(page_title="VaibhavEdits AI", page_icon="🎬", layout="centered")

# Custom CSS for Dark/Red Theme
custom_css = """
<style>
.stApp { background-color: #0a0a0a; color: #ffffff; }
h1, h2, h3 { color: #ffffff !important; font-family: 'Helvetica', 'Neue Haas Display', sans-serif !important; text-transform: uppercase; letter-spacing: 1px; }
.highlight-red { color: #ff3333; }
.stTextInput > div > div > input { background-color: #1a1a1a; color: #ffffff; border: 1px solid #333333; border-radius: 8px; }
.stTextInput > div > div > input:focus { border-color: #ff3333; box-shadow: none; }
.stButton > button { background-color: transparent; color: #ff3333; border: 1px solid #ff3333; border-radius: 8px; transition: all 0.3s ease; font-weight: bold; }
.stButton > button:hover { background-color: #ff3333; color: #ffffff; border: 1px solid #ff3333; }
div[data-baseweb="toast"] { background-color: #1a1a1a; }
.st-emotion-cache-1rtdyuf, .st-emotion-cache-1v0mbdj { background-color: #1a1a1a; color: #ffffff; border-left-color: #ff3333; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# UI Content
st.markdown("<h1><span class='highlight-red'>VAIBHAVEDITS</span> AI ASSISTANT</h1>", unsafe_allow_html=True)
st.write("Professional editing guidance — CapCut, Alight Motion, aur animation techniques ke baare mein puchiye.")
st.markdown("---")

# User se sawal lena
user_question = st.text_input("Apna doubt yahan type karo...")

# Button dabane par kya hoga
if st.button("Sawal Puchiye"):
    if user_question:
        with st.spinner("AI aapke sawal ka jawab dhoondh raha hai..."):
            
            # 2. Yahan humara AI 'knowledge.txt' file padh raha hai
            try:
                with open("knowledge.txt", "r", encoding="utf-8") as file:
                    mera_data = file.read()
            except:
                mera_data = "Koi extra knowledge nahi mili."

            # AI ko command dena
            prompt = f"""Tum ek expert video editor ho jiska naam VaibhavEdits AI hai.
            Neeche di gayi knowledge ko dhyan mein rakh kar user ke sawal ka jawab aasaan Hindi/Hinglish mein do:

            VAIBHAV KI SECRET KNOWLEDGE:
            {mera_data}

            USER KA SAWAL:
            {user_question}
            """
            
            # AI se jawab lena aur error ko handle karna
            try:
                response = model.generate_content(prompt)
                st.success("Jawab mil gaya!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error aaya hai: {e}")
    else:
        st.warning("Bhai, pehle koi sawal toh type karo!")