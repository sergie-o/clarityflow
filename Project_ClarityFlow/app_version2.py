"""
ClarityFlow - Custom Logo + Matching Blue-Orange Palette
Glassmorphism design with colors from logo
"""

from features.productivity_rhythm import PersonalProductivityRhythmTracker
from features.schedule_realism import ScheduleRealismScorer
from features.cognitive_load import CognitiveLoadDetector
from features.execution_drift import ExecutionDriftAnalyzer
from features.task_prioritization import TaskPrioritizer
from core.models import Task
import os
import sys
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

st.set_page_config(
    page_title="ClarityFlow",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# BLUE-ORANGE GRADIENT PALETTE FROM LOGO
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* BLUE-ORANGE ANIMATED GRADIENT BACKGROUND (from logo) */
    .stApp {
        background: linear-gradient(135deg, 
            #0ea5e9 0%,      /* Sky blue */
            #06b6d4 20%,     /* Cyan */
            #3b82f6 40%,     /* Blue */
            #f97316 60%,     /* Orange */
            #fb923c 80%,     /* Light orange */
            #fbbf24 100%);   /* Amber */
        background-size: 400% 400%;
        animation: gradient 20s ease infinite;
    }
    
    @keyframes gradient {
        0%, 100% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1600px;
    }
    
    /* LOGO BANNER WITH DARK BACKGROUND */
    .logo-banner {
        background: linear-gradient(135deg, 
            rgba(30, 41, 59, 0.98) 0%,     /* CHANGED: Dark slate */
            rgba(15, 23, 42, 0.95) 100%);  /* CHANGED: Darker slate */
        backdrop-filter: blur(30px) saturate(180%);
        -webkit-backdrop-filter: blur(30px) saturate(180%);
        border-radius: 28px;
        padding: 2.5rem 3rem;
        margin-bottom: 2.5rem;
        box-shadow: 
            0 25px 70px rgba(0,0,0,0.3),
            0 10px 40px rgba(59, 130, 246, 0.2),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 2px solid rgba(59, 130, 246, 0.3);  /* CHANGED: Blue border */
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2rem;
    }
    
    .logo-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(
            from 0deg,
            transparent,
            rgba(59, 130, 246, 0.15) 60deg,   /* CHANGED: More visible */
            transparent 120deg,
            transparent 240deg,
            rgba(249, 115, 22, 0.15) 300deg,  /* CHANGED: More visible */
            transparent 360deg
        );
        animation: rotateLogo 12s linear infinite;
    }
    
    @keyframes rotateLogo {
        from {transform: rotate(0deg);}
        to {transform: rotate(360deg);}
    }
    
    .logo-image {
        max-width: 280px;  /* CHANGED: was 500px */
        width: 100%;
        height: auto;
        display: block;
        filter: drop-shadow(0 8px 24px rgba(59, 130, 246, 0.4))
                drop-shadow(0 4px 12px rgba(249, 115, 22, 0.3));
        position: relative;
        z-index: 1;
        animation: float 4s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% {transform: translateY(0px);}
        50% {transform: translateY(-12px);}
    }
    
    .brand-tagline {
        color: rgba(255, 255, 255, 0.95);  /* CHANGED: White text */
        font-size: 1.3rem;
        font-weight: 600;
        margin: 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* GLASS FEATURE CARDS WITH BLUE-ORANGE ACCENTS */
    .feature-card {
        background: linear-gradient(135deg,
            rgba(255, 255, 255, 0.95) 0%,
            rgba(255, 255, 255, 0.85) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        padding: 1.75rem;
        border: 2px solid rgba(255,255,255,0.5);
        box-shadow: 
            0 8px 32px rgba(59, 130, 246, 0.12),
            0 4px 16px rgba(0,0,0,0.08),
            inset 0 1px 0 rgba(255,255,255,0.7);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, 
            #06b6d4 0%,    /* Cyan */
            #3b82f6 50%,   /* Blue */
            #f97316 100%); /* Orange */
        opacity: 0;
        transition: opacity 0.4s;
    }
    
    .feature-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(59, 130, 246, 0.2),
            0 8px 24px rgba(249, 115, 22, 0.1),
            inset 0 1px 0 rgba(255,255,255,0.9);
        border-color: rgba(59, 130, 246, 0.4);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-icon {
        font-size: 2.75rem;
        margin-bottom: 0.75rem;
        filter: drop-shadow(0 4px 8px rgba(59, 130, 246, 0.2));
    }
    
    .feature-title {
        color: #1e293b;
        font-size: 1.15rem;
        font-weight: 800;
        margin: 0.75rem 0;
    }
    
    .feature-value {
        font-size: 2.25rem;
        font-weight: 900;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #0ea5e9 0%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .feature-desc {
        color: #475569;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* METRICS WITH BLUE-ORANGE GRADIENT */
    [data-testid="stMetricValue"] {
        font-size: 2.25rem;
        font-weight: 900;
        background: linear-gradient(135deg, #0ea5e9 0%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        color: #1e293b !important;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.875rem;
        letter-spacing: 0.5px;
    }
    
    /* BUTTONS WITH BLUE-ORANGE GRADIENT */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 50%, #3b82f6 100%);
        color: white !important;
        border: none;
        border-radius: 14px;
        padding: 0.85rem 1.75rem;
        font-weight: 700;
        box-shadow: 
            0 6px 20px rgba(14, 165, 233, 0.4),
            0 0 20px rgba(59, 130, 246, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 
            0 12px 36px rgba(14, 165, 233, 0.5),
            0 0 30px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* PRIMARY BUTTON WITH ORANGE ACCENT */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #f97316 0%, #fb923c 50%, #fbbf24 100%);
        box-shadow: 
            0 6px 20px rgba(249, 115, 22, 0.4),
            0 0 20px rgba(251, 146, 60, 0.2);
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: 
            0 12px 36px rgba(249, 115, 22, 0.5),
            0 0 30px rgba(251, 146, 60, 0.3);
    }
    
    /* TABS WITH GRADIENT */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(12px);
        padding: 0.75rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.5);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 56px;
        background: transparent;
        border-radius: 12px;
        color: #1e293b;
        font-weight: 700;
        padding: 0 28px;
        transition: all 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(14, 165, 233, 0.1);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        color: white !important;
        box-shadow: 
            0 6px 20px rgba(14, 165, 233, 0.4),
            0 0 20px rgba(59, 130, 246, 0.3);
    }
    
    /* ALERTS WITH COLORED GLASS */
    div[data-baseweb="notification"] {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(12px);
        border-radius: 14px;
        color: #1e293b !important;
        border: 1px solid rgba(255,255,255,0.5);
    }
    
    div[data-baseweb="notification"][kind="success"] {
        border-left: 4px solid #10b981;
        background: linear-gradient(135deg, rgba(209, 250, 229, 0.95), rgba(167, 243, 208, 0.9));
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.2);
    }
    
    div[data-baseweb="notification"][kind="warning"] {
        border-left: 4px solid #f97316;
        background: linear-gradient(135deg, rgba(254, 243, 199, 0.95), rgba(253, 224, 71, 0.9));
        box-shadow: 0 4px 16px rgba(249, 115, 22, 0.2);
    }
    
    div[data-baseweb="notification"][kind="error"] {
        border-left: 4px solid #ef4444;
        background: linear-gradient(135deg, rgba(254, 226, 226, 0.95), rgba(252, 165, 165, 0.9));
        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.2);
    }
    
    div[data-baseweb="notification"][kind="info"] {
        border-left: 4px solid #0ea5e9;
        background: linear-gradient(135deg, rgba(224, 242, 254, 0.95), rgba(186, 230, 253, 0.9));
        box-shadow: 0 4px 16px rgba(14, 165, 233, 0.2);
    }
    
    /* EXPANDER */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(12px);
        border: 1.5px solid rgba(255,255,255,0.5);
        border-radius: 12px;
        font-weight: 700;
        color: #1e293b !important;
        transition: all 0.3s;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255,255,255,0.95);
        border-color: rgba(14, 165, 233, 0.5);
        transform: translateX(6px);
    }
    
    /* SIDEBAR GLASS */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,
            rgba(255, 255, 255, 0.98) 0%,
            rgba(255, 255, 255, 0.92) 100%);
        backdrop-filter: blur(30px);
        border-right: 2px solid rgba(255,255,255,0.5);
        box-shadow: 4px 0 30px rgba(14, 165, 233, 0.1);
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.8);
        color: #1e293b !important;
        border: 1.5px solid rgba(255,255,255,0.6);
        backdrop-filter: blur(8px);
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.95);
        border-color: rgba(14, 165, 233, 0.4);
    }
    
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        color: white !important;
        border: none;
    }
    
    /* INPUT FIELDS */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea textarea {
        background: rgba(255,255,255,0.9) !important;
        backdrop-filter: blur(12px);
        border: 1.5px solid rgba(255,255,255,0.5) !important;
        border-radius: 12px !important;
        color: #1e293b !important;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea textarea:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.15) !important;
    }
    
    /* DATAFRAME */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        border: 1.5px solid rgba(255,255,255,0.5);
        box-shadow: 0 8px 24px rgba(14, 165, 233, 0.12);
    }
    
    /* TEXT COLORS */
    h1, h2, h3, h4, h5, h6 {
        color: #1e293b !important;
        font-weight: 800 !important;
    }
    
    p, span, div, label {
        color: #1e293b !important;
    }
    
    .caption, [data-testid="stCaptionContainer"] {
        color: #475569 !important;
    }
    
    /* PRIORITY CARDS */
    .priority-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(12px);
        padding: 1.25rem;
        border-radius: 14px;
        margin: 0.75rem 0;
        box-shadow: 0 4px 16px rgba(14, 165, 233, 0.08);
        border: 1px solid rgba(255,255,255,0.5);
    }
    
    .priority-card strong {
        color: #1e293b !important;
        font-weight: 800;
    }
    
    /* SCROLLBAR */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.4);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #0ea5e9 0%, #f97316 100%);
        border-radius: 10px;
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #06b6d4 0%, #fb923c 100%);
    }
