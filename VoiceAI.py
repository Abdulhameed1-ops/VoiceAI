import streamlit as st
import speech_recognition as sr
import cohere
import os
import platform
from TTS.api import TTS

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Voice AI Assistant",
    layout="centered"
)

COHERE_API_KEY = "bf5Qur8XrFgfmiAoU0KL111qbVud0P2KGQFZvdW8"
co = cohere.Client(COHERE_API_KEY)

# =========================
# SESSION STATE
# =========================
if "ai_name" not in st.session_state:
    st.session_state.ai_name = "Nova"

if "ai_role" not in st.session_state:
    st.session_state.ai_role = "A smart, friendly voice assistant"

# =========================
# CSS (ORB ANIMATION)
# =========================
st.markdown("""
<style>
body {
    background: #0f172a;
    color: white;
}

.orb {
    width: 160px;
    height: 160px;
    margin: 20px auto;
    border-radius: 50%;
    background: radial-gradient(circle, #6366f1, #020617);
    animation: pulse 2s infinite;
    box-shadow: 0 0 45px #6366f1;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.15); }
    100% { transform: scale(1); }
}

button {
    background-color: #6366f1 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TEXT TO SPEECH MODELS
# =========================
voices = {
    "Female – Fast": "tts_models/en/ljspeech/tacotron2-DDC",
    "Female – Natural": "tts_models/en/vctk/vits"
}

@st.cache_resource
def load_tts(model_name):
    return TTS(model_name)

# =========================
# FUNCTIONS
# =========================
def listen_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return ""

def speak(text, voice):
    tts = load_tts(voices[voice])
    tts.tts_to_file(text=text, file_path="reply.wav")

    if platform.system() == "Windows":
        os.system("start reply.wav")
    elif platform.system() == "Linux":
        os.system("aplay reply.wav")
    elif platform.system() == "Darwin":
        os.system("afplay reply.wav")

def ai_response(user_text):
    response = co.generate(
        model="command-a-03-2025",
        prompt=f"""
You are {st.session_state.ai_name}.
Role: {st.session_state.ai_role}

User: {user_text}
AI:
""",
        max_tokens=200
    )
    return response.generations[0].text.strip()

def open_apps(command):
    apps = {
        "chrome": "chrome",
        "calculator": "calc",
        "notepad": "notepad"
    }

    for app in apps:
        if app in command.lower():
            os.system(apps[app])

# =========================
# UI
# =========================
st.markdown("<div class='orb'></div>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align:center'>{st.session_state.ai_name}</h2>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🎤 Assistant", "⚙️ Settings"])

with tab1:
    selected_voice = st.selectbox("Select Voice", list(voices.keys()))

    if st.button("🎙️ Talk"):
        user_text = listen_voice()
        st.write("**You:**", user_text)

        if user_text:
            open_apps(user_text)
            reply = ai_response(user_text)
            st.write(f"**{st.session_state.ai_name}:**", reply)
            speak(reply, selected_voice)

with tab2:
    st.session_state.ai_name = st.text_input(
        "AI Name",
        st.session_state.ai_name
    )

    st.session_state.ai_role = st.text_area(
        "AI Role / Personality",
        st.session_state.ai_role
    )
    
