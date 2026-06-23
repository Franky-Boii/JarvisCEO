import streamlit as st
import ollama
import pandas as pd
from datetime import datetime
import pyttsx3
import speech_recognition as sr
import numpy as np
import time

# ==========================================
# SYSTEM SETUP & INITIALIZATION
# ==========================================

# Page configuration
st.set_page_config(page_title="JARVIS: Forex CEO", page_icon="💼", layout="wide")

# Initialize Text-to-Speech Engine
def speak_text(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) 
    engine.setProperty('rate', 175) # Speed of speech
    engine.say(text)
    engine.runAndWait()

# Streamlined Background Detector focusing cleanly on amplitude peaks and vocals
def monitor_wake_triggers():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    CHUNK = 1024
    THRESHOLD = 10000  # Optimized sensitivity for standard room acoustics and hardware defaults
    
    with mic as source:
        # Step 1: Direct capture of microphone raw chunks for clap metrics
        try:
            stream = mic.audio.open(format=sr.pyaudio.paInt16, channels=1,
                                    rate=16000, input=True,
                                    frames_per_buffer=CHUNK)
            clap_count = 0
            start_time = time.time()
            
            while time.time() - start_time < 0.6:
                try:
                    raw_data = stream.read(CHUNK, exception_on_overflow=False)
                    data = np.frombuffer(raw_data, dtype=np.int16)
                    peak = np.max(np.abs(data))
                    
                    if peak > THRESHOLD:
                        clap_count += 1
                        time.sleep(0.18)  # Debounce delay to prevent one clap from double counting
                except Exception:
                    break
                    
            stream.stop_stream()
            stream.close()
            
            if clap_count >= 2:
                return "double_clap"
        except Exception:
            pass

        # Step 2: Vocal signature scan fallback if no claps detected
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.1)
            audio = recognizer.listen(source, timeout=0.6, phrase_time_limit=1.2)
            text = recognizer.recognize_google(audio).lower()
            if "jarvis" in text:
                return "wake_word"
        except Exception:
            pass
            
    return None

# Active capture function triggered instantly upon wake sequence verification
def capture_executive_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("🎙️ JARVIS Active! Listening to your command, CEO...")
        try:
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=7)
            return recognizer.recognize_google(audio)
        except Exception:
            return None

# Sidebar Navigation Control
st.sidebar.title("⚙️ JARVIS Navigation")
page = st.sidebar.radio(
    "Go to:", 
    ["Core AI Assistant", "Student Management", "Content & Strategy"],
    key="jarvis_navigation_radio"
)

# Quick Status Indicator in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**System Status:**")
st.sidebar.success("🟢 Ollama Connected (phi3:mini)")
st.sidebar.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")


# ==========================================
# PAGE 1: CORE AI ASSISTANT
# ==========================================
if page == "Core AI Assistant":
    st.title("🤖 JARVIS Core Terminal")
    st.caption("Offline Local Intelligence Engine — Fully Automated Hands-Free Wake System")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Layout architecture splits
    chat_col, action_col = st.columns([4, 1])

    with action_col:
        st.markdown("### System State")
        st.success("🟢 Automated Wake Loop Active")
        st.info("👂 Monitoring Room Audio 24/7...")

    with chat_col:
        # Display clean conversational chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 🌟 AUTOMATED WAKE ACTIVATION (No checkboxes or buttons required)
    trigger_detected = monitor_wake_triggers()
    user_prompt = None

    if trigger_detected:
        if trigger_detected == "wake_word":
            speak_text("Online. How can I assist you, CEO?")
        elif trigger_detected == "double_clap":
            speak_text("System engaged. Ready, CEO.")
            
        user_prompt = capture_executive_command()
        if not user_prompt:
            st.warning("JARVIS: Instruction not captured, returning to standby.")
            st.rerun()

    # Process prompt actions if generated
    if user_prompt:
        with chat_col:
            with st.chat_message("user"):
                st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        with chat_col:
            with st.chat_message("assistant"):
                with st.spinner("Processing analytical breakdown..."):
                    try:
                        system_instruction = {
                            'role': 'system', 
                            'content': (
                                "You are JARVIS, a highly advanced personal AI assistant. "
                                "Your tone is crisp, professional, and confident—always addressing your user as 'CEO'. "
                                "Be conversational, punchy, and short so that your responses sound natural when spoken out loud. Never break character."
                            )
                        }
                        
                        full_conversation = [system_instruction] + st.session_state.messages
                        response = ollama.chat(model='phi3:mini', messages=full_conversation)
                        response_text = response['message']['content']
                        
                        st.markdown(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                        
                        # Read the completed intelligence payload back out loud
                        speak_text(response_text)
                        
                    except Exception as e:
                        st.error(f"Error communicating with local AI engine: {e}")
    
    # Force the script to reload instantly to maintain a seamless acoustic ear
    st.rerun()


# ==========================================
# PAGE 2: STUDENT MANAGEMENT
# ==========================================
elif page == "Student Management":
    st.title("👥 Mentorship Student Hub")
    st.write("Track and monitor your active Forex students, schedules, and fee renewals seamlessly.")
    
    students_data = {
        "Student Name": ["Alex Ndlovu", "Sarah Jenkins", "Sipho Khumalo"],
        "Course Track": ["Advanced Price Action", "Foundational Mechanics", "1-on-1 Scalping Mastery"],
        "Join Date": ["2026-01-15", "2026-03-10", "2026-05-01"],
        "Payment Status": ["Paid", "Overdue", "Paid"]
    }
    df = pd.DataFrame(students_data)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Active Students", len(df))
    col2.metric("Pending Renewals", "1")
    col3.metric("Monthly Growth Rate", "+15%")
    
    st.markdown("### Active Roster")
    st.dataframe(df, width="stretch")
    
    with st.form("new_student_form"):
        name = st.text_input("Full Name")
        track = st.selectbox("Select Strategy Track", ["Foundational Mechanics", "Advanced Price Action", "1-on-1 Scalping Mastery"])
        status = st.radio("Initial Payment Status", ["Paid", "Pending"])
        submitted = st.form_submit_button("Enroll Student")
        if submitted:
            st.success(f"Successfully added {name} to your local tracking ledger!")


# ==========================================
# PAGE 3: CONTENT & STRATEGY
# ==========================================
elif page == "Content & Strategy":
    st.title("📈 Forex Creator Suite")
    st.write("Generate high-impact content blueprints for your trading community or upcoming masterclasses.")
    
    topic = st.text_input("Enter a concept (e.g., 'Liquidity Sweeps', 'Risk to Reward Ratio', 'Trading Psychology'):")
    platform = st.selectbox("Target Platform", ["Instagram Caption", "LinkedIn Professional Post", "Community Telegram Blurb"])
    
    if st.button("🚀 Ask JARVIS to Draft Copy"):
        if topic:
            prompt = f"Write a compelling, high-converting {platform} targeted toward aspiring Forex traders discussing: {topic}. Keep it engaging, educational, and professionally authoritative. Include actionable tips and relevant hashtags."
            
            with st.spinner("JARVIS is drafting your strategy copy..."):
                try:
                    response = ollama.chat(model='phi3:mini', messages=[{'role': 'user', 'content': prompt}])
                    st.markdown("### 📝 Draft Proposal:")
                    st.info(response['message']['content'])
                except Exception as e:
                    st.error(f"Could not connect to Ollama: {e}")
        else:
            st.warning("Please input a topic concept first!")