"""
ClarityFlow - Ultra-Modern Manager Interface
Premium Design with Glassmorphism, Animations & Contemporary UI

Design Features:
- Glassmorphism effects
- Smooth animations & transitions
- 3D card effects
- Gradient overlays
- Modern iconography
- Neumorphism elements
- Floating action buttons
"""

from features.emotion_planner import EmotionAwarePlanner
from features.interruption_cost import InterruptionCostEstimator
from features.decision_fatigue import DecisionFatigueMonitor
from features.productivity_rhythm import PersonalProductivityRhythmTracker
from features.schedule_realism import ScheduleRealismScorer
from features.cognitive_load import CognitiveLoadDetector
from features.execution_drift import ExecutionDriftAnalyzer
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

# Add current directory to path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

# Import modules

# =========================================
# 🎨 ULTRA-MODERN STYLING
# =========================================

st.set_page_config(
    page_title="ClarityFlow",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Premium CSS with modern effects
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main container with glassmorphism */
    .main .block-container {
        padding: 2rem;
        max-width: 1400px;
    }
    
    /* Glass card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px 0 rgba(31, 38, 135, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    /* Hero header with animated gradient */
    .hero-header {
        background: linear-gradient(135deg, 
            rgba(102, 126, 234, 0.9) 0%,
            rgba(118, 75, 162, 0.9) 100%);
        backdrop-filter: blur(10px);
        padding: 3rem 2.5rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        box-shadow: 
            0 20px 60px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .hero-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 20px rgba(0,0,0,0.2);
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
    }
    
    .hero-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.25rem;
        margin: 1rem 0 0 0;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* Modern metric cards with 3D effect */
    .metric-card-modern {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1.75rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-modern::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.4s ease;
    }
    
    .metric-card-modern:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(31, 38, 135, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    .metric-card-modern:hover::before {
        transform: scaleX(1);
    }
    
    .metric-value-modern {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
        line-height: 1;
    }
    
    .metric-label-modern {
        font-size: 0.875rem;
        color: rgba(255, 255, 255, 0.8);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin: 0;
    }
    
    .metric-subtitle {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.7);
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
    
    /* Task cards with neumorphism */
    .task-card-ultra {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 4px 16px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .task-card-ultra:hover {
        transform: translateX(8px);
        background: rgba(255, 255, 255, 0.18);
        box-shadow: 
            0 8px 24px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    .task-card-urgent {
        border-left: 4px solid #ff6b6b;
        background: rgba(255, 107, 107, 0.15);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.7); }
        50% { box-shadow: 0 0 0 10px rgba(255, 107, 107, 0); }
    }
    
    /* Modern buttons with gradient */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.2);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:hover:before {
        left: 100%;
    }
    
    /* Status badges with glow */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1.25rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .status-badge:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    
    .status-excellent {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
    }
    
    .status-good {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(250, 112, 154, 0.4);
    }
    
    /* Alert boxes with modern design */
    .alert-modern {
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .alert-success {
        background: rgba(17, 153, 142, 0.15);
        border-color: rgba(17, 153, 142, 0.5);
        color: #ffffff;
    }
    
    .alert-warning {
        background: rgba(250, 112, 154, 0.15);
        border-color: rgba(250, 112, 154, 0.5);
        color: #ffffff;
    }
    
    .alert-danger {
        background: rgba(255, 107, 107, 0.15);
        border-color: rgba(255, 107, 107, 0.5);
        color: #ffffff;
    }
    
    .alert-info {
        background: rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.5);
        color: #ffffff;
    }
    
    /* Progress bar with gradient */
    .progress-container-modern {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    
    .progress-bar-modern {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        box-shadow: 0 0 10px rgba(56, 239, 125, 0.5);
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar-modern::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255,255,255,0.3), 
            transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Floating action button */
    .fab {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 1000;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .fab:hover {
        transform: scale(1.1) rotate(90deg);
        box-shadow: 0 12px 36px rgba(102, 126, 234, 0.7);
    }
    
    /* Insight panel with frosted glass */
    .insight-panel {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(25px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .insight-panel h3 {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 0 1.5rem 0;
    }
    
    /* Text styling */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        font-weight: 700;
    }
    
    p, span, div {
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Streamlit specific overrides */
    .stMetric {
        background: transparent;
    }
    
    .stMetric > div {
        background: transparent;
    }
    
    /* Input fields with glass effect */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stSlider > div > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: rgba(102, 126, 234, 0.8) !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.5rem;
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white !important;
        font-weight: 600;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Loading animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-spinner {
        border: 3px solid rgba(255, 255, 255, 0.1);
        border-top: 3px solid white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
</style>
""", unsafe_allow_html=True)

# =========================================
# 🔧 SESSION STATE
# =========================================

if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "models" not in st.session_state:
    st.session_state.models = {}
if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"
if "show_quick_add" not in st.session_state:
    st.session_state.show_quick_add = False
if "current_mood" not in st.session_state:
    st.session_state.current_mood = 3

# =========================================
# 🎯 UTILITY FUNCTIONS
# =========================================


def get_today_tasks() -> list:
    today = datetime.now().date()
    return [t for t in st.session_state.tasks if t.time_of_day.date() == today]


def get_status_badge(score: float, thresholds: tuple = (75, 50)) -> str:
    high, medium = thresholds
    if score >= high:
        return '<span class="status-badge status-excellent">✓ Excellent</span>'
    elif score >= medium:
        return '<span class="status-badge status-good">△ Good</span>'
    else:
        return '<span class="status-badge status-warning">! Attention</span>'

# =========================================
# 📱 MODERN HERO HEADER
# =========================================


def render_hero_header():
    hour = datetime.now().hour
    if hour < 12:
        greeting, emoji = "Good Morning", "🌅"
    elif hour < 18:
        greeting, emoji = "Good Afternoon", "☀️"
    else:
        greeting, emoji = "Good Evening", "🌙"

    st.markdown(f"""
    <div class="hero-header">
        <h1>{emoji} {greeting}</h1>
        <p>📅 {datetime.now().strftime('%A, %B %d, %Y')} • Make today count</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# 🎯 ULTRA-MODERN DASHBOARD
# =========================================


def render_dashboard():
    render_hero_header()

    # Quick action bar
    col1, col2, col3, col4, col5, col6 = st.columns([2.5, 1, 1, 1, 1, 1])

    with col1:
        st.markdown("### 🎯 Today's Focus")

    with col2:
        if st.button("➕ Quick Add", use_container_width=True, type="primary"):
            st.session_state.show_quick_add = True
            st.rerun()

    with col3:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.active_page = "Analytics"
            st.rerun()

    with col4:
        mood_emoji = ["😫", "😕", "😐", "🙂",
                      "😄"][st.session_state.current_mood - 1]
        if st.button(f"{mood_emoji} Mood", use_container_width=True):
            st.session_state.active_page = "Mood"
            st.rerun()

    with col5:
        if st.button("🎓 Insights", use_container_width=True):
            st.session_state.active_page = "Insights"
            st.rerun()

    with col6:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.active_page = "Settings"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Get today's data
    today_tasks = get_today_tasks()
    completed_today = [t for t in today_tasks if t.completed]
    incomplete_today = [t for t in today_tasks if not t.completed]

    # Metrics row with modern cards
    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        progress_pct = (len(completed_today) / len(today_tasks)
                        * 100) if today_tasks else 0
        st.markdown(f"""
        <div class="metric-card-modern">
            <p class="metric-label-modern">TODAY'S PROGRESS</p>
            <p class="metric-value-modern">{len(completed_today)}<span style="font-size: 1.5rem; opacity: 0.6;">/{len(today_tasks)}</span></p>
            <div class="progress-container-modern">
                <div class="progress-bar-modern" style="width: {progress_pct}%;"></div>
            </div>
            <p class="metric-subtitle">{progress_pct:.0f}% Complete</p>
        </div>
        """, unsafe_allow_html=True)

    with metric2:
        if today_tasks:
            load = CognitiveLoadDetector.calculate_load(today_tasks)
            load_score = load['score']
            load_emoji = "🔴" if load_score > 75 else "🟡" if load_score > 50 else "🟢"
            load_text = "HIGH" if load_score > 75 else "MODERATE" if load_score > 50 else "HEALTHY"
        else:
            load_score = 0
            load_emoji = "🟢"
            load_text = "HEALTHY"

        st.markdown(f"""
        <div class="metric-card-modern">
            <p class="metric-label-modern">COGNITIVE LOAD</p>
            <p class="metric-value-modern">{load_score:.0f}<span style="font-size: 1rem; opacity: 0.6;">/100</span></p>
            <p class="metric-subtitle">{load_emoji} {load_text}</p>
        </div>
        """, unsafe_allow_html=True)

    with metric3:
        drift_analyzer = st.session_state.models.get("drift_analyzer")
        if drift_analyzer and drift_analyzer.model:
            model_icon = "🟢"
            model_text = "ACTIVE"
            model_sub = "AI Learning"
        else:
            completed_count = len(
                [t for t in st.session_state.tasks if t.completed])
            needed = max(0, 20 - completed_count)
            model_icon = "🟡" if needed > 0 else "🟢"
            model_text = f"{needed}"
            model_sub = "Tasks to Train" if needed > 0 else "Ready!"

        st.markdown(f"""
        <div class="metric-card-modern">
            <p class="metric-label-modern">AI MODEL</p>
            <p class="metric-value-modern">{model_icon} {model_text}</p>
            <p class="metric-subtitle">{model_sub}</p>
        </div>
        """, unsafe_allow_html=True)

    with metric4:
        if today_tasks:
            drift_analyzer = st.session_state.models.get(
                "drift_analyzer", ExecutionDriftAnalyzer())
            realism = ScheduleRealismScorer.calculate_score(
                today_tasks, drift_analyzer)
            realism_score = realism['score']
            realism_emoji = "🟢" if realism_score > 75 else "🟡" if realism_score > 50 else "🔴"
            realism_text = "REALISTIC" if realism_score > 75 else "MODERATE" if realism_score > 50 else "RISKY"
        else:
            realism_score = 100
            realism_emoji = "🟢"
            realism_text = "EXCELLENT"

        st.markdown(f"""
        <div class="metric-card-modern">
            <p class="metric-label-modern">SCHEDULE REALISM</p>
            <p class="metric-value-modern">{realism_score:.0f}<span style="font-size: 1rem; opacity: 0.6;">/100</span></p>
            <p class="metric-subtitle">{realism_emoji} {realism_text}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Main content area
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Today's Tasks")

        if not incomplete_today:
            st.markdown("""
            <div class="alert-modern alert-success">
                <strong style="font-size: 1.25rem;">🎉 All Clear!</strong><br>
                You've completed everything for today. Time to relax or plan ahead!
            </div>
            """, unsafe_allow_html=True)
        else:
            # Urgent tasks
            now = datetime.now()
            urgent = [t for t in incomplete_today if (
                t.time_of_day - now).total_seconds() < 3600]
            later = [t for t in incomplete_today if t not in urgent]

            if urgent:
                st.markdown("**🔥 Urgent (< 1 hour)**")
                for task in sorted(urgent, key=lambda t: t.time_of_day):
                    render_modern_task_card(task, urgent=True)

            if later:
                st.markdown("**📅 Scheduled**")
                for task in sorted(later, key=lambda t: t.time_of_day):
                    render_modern_task_card(task)

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="insight-panel">', unsafe_allow_html=True)
        st.markdown("### 💡 Smart Insights")

        if today_tasks:
            load = CognitiveLoadDetector.calculate_load(today_tasks)

            if load['score'] > 75:
                st.markdown("""
                <div class="alert-modern alert-danger">
                    <strong>⚠️ Overload Warning</strong><br>
                    Your cognitive load is critically high. Consider:
                    <ul style="margin: 0.75rem 0 0 1rem; padding: 0;">
                        <li>Postpone 2-3 non-urgent tasks</li>
                        <li>Delegate if possible</li>
                        <li>Block all interruptions</li>
                        <li>Take strategic breaks</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            elif load['score'] > 50:
                st.markdown("""
                <div class="alert-modern alert-warning">
                    <strong>△ Capacity Alert</strong><br>
                    You're near your limit. Avoid adding more tasks and stay focused on priorities.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert-modern alert-success">
                    <strong>✓ Optimal Load</strong><br>
                    Perfect balance! You have room for unexpected work while maintaining productivity.
                </div>
                """, unsafe_allow_html=True)

            # Load breakdown mini chart
            st.markdown("<br>", unsafe_allow_html=True)
            components_df = pd.DataFrame([load['components']]).T
            components_df.columns = ['Score']
            components_df = components_df.reset_index()
            components_df.columns = ['Factor', 'Score']

            fig = go.Figure(go.Bar(
                x=components_df['Score'],
                y=components_df['Factor'],
                orientation='h',
                marker=dict(
                    color=components_df['Score'],
                    colorscale='RdYlGn_r',
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=components_df['Score'].round(0).astype(int),
                textposition='inside',
                textfont=dict(color='white', size=12, family='Inter')
            ))

            fig.update_layout(
                height=200,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                xaxis=dict(showgrid=False, showticklabels=False,
                           range=[0, 100]),
                yaxis=dict(showgrid=False, tickfont=dict(
                    color='white', size=11)),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Inter')
            )

            st.plotly_chart(fig, use_container_width=True)

            # AI Predictions
            drift_analyzer = st.session_state.models.get("drift_analyzer")
            if drift_analyzer and drift_analyzer.model and incomplete_today:
                st.markdown("<br>**🤖 AI Duration Estimates**",
                            unsafe_allow_html=True)
                for task in incomplete_today[:3]:
                    pred = drift_analyzer.predict(task)
                    diff = pred['ai_prediction'] - pred['user_estimate']
                    if abs(diff) > 5:
                        color = "#ff6b6b" if diff > 0 else "#51cf66"
                        icon = "⚠️" if diff > 0 else "✓"
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.08); padding: 1rem; border-radius: 12px; margin: 0.5rem 0; border-left: 3px solid {color};">
                            <strong style="font-size: 0.9rem;">{task.task_type.title()}</strong><br>
                            <span style="font-size: 0.8rem; opacity: 0.9;">
                                {pred['user_estimate']:.0f}m → {pred['ai_prediction']:.0f}m
                                <strong style="color: {color};"> {icon} {diff:+.0f}m</strong>
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


def render_modern_task_card(task: Task, urgent: bool = False):
    time_str = task.time_of_day.strftime("%I:%M %p")
    drift_analyzer = st.session_state.models.get("drift_analyzer")
    ai_prediction = None

    if drift_analyzer and drift_analyzer.model:
        pred = drift_analyzer.predict(task)
        ai_prediction = pred['ai_prediction']

    card_class = "task-card-urgent" if urgent else ""

    col1, col2, col3 = st.columns([3, 2, 1])

    with col1:
        st.markdown(f"**{task.task_type.title()}**")
        if ai_prediction:
            diff = ai_prediction - task.estimated_minutes
            if abs(diff) > 5:
                st.caption(
                    f"⏱️ {task.estimated_minutes:.0f}m → 🤖 {ai_prediction:.0f}m ({diff:+.0f}m)")
            else:
                st.caption(f"⏱️ {task.estimated_minutes:.0f}m • {time_str}")
        else:
            st.caption(f"⏱️ {task.estimated_minutes:.0f}m • {time_str}")

    with col2:
        stars = "⭐" * int(task.complexity_score)
        st.caption(f"{stars}")

    with col3:
        if st.button("✓", key=f"complete_{task.task_id}", use_container_width=True):
            st.session_state.active_task = task
            st.session_state.active_page = "Complete"
            st.rerun()

# =========================================
# ➕ QUICK ADD MODAL
# =========================================


def render_quick_add():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### ➕ Quick Add Task")

    with st.form("quick_add"):
        col1, col2 = st.columns(2)

        with col1:
            task_type = st.selectbox(
                "Type", ["deep_work", "meeting", "coding", "admin", "communication"])
            estimated = st.number_input("Duration (min)", 5, 480, 60, 15)

        with col2:
            time = st.time_input("Time", datetime.now().time())
            complexity = st.slider("Complexity", 1.0, 5.0, 3.0, 0.5)

        col_submit, col_cancel = st.columns(2)

        with col_submit:
            submitted = st.form_submit_button(
                "Add Task", use_container_width=True, type="primary")
        with col_cancel:
            cancelled = st.form_submit_button(
                "Cancel", use_container_width=True)

        if submitted:
            dt = datetime.combine(datetime.now().date(), time)
            task = Task(
                task_id=f"task_{len(st.session_state.tasks)+1}_{datetime.now().timestamp()}",
                task_type=task_type,
                estimated_minutes=estimated,
                complexity_score=complexity,
                time_of_day=dt,
            )
            st.session_state.tasks.append(task)
            st.session_state.show_quick_add = False
            st.success("✓ Task added!")
            st.rerun()

        if cancelled:
            st.session_state.show_quick_add = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# ✅ COMPLETE TASK
# =========================================


def render_complete_task():
    task = st.session_state.get("active_task")
    if not task:
        st.session_state.active_page = "Dashboard"
        st.rerun()
        return

    render_hero_header()

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### ✅ Complete Task")
    st.markdown(
        f"**{task.task_type.title()}** • {task.time_of_day.strftime('%I:%M %p')}")

    with st.form("complete_form"):
        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            actual_minutes = st.number_input(
                "Actual duration (min)", 1, 600, int(task.estimated_minutes))
            focus_level = st.select_slider(
                "Focus level",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: [
                    "😫 Distracted", "😕 Low", "😐 OK", "🙂 Good", "😄 Excellent"][x-1]
            )

        with col2:
            interruptions = st.number_input("Interruptions", 0, 50, 0)
            context_switches = st.number_input("Context switches", 0, 20, 0)

        col_submit, col_back = st.columns(2)

        with col_submit:
            submitted = st.form_submit_button(
                "✓ Complete", use_container_width=True, type="primary")
        with col_back:
            back = st.form_submit_button("← Back", use_container_width=True)

        if submitted:
            task.actual_minutes = actual_minutes
            task.focus_level = focus_level
            task.interruption_count = interruptions
            task.context_switches = context_switches
            task.completed = True

            # Retrain if ready
            completed_tasks = [
                t for t in st.session_state.tasks if t.completed]
            if len(completed_tasks) >= 20:
                drift_analyzer = st.session_state.models.get(
                    "drift_analyzer", ExecutionDriftAnalyzer())
                result = drift_analyzer.train(st.session_state.tasks)
                if result["status"] == "success":
                    st.session_state.models["drift_analyzer"] = drift_analyzer

            st.session_state.active_page = "Dashboard"
            st.balloons()
            st.rerun()

        if back:
            st.session_state.active_page = "Dashboard"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# 📊 ANALYTICS
# =========================================


def render_analytics():
    render_hero_header()

    if st.button("← Dashboard"):
        st.session_state.active_page = "Dashboard"
        st.rerun()

    completed = [
        t for t in st.session_state.tasks if t.completed and t.actual_minutes]

    if len(completed) < 5:
        st.markdown("""
        <div class="alert-modern alert-warning">
            <strong>📊 Not Enough Data</strong><br>
            Complete at least 5 tasks to see analytics. You're building your productivity intelligence!
        </div>
                    
        """, unsafe_allow_html=True)
        return

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Performance Analytics")

    # Summary metrics
    total_time = sum(t.actual_minutes for t in completed)
    avg_drift = np.mean(
        [t.actual_minutes / t.estimated_minutes for t in completed])
    avg_focus = np.mean([t.focus_level for t in completed])

    met1, met2, met3, met4 = st.columns(4)

    with met1:
        st.markdown(f"""
        <div class="metric-card-modern">
            <p class="metric-label-modern">TIME TRACKED</p>
            <p class="metric-value-modern">{total_time/60:.1f}h</p>
        </div>
        """, unsafe_allow_html=True)

    with met2:
        drift_pct = (avg_drift - 1) * 100
        st.markdown(f"""
        <div class="metric-card-modern">
            <p class="metric-label-modern">AVG DRIFT</p>
            <p class="metric-value-modern">{drift_pct:+.0f}%</p>
        </div>
        """, unsafe_allow_html=True)

    with met3:
        st.markdown(f"""
        <div class="metric-card-modern">
            <p class="metric-label-modern">AVG FOCUS</p>
            <p class="metric-value-modern">{avg_focus:.1f}/5</p>
        </div>
        """, unsafe_allow_html=True)

    with met4:
        st.markdown(f"""
        <div class="metric-card-modern">
            <p class="metric-label-modern">COMPLETED</p>
            <p class="metric-value-modern">{len(completed)}</p>
        </div>
        """, unsafe_allow_html=True)

    # Rhythm analysis
    tracker = PersonalProductivityRhythmTracker()
    rhythm = tracker.summarize_rhythm(completed)

    if rhythm:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🌟 Peak Performance")
            st.success(
                f"**{rhythm['best_focus_hour']}:00** (Focus: {rhythm['best_focus_value']:.1f}/5)")

            fig1 = px.bar(
                rhythm['hourly_focus'],
                x='hour',
                y='focus_level',
                title="Focus by Hour",
                color='focus_level',
                color_continuous_scale='Viridis'
            )
            fig1.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.markdown("#### ⚠️ Accuracy Pattern")
            st.error(
                f"**{rhythm['worst_drift_hour']}:00** (Drift: {rhythm['worst_drift_value']:+.0f}%)")

            fig2 = px.line(
                rhythm['hourly_drift'],
                x='hour',
                y='drift',
                title="Drift by Hour",
                markers=True
            )
            fig2.add_hline(y=0, line_dash="dash", line_color="white")
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# ⚙️ SETTINGS
# =========================================


def render_settings():
    render_hero_header()

    if st.button("← Dashboard"):
        st.session_state.active_page = "Dashboard"
        st.rerun()

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Settings")

    tab1, tab2, tab3 = st.tabs(["🤖 AI Model", "💾 Data", "🎲 Testing"])

    with tab1:
        completed = [t for t in st.session_state.tasks if t.completed]
        drift_analyzer = st.session_state.models.get("drift_analyzer")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Completed Tasks", len(completed))

            if len(completed) >= 20:
                if st.button("🔄 Train Model", use_container_width=True, type="primary"):
                    with st.spinner("Training..."):
                        analyzer = ExecutionDriftAnalyzer()
                        result = analyzer.train(st.session_state.tasks)
                        if result["status"] == "success":
                            st.session_state.models["drift_analyzer"] = analyzer
                            st.success(f"✓ Trained! MAE: {result['mae']:.3f}")
                            st.balloons()
            else:
                needed = 20 - len(completed)
                st.warning(f"Need {needed} more tasks")

        with col2:
            if drift_analyzer and drift_analyzer.model:
                st.success("🟢 Model Active")
            else:
                st.error("🔴 Not Trained")

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📥 Export", use_container_width=True):
                data = {
                    'tasks': [t.to_dict() for t in st.session_state.tasks],
                    'export_date': datetime.now().isoformat()
                }
                st.download_button(
                    "Download",
                    data=json.dumps(data, indent=2, default=str),
                    file_name=f"clarityflow_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )

        with col2:
            if st.button("🗑️ Clear All", use_container_width=True):
                if st.checkbox("Confirm"):
                    st.session_state.tasks = []
                    st.session_state.models = {}
                    st.success("Cleared!")
                    st.rerun()

    with tab3:
        if st.button("🎲 Generate 30 Sample Tasks"):
            import random
            task_types = ["coding", "meeting",
                          "admin", "deep_work", "communication"]
            base_date = datetime.now() - timedelta(days=30)

            for i in range(30):
                days_ago = random.randint(0, 30)
                task_date = base_date + timedelta(days=days_ago)
                task_type = random.choice(task_types)
                estimated = random.choice([15, 30, 45, 60, 90, 120])
                drift_factor = random.uniform(0.9, 1.4)
                actual = int(estimated * drift_factor)

                task = Task(
                    task_id=f"sample_{i}",
                    task_type=task_type,
                    estimated_minutes=estimated,
                    complexity_score=random.uniform(1, 5),
                    time_of_day=task_date.replace(hour=random.randint(8, 18)),
                    actual_minutes=actual,
                    interruption_count=random.randint(0, 5),
                    context_switches=random.randint(0, 3),
                    focus_level=random.randint(2, 5),
                    completed=True
                )
                st.session_state.tasks.append(task)

            st.success("✓ Generated!")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# 🎯 ROUTER
# =========================================


def main():
    if st.session_state.show_quick_add:
        render_quick_add()
        return

    page = st.session_state.active_page

    if page == "Dashboard":
        render_dashboard()
    elif page == "Complete":
        render_complete_task()
    elif page == "Analytics":
        render_analytics()
    elif page == "Settings":
        render_settings()


if __name__ == "__main__":
    main()
