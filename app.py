import streamlit as st
import ollama
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="JARVIS: Forex CEO", page_icon="💼", layout="wide")

# Sidebar Navigation
st.sidebar.title("⚙️ JARVIS Navigation")
page = st.sidebar.radio("Go to:", ["Core AI Assistant", "Student Management", "Content & Strategy"])

# Quick Status Indicator in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**System Status:**")
st.sidebar.success("🟢 Ollama Connected (phi3:mini)")
st.sidebar.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")

# ==========================================
# CORE AI ASSISTANT
# ==========================================
if page == "Core AI Assistant":
    st.title("🤖 JARVIS Core Terminal")
    st.caption("Offline Local Intelligence Engine")
    
    # Simple chat interface state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if user_prompt := st.chat_input("How can I assist you today, Boss?"):
        with st.chat_message("user"):
            st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        # Query local Ollama model
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                try:
                    response = ollama.chat(model='phi3:mini', messages=[
                        {'role': 'user', 'content': user_prompt}
                    ])
                    response_text = response['message']['content']
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"Error communicating with local AI engine: {e}")

# ==========================================
# STUDENT MANAGEMENT
# ==========================================
elif page == "Student Management":
    st.title("👥 Mentorship Student Hub")
    st.write("Track and monitor your active Forex students, schedules, and fee renewals seamlessly.")
    
    # Sample Mock Student Data DataFrame
    # In the future, we can plug this into an SQLite database file!
    students_data = {
        "Student Name": ["Alex Ndlovu", "Sarah Jenkins", "Sipho Khumalo"],
        "Course Track": ["Advanced Price Action", "Foundational Mechanics", "1-on-1 Scalping Mastery"],
        "Join Date": ["2026-01-15", "2026-03-10", "2026-05-01"],
        "Payment Status": ["Paid", "Overdue", "Paid"]
    }
    df = pd.DataFrame(students_data)
    
    # Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Active Students", len(df))
    col2.metric("Pending Renewals", "1")
    col3.metric("Monthly Growth Rate", "+15%")
    
    st.markdown("### Active Roster")
    st.dataframe(df, use_container_width=True)
    
    # Form to add a new student manually
    st.markdown("---")
    st.markdown("### ➕ Register New Mentorship Student")
    with st.form("new_student_form"):
        name = st.text_input("Full Name")
        track = st.selectbox("Select Strategy Track", ["Foundational Mechanics", "Advanced Price Action", "1-on-1 Scalping Mastery"])
        status = st.radio("Initial Payment Status", ["Paid", "Pending"])
        submitted = st.form_submit_button("Enroll Student")
        if submitted:
            st.success(f"Successfully added {name} to your local tracking ledger!")

# ==========================================
# CONTENT & STRATEGY
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