</style>
""", unsafe_allow_html=True)

# Session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "models" not in st.session_state:
    st.session_state.models = {}
if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"


def generate_sample_tasks(num_tasks=10):
    task_types = ['coding', 'meeting', 'admin', 'deep_work', 'communication']
    base_date = datetime.now()
    tasks = []
    for i in range(num_tasks):
        days_offset = np.random.randint(-3, 4)
        task_date = base_date + timedelta(days=days_offset)
        hour = np.random.randint(8, 18)
        task = Task(
            task_id=f"task_{i+1}",
            task_type=np.random.choice(task_types),
            estimated_minutes=np.random.choice([15, 30, 45, 60, 90, 120]),
            complexity_score=np.random.uniform(1, 5),
            time_of_day=task_date.replace(hour=hour, minute=0),
        )
        if days_offset < 0 or (days_offset == 0 and hour < datetime.now().hour):
            task.completed = True
            task.actual_minutes = int(
                task.estimated_minutes * np.random.uniform(0.9, 1.4))
            task.focus_level = np.random.randint(2, 6)
            task.interruption_count = np.random.randint(0, 5)
            task.context_switches = np.random.randint(0, 3)
        tasks.append(task)
    return tasks


def render_header():
    """Logo banner with custom image"""
    import base64
    from pathlib import Path

    # Load and encode the logo image
    logo_path = Path(
        "/Users/turfdiddy/Desktop/Bootcamp_ds:ml/Project_ClarityFlow/Project_ClarityFlow/clarityflowlogo.png")

    if logo_path.exists():
        with open(logo_path, "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()

        st.markdown(f"""
        <div class="logo-banner">
            <img src="data:image/png;base64,{logo_base64}" class="logo-image" alt="ClarityFlow Logo">
            <div class="brand-tagline">Your ML-Powered Personal Operating System</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback if image not found
        st.markdown("""
        <div class="logo-banner">
            <div style="position: relative; z-index: 1;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 4rem; font-weight: 800;
                     background: linear-gradient(135deg, #0ea5e9 0%, #f97316 100%);
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                     background-clip: text; margin-bottom: 1rem;">
                    🧠 ClarityFlow
                </div>
                <div class="brand-tagline">Your ML-Powered Personal Operating System</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("## 🎯 Navigation")
        st.markdown("---")
        for page in ["Dashboard", "Add Task", "Task History", "Analytics", "Settings"]:
            button_type = "primary" if st.session_state.active_page == page else "secondary"
            if st.button(page, key=f"nav_{page}", use_container_width=True, type=button_type):
                st.session_state.active_page = page
                st.rerun()
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        completed = len([t for t in st.session_state.tasks if t.completed])
        st.metric("Completed", completed)
        st.metric("Total", len(st.session_state.tasks))
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        if st.button("🎲 Generate Samples", use_container_width=True):
            st.session_state.tasks.extend(generate_sample_tasks(10))
            st.success("✓ Added 10 tasks!")
            st.rerun()


def render_dashboard():
    st.title("📊 Dashboard")
    st.caption("Your AI-powered productivity insights")
    st.markdown("---")

    today = datetime.now().date()
    today_tasks = [
        t for t in st.session_state.tasks if t.time_of_day.date() == today]
    incomplete_tasks = [t for t in st.session_state.tasks if not t.completed]

    if not st.session_state.tasks:
        st.info("👋 Welcome! Generate sample tasks to see ClarityFlow in action.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎲 Generate Sample Tasks", use_container_width=True, type="primary"):
                st.session_state.tasks.extend(generate_sample_tasks(20))
                st.success("✓ Generated 20 tasks!")
                st.rerun()
        with col2:
            if st.button("➕ Add Your Own Task", use_container_width=True):
                st.session_state.active_page = "Add Task"
                st.rerun()
        return

    st.subheader("🤖 AI-Powered Features")
    st.caption("Click any feature to explore")

    # Feature cards with all 6 features
    # [Feature cards code here - keeping dashboard functional]
    st.info("Feature cards displayed here with glassmorphism styling")


def render_add_task():
    st.title("➕ Add Task")
    st.markdown("---")
    with st.form("add_task"):
        col1, col2 = st.columns(2)
        with col1:
            task_type = st.selectbox(
                "Type", ["coding", "meeting", "admin", "deep_work", "communication"])
            estimated = st.number_input("Duration (min)", 5, 480, 30, 15)
        with col2:
            complexity = st.slider("Complexity", 1.0, 5.0, 3.0, 0.5)
            date = st.date_input("Date", datetime.now())
        time = st.time_input("Time", datetime.now().time())
        if st.form_submit_button("✅ Add Task", type="primary"):
            task = Task(f"task_{len(st.session_state.tasks)+1}", task_type,
                        estimated, complexity, datetime.combine(date, time))
            st.session_state.tasks.append(task)
            st.success("✅ Task added!")
            st.balloons()


def render_task_history():
    st.title("📋 Task History")
    st.markdown("---")
    st.info("Task history here")


def render_analytics():
    st.title("📈 Analytics")
    st.markdown("---")
    st.info("Analytics here")


def render_settings():
    st.title("⚙️ Settings")
    st.markdown("---")
    st.info("Settings here")


def main():
    render_header()
    render_sidebar()
    page = st.session_state.active_page
    if page == "Dashboard":
        render_dashboard()
    elif page == "Add Task":
        render_add_task()
    elif page == "Task History":
        render_task_history()
    elif page == "Analytics":
        render_analytics()
    elif page == "Settings":
        render_settings()


if __name__ == "__main__":
    main()
