"""
ClarityFlow - COMPLETE VERSION
✅ Compact logo banner
✅ All 6 feature cards
✅ Dark background
✅ Perfect sizing
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
import base64
from pathlib import Path
from streamlit_echarts import st_echarts 


APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

st.set_page_config(
    page_title="ClarityFlow",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===== LOAD LOGO =====


def load_logo():
    logo_path = Path(
        "/Users/turfdiddy/Desktop/Bootcamp_ds:ml/Project_ClarityFlow/Project_ClarityFlow/clarityflowlogo.png")
    try:
        if logo_path.exists():
            with open(logo_path, "rb") as img_file:
                logo_bytes = img_file.read()
                logo_base64 = base64.b64encode(logo_bytes).decode()
                return f"data:image/png;base64,{logo_base64}"
        return None
    except Exception as e:
        st.error(f"Error loading logo: {e}")
        return None


LOGO_DATA = load_logo()

# CSS WITH COMPACT LOGO BANNER
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * {font-family: 'Inter', sans-serif;}
    #MainMenu, footer, header {visibility: hidden;}
    
    /* ANIMATED BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, 
            #0ea5e9 0%, #06b6d4 20%, #3b82f6 40%,
            #f97316 60%, #fb923c 80%, #fbbf24 100%);
        background-size: 400% 400%;
        animation: gradient 20s ease infinite;
    }
    @keyframes gradient {
        0%, 100% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
    }
    
    .main .block-container {
        padding: 1.5rem 2.5rem;
        max-width: 1600px;
    }
    
    /* COMPACT LOGO BANNER - FIXED */
    .logo-banner {
    background: linear-gradient(135deg, 
        rgba(30, 41, 59, 0.98) 0%,
        rgba(15, 23, 42, 0.95) 100%);
    backdrop-filter: blur(30px);
    border-radius: 24px;
    padding: 2rem;              /* Reduced padding */
    margin-bottom: 1.5rem;
    max-width: 600px;           /* ← LIMIT WIDTH */
    margin-left: auto;          /* ← CENTER IT */
    margin-right: auto;         /* ← CENTER IT */
    box-shadow: 
        0 15px 40px rgba(0,0,0,0.3),
        0 5px 20px rgba(59, 130, 246, 0.2);
    border: 2px solid rgba(59, 130, 246, 0.3);
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;                     /* No gap - logo only */
}

.logo-image {
    max-width: 350px;           /* LARGER LOGO */
    width: auto;
    height: 160px;              /* TALLER */
    display: block;
    filter: drop-shadow(0 6px 16px rgba(59, 130, 246, 0.5));
    position: relative;
    z-index: 1;
}
    
    .brand-text {
        position: relative;
        z-index: 1;
        flex-grow: 1;
    }
    
    .brand-name {
        font-size: 2.25rem;  /* BIGGER TEXT */
        font-weight: 900;
        color: white;       /* WHITE - HIGH CONTRAST */
        margin: 0;
        line-height: 1.1;
        text-shadow: 0 2px 8px rgba(0,0,0,0.4);  /* Strong shadow */
    }
    
    .brand-tagline {
        color: rgba(255, 255, 255, 0.95);  /* BRIGHT WHITE */
        font-size: 1.1rem;  /* Bigger tagline */
        font-weight: 600;
        margin: 0.5rem 0 0 0;
        text-shadow: 0 1px 4px rgba(0,0,0,0.3);
    }
    
    /* FEATURE CARDS */
    .feature-card {
        background: linear-gradient(135deg,
            rgba(255, 255, 255, 0.95) 0%,
            rgba(255, 255, 255, 0.85) 100%);
        backdrop-filter: blur(20px);
        border-radius: 18px;
        padding: 1.5rem;
        border: 2px solid rgba(255,255,255,0.5);
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.12);
        transition: all 0.3s;
        cursor: pointer;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.2);
        border-color: rgba(59, 130, 246, 0.4);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        color: #1e293b;
        font-size: 1.05rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }
    
    .feature-value {
        font-size: 2rem;
        font-weight: 900;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #0ea5e9 0%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .feature-desc {
        color: #475569;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        box-shadow: 0 4px 16px rgba(14, 165, 233, 0.4);
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #f97316 0%, #fbbf24 100%);
        box-shadow: 0 4px 16px rgba(249, 115, 22, 0.4);
    }
    
    h1, h2, h3 {color: #1e293b !important; font-weight: 800 !important;}
    p, div, label {color: #1e293b !important;}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * {font-family: 'Inter', sans-serif;}
    
    /* Hide branding but KEEP sidebar toggle visible */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* DO NOT hide header - we need the sidebar toggle button */
    
    /* ANIMATED BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, 
            #0ea5e9 0%, #06b6d4 20%, #3b82f6 40%,
            #f97316 60%, #fb923c 80%, #fbbf24 100%);
        background-size: 400% 400%;
        animation: gradient 20s ease infinite;
    }
    
    @keyframes gradient {
        0%, 100% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
    }
    
    .main .block-container {
        padding: 1.5rem 2.5rem;
        max-width: 1600px;
    }
    
    /* COMPACT CENTERED LOGO BANNER */
    .logo-banner {
        background: linear-gradient(135deg, 
            rgba(30, 41, 59, 0.98) 0%,
            rgba(15, 23, 42, 0.95) 100%);
        backdrop-filter: blur(30px);
        border-radius: 24px;
        padding: 2rem;
        margin: 0 auto 1.5rem auto;
        max-width: 600px;
        min-height: 200px;
        box-shadow: 
            0 15px 40px rgba(0,0,0,0.3),
            0 5px 20px rgba(59, 130, 246, 0.2);
        border: 2px solid rgba(59, 130, 246, 0.3);
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .logo-image {
        max-width: 350px;
        width: auto;
        height: 160px;
        display: block;
        filter: drop-shadow(0 6px 16px rgba(59, 130, 246, 0.5));
        position: relative;
        z-index: 1;
    }
    
    /* FEATURE CARDS */
    .feature-card {
        background: linear-gradient(135deg,
            rgba(255, 255, 255, 0.95) 0%,
            rgba(255, 255, 255, 0.85) 100%);
        backdrop-filter: blur(20px);
        border-radius: 18px;
        padding: 1.5rem;
        border: 2px solid rgba(255,255,255,0.5);
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.12);
        transition: all 0.3s;
        cursor: pointer;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.2);
        border-color: rgba(59, 130, 246, 0.4);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        color: #1e293b;
        font-size: 1.05rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }
    
    .feature-value {
        font-size: 2rem;
        font-weight: 900;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #0ea5e9 0%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .feature-desc {
        color: #475569;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        box-shadow: 0 4px 16px rgba(14, 165, 233, 0.4);
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #f97316 0%, #fbbf24 100%);
        box-shadow: 0 4px 16px rgba(249, 115, 22, 0.4);
    }
    
    /* SIDEBAR - WHITE TEXT ON DARK */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,
            rgba(30, 41, 59, 0.98) 0%,
            rgba(15, 23, 42, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-right: 2px solid rgba(59, 130, 246, 0.3);
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.1);
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.2);
    }
    
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
        color: white !important;
        border: none;
    }
    
    /* TEXT COLORS */
    h1, h2, h3 {
        color: #1e293b !important;
        font-weight: 800 !important;
    }
    
    p, div, label {
        color: #1e293b !important;
    }
</style>
""", unsafe_allow_html=True) # ← This closes the main CSS block

# ===== ADD THE SIDEBAR CODE HERE =====
st.markdown("""
<style>
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if "tasks" not in st.session_state:
    st.session_state.tasks = [] 

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
        days_offset = np.random.randint(-7, 1)  # Last week of data
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
            task.actual_minutes = int(task.estimated_minutes * np.random.uniform(0.9, 1.4))
            task.focus_level = np.random.randint(2, 6)  # ← MAKE SURE THIS IS HERE
            task.interruption_count = np.random.randint(0, 5)
            task.context_switches = np.random.randint(0, 3)
        
        tasks.append(task)
    return tasks

def render_productivity_heatmap():
    """Productivity rhythm heatmap visualization"""
    st.subheader("🔥 Your Productivity Rhythm Heatmap")
    st.caption("Discover your peak performance times")
    
    # Get completed tasks with data
    completed = [t for t in st.session_state.tasks 
                 if t.completed and hasattr(t, 'focus_level') and t.focus_level]
    
    if len(completed) < 10:
        st.info(f"📊 Complete {10 - len(completed)} more tasks to unlock your rhythm heatmap!")
        return
    
    # Process data
    hours = list(range(8, 19))  # 8am to 6pm
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    
    # Calculate average focus by day and hour
    focus_data = {}
    for task in completed:
        day = task.time_of_day.strftime('%a')[:3]  # Mon, Tue, etc.
        hour = task.time_of_day.hour
        
        if day in days and 8 <= hour < 19:
            key = (days.index(day), hour - 8)
            if key not in focus_data:
                focus_data[key] = []
            focus_data[key].append(task.focus_level)
    
    # Create heatmap data: [day_index, hour_index, avg_focus]
    heatmap_data = []
    for d in range(len(days)):
        for h in range(len(hours)):
            key = (d, h)
            if key in focus_data:
                avg_focus = sum(focus_data[key]) / len(focus_data[key])
                heatmap_data.append([d, h, round(avg_focus, 1)])
            else:
                heatmap_data.append([d, h, 0])  # No data
    
    # ECharts configuration
    option = {
        "title": {
            "text": "Your Peak Performance Times",
            "left": "center",
            "textStyle": {
                "fontSize": 24,
                "fontWeight": "bold",
                "color": "#1e293b"
            }
        },
        "tooltip": {
            "position": "top",
            "formatter": "{b0} {b1}:00<br/>Focus: {c}/5"
        },
        "grid": {
            "height": "60%",
            "top": "20%",
            "left": "10%",
            "right": "10%"
        },
        "xAxis": {
            "type": "category",
            "data": days,
            "splitArea": {"show": True},
            "axisLabel": {"fontSize": 14, "fontWeight": "bold"}
        },
        "yAxis": {
            "type": "category",
            "data": [f"{h}:00" for h in hours],
            "splitArea": {"show": True},
            "axisLabel": {"fontSize": 12}
        },
        "visualMap": {
            "min": 0,
            "max": 5,
            "calculable": True,
            "orient": "horizontal",
            "left": "center",
            "bottom": "5%",
            "inRange": {
                "color": [
                    "#313695",  # Dark blue (low)
                    "#4575b4",
                    "#74add1", 
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",  # Yellow (medium)
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026"   # Dark red (high)
                ]
            },
            "text": ["High Focus", "Low Focus"],
            "textStyle": {"fontSize": 12, "fontWeight": "bold"}
        },
        "series": [{
            "name": "Focus Level",
            "type": "heatmap",
            "data": heatmap_data,
            "label": {
                "show": True,
                "fontSize": 11,
                "fontWeight": "bold"
            },
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                }
            }
        }]
    }
    
    # Render the chart
    st_echarts(options=option, height="550px")
    
    # Show insights
    if heatmap_data:
        # Find best time
        best_slot = max(heatmap_data, key=lambda x: x[2])
        if best_slot[2] > 0:
            best_day = days[best_slot[0]]
            best_hour = hours[best_slot[1]]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🏆 Peak Time", f"{best_day} {best_hour}:00")
            with col2:
                avg_focus = sum(d[2] for d in heatmap_data if d[2] > 0) / len([d for d in heatmap_data if d[2] > 0])
                st.metric("📊 Avg Focus", f"{avg_focus:.1f}/5")
            with col3:
                tasks_analyzed = len(completed)
                st.metric("📈 Tasks Analyzed", tasks_analyzed)

def render_3d_focus_surface():
    """3D surface showing focus by hour and complexity"""
    st.subheader("🎢 3D Focus Landscape")
    st.caption("Your focus level across time and task complexity")
    
    completed = [t for t in st.session_state.tasks 
                 if t.completed and hasattr(t, 'focus_level') and t.focus_level]
    
    if len(completed) < 20:
        st.info(f"📊 Complete {20 - len(completed)} more tasks to unlock 3D visualization!")
        return
    
    # Create 3D grid data
    hours = list(range(8, 19))  # 8am to 6pm
    complexity_levels = [1, 2, 3, 4, 5]
    
    # Calculate average focus for each hour x complexity combo
    grid_data = []
    for complexity in complexity_levels:
        row = []
        for hour in hours:
            matching_tasks = [
                t for t in completed 
                if t.time_of_day.hour == hour 
                and abs(t.complexity_score - complexity) < 0.8
            ]
            
            if matching_tasks:
                avg_focus = np.mean([t.focus_level for t in matching_tasks])
                row.append(round(avg_focus, 2))
            else:
                row.append(1.5)
        grid_data.append(row)
    
    # Format data for 3D surface
    surface_data = []
    for y, complexity in enumerate(complexity_levels):
        for x, hour in enumerate(hours):
            surface_data.append([x, y, grid_data[y][x]])
    
    option = {
        "backgroundColor": "rgba(255,255,255,0)",
        "title": {
            "text": "Your 3D Focus Landscape",
            "subtext": "Higher peaks = Better focus",
            "left": "center",
            "top": "5%",
            "textStyle": {"fontSize": 24, "fontWeight": "bold", "color": "#1e293b"}
        },
        "tooltip": {},
        "visualMap": {
            "show": True,
            "min": 0,
            "max": 5,
            "dimension": 2,
            "inRange": {
                "color": [
                    "#313695", "#4575b4", "#74add1", 
                    "#fee090", "#f46d43", "#d73027", "#a50026"
                ]
            },
            "text": ["High", "Low"],
            "calculable": True,
            "left": "right",
            "top": "center"
        },
        "xAxis3D": {
            "type": "category",
            "data": [f"{h}:00" for h in hours],
            "name": "Time",
            "nameTextStyle": {"fontSize": 14, "fontWeight": "bold"}
        },
        "yAxis3D": {
            "type": "category",
            "data": [f"L{c}" for c in complexity_levels],
            "name": "Complexity",
            "nameTextStyle": {"fontSize": 14, "fontWeight": "bold"}
        },
        "zAxis3D": {
            "type": "value",
            "name": "Focus",
            "max": 5,
            "nameTextStyle": {"fontSize": 14, "fontWeight": "bold"}
        },
        "grid3D": {
            "boxWidth": 200,
            "boxDepth": 80,
            "viewControl": {
                "autoRotate": True,
                "autoRotateSpeed": 10
            }
        },
        "series": [{
            "type": "surface",
            "data": surface_data
        }]
    }
    
    # CRITICAL: Include ECharts GL library
    st_echarts(
        options=option, 
        height="650px",
        key="3d_surface",
        renderer="canvas"
    )
    
    # Key insights
    st.markdown("### 🔍 Key Insights")
    col1, col2, col3 = st.columns(3)
    
    max_focus = 0
    peak_hour = 0
    peak_complexity = 0
    for y, complexity in enumerate(complexity_levels):
        for x, hour in enumerate(hours):
            if grid_data[y][x] > max_focus:
                max_focus = grid_data[y][x]
                peak_hour = hour
                peak_complexity = complexity
    
    with col1:
        st.metric("🏔️ Peak Focus", f"{max_focus:.1f}/5")
    with col2:
        st.metric("🕐 Best Time", f"{peak_hour}:00")
    with col3:
        st.metric("⚡ Optimal Complexity", f"Level {peak_complexity}")

def render_priority_matrix():
    """Eisenhower Matrix showing AI-prioritized tasks"""
    st.subheader("🎯 AI Priority Matrix")
    st.caption("Tasks organized by urgency and impact")
    
    incomplete = [t for t in st.session_state.tasks if not t.completed]
    
    if len(incomplete) < 3:
        st.info("📋 Add 3+ tasks to see the priority matrix!")
        return
    
    # Prioritize tasks using AI
    try:
        prioritized = TaskPrioritizer.prioritize_tasks(incomplete, current_energy=3)
    except Exception as e:
        st.error(f"Error prioritizing tasks: {e}")
        return
    
    if not prioritized:
        st.warning("No tasks to prioritize")
        return
    
    # Prepare data for scatter plot
    scatter_data = []
    
    for task_data in prioritized[:20]:  # Top 20 tasks
        task = task_data['task']
        
        # FIXED: Access factors correctly
        if 'factors' in task_data:
            factors = task_data['factors']
            urgency = factors.get('urgency', 50)
            impact = factors.get('impact', 50)
        else:
            # Fallback: calculate from task properties
            urgency = min(100, task.estimated_minutes / 2)  # Simple urgency estimate
            impact = task.complexity_score * 20  # Convert 1-5 to 0-100
        
        total_score = task_data.get('total_score', 50)
        
        scatter_data.append({
            "name": f"{task.task_type[:10]}",
            "value": [urgency, impact, total_score],
            "priority": task_data.get('priority_level', 'MEDIUM')
        })
    
    # Create the scatter plot
    option = {
        "title": {
            "text": "AI Priority Matrix",
            "subtext": "Eisenhower-style prioritization powered by ML",
            "left": "center",
            "textStyle": {"fontSize": 24, "fontWeight": "bold"}
        },
        "tooltip": {
            "trigger": "item"
        },
        "grid": {
            "left": "10%",
            "right": "10%",
            "bottom": "10%",
            "top": "20%",
            "containLabel": True
        },
        "xAxis": {
            "type": "value",
            "name": "Urgency →",
            "nameLocation": "middle",
            "nameGap": 30,
            "nameTextStyle": {"fontSize": 14, "fontWeight": "bold"},
            "min": 0,
            "max": 100,
            "splitLine": {"lineStyle": {"type": "dashed"}},
            "axisLine": {"lineStyle": {"width": 2}}
        },
        "yAxis": {
            "type": "value",
            "name": "↑ Impact",
            "nameLocation": "middle",
            "nameGap": 40,
            "nameTextStyle": {"fontSize": 14, "fontWeight": "bold"},
            "min": 0,
            "max": 100,
            "splitLine": {"lineStyle": {"type": "dashed"}},
            "axisLine": {"lineStyle": {"width": 2}}
        },
        "series": [{
            "type": "scatter",
            "data": scatter_data,
            "symbolSize": 20,
            "itemStyle": {"opacity": 0.8},
            "markLine": {
                "silent": True,
                "lineStyle": {
                    "color": "#999",
                    "width": 2,
                    "type": "solid"
                },
                "data": [
                    {"xAxis": 50},
                    {"yAxis": 50}
                ]
            }
        }]
    }
    
    st_echarts(options=option, height="550px")
    
    # Categorize into quadrants
    quadrants = {
        "urgent_important": [],
        "not_urgent_important": [],
        "urgent_not_important": [],
        "not_urgent_not_important": []
    }
    
    for i, task_data in enumerate(prioritized):
        # Use scatter_data if available, otherwise calculate
        if i < len(scatter_data):
            urgency = scatter_data[i]['value'][0]
            impact = scatter_data[i]['value'][1]
        else:
            urgency = 50
            impact = 50
        
        if urgency >= 50 and impact >= 50:
            quadrants['urgent_important'].append(task_data)
        elif urgency < 50 and impact >= 50:
            quadrants['not_urgent_important'].append(task_data)
        elif urgency >= 50 and impact < 50:
            quadrants['urgent_not_important'].append(task_data)
        else:
            quadrants['not_urgent_not_important'].append(task_data)
    
    # Show quadrant breakdown
    st.markdown("### 📊 Quadrant Breakdown")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("#### 🔥 Do First")
        st.metric("Tasks", len(quadrants['urgent_important']))
        st.caption("Urgent + Important")
    
    with col2:
        st.markdown("#### 📅 Schedule")
        st.metric("Tasks", len(quadrants['not_urgent_important']))
        st.caption("Not Urgent + Important")
    
    with col3:
        st.markdown("#### 🤝 Delegate")
        st.metric("Tasks", len(quadrants['urgent_not_important']))
        st.caption("Urgent + Not Important")
    
    with col4:
        st.markdown("#### 🗑️ Eliminate")
        st.metric("Tasks", len(quadrants['not_urgent_not_important']))
        st.caption("Neither")
    
    # Show top priority tasks
    st.markdown("### 🏆 Top 5 Priority Tasks")
    
    for i, task_data in enumerate(prioritized[:5], 1):
        task = task_data['task']
        score = task_data.get('total_score', 0)
        priority = task_data.get('priority_level', 'MEDIUM')
        
        # Color code by priority
        if priority == "CRITICAL":
            color = "#ef4444"
            icon = "🔴"
        elif priority == "HIGH":
            color = "#f97316"
            icon = "🟠"
        elif priority == "MEDIUM":
            color = "#f59e0b"
            icon = "🟡"
        else:
            color = "#10b981"
            icon = "🟢"
        
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 12px; 
                    border-left: 4px solid {color}; margin: 0.5rem 0;">
            <strong>{icon} #{i}: {task.task_type.title()}</strong> ({task.estimated_minutes} min)
            <br/>
            <small>Priority Score: {score:.0f}/100 | Level: {priority}</small>
        </div>
        """, unsafe_allow_html=True)

def render_header():
    """Compact logo banner"""
    if LOGO_DATA:
        # If logo image loaded successfully
        st.markdown(f"""
        <div class="logo-banner">
            <img src="{LOGO_DATA}" class="logo-image" alt="ClarityFlow">
        </div>
        """, unsafe_allow_html=True)
        # ↑ This parameter MUST be here to render HTML
    else:
        # Fallback if logo doesn't load
        st.markdown("""
        <div class="logo-banner">
            <div class="brand-text">
                <div class="brand-name">🧠 ClarityFlow</div>
                <div class="brand-tagline">Your ML-Powered Personal Operating System</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # ↑ This parameter MUST be here too


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
                st.success("✓ Generated!")
                st.rerun()
        with col2:
            if st.button("➕ Add Your Own", use_container_width=True):
                st.session_state.active_page = "Add Task"
                st.rerun()
        return

    st.subheader("🤖 AI-Powered Features")
    st.caption("Click any feature to explore")

    # ROW 1: Core Features
    col1, col2, col3 = st.columns(3)

    with col1:
        drift_analyzer = st.session_state.models.get("drift_analyzer")
        completed = [t for t in st.session_state.tasks if t.completed]

        if drift_analyzer and drift_analyzer.model:
            status = "✅ Active"
            status_color = "#10b981"
            desc = "Predicting duration"
        elif len(completed) >= 20:
            status = "Ready"
            status_color = "#f59e0b"
            desc = "Click to train"
        else:
            needed = 20 - len(completed)
            status = f"{needed} needed"
            status_color = "#64748b"
            desc = "Complete more tasks"

        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Execution Drift Analyzer</div>
            <div class="feature-value" style="color: {status_color};">{status}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("View Details", key="drift_btn", use_container_width=True):
            st.session_state.active_page = "Analytics"
            st.rerun()

    with col2:
        if today_tasks:
            load = CognitiveLoadDetector.calculate_load(today_tasks)
            load_score = load['score']

            if load_score > 75:
                load_status = "🔴 HIGH"
                load_color = "#ef4444"
            elif load_score > 50:
                load_status = "🟡 MODERATE"
                load_color = "#f59e0b"
            else:
                load_status = "🟢 HEALTHY"
                load_color = "#10b981"
        else:
            load_score = 0
            load_status = "N/A"
            load_color = "#64748b"

        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">Cognitive Load</div>
            <div class="feature-value" style="color: {load_color};">{load_score:.0f}/100</div>
            <div class="feature-desc">{load_status}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("View Breakdown", key="load_btn", use_container_width=True):
            st.session_state.show_load_detail = True
            st.rerun()

    with col3:
        if incomplete_tasks:
            priority_count = len(incomplete_tasks)
            priority_status = f"{priority_count} tasks"
            priority_color = "#667eea"
            desc = "Ready to prioritize"
        else:
            priority_status = "No tasks"
            priority_color = "#64748b"
            desc = "Add tasks first"

        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">AI Task Prioritization</div>
            <div class="feature-value" style="color: {priority_color};">{priority_status}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Prioritize Now", key="priority_btn", use_container_width=True, type="primary"):
            if incomplete_tasks:
                prioritized = TaskPrioritizer.prioritize_tasks(
                    incomplete_tasks, current_energy=3)
                st.session_state.prioritized_tasks = prioritized
                st.session_state.show_priority_detail = True
                st.rerun()
            else:
                st.warning("Add tasks first!")

    # ROW 2: Supporting Features
    col1, col2, col3 = st.columns(3)

    with col1:
        if today_tasks:
            drift_analyzer = st.session_state.models.get(
                "drift_analyzer", ExecutionDriftAnalyzer())
            realism = ScheduleRealismScorer.calculate_score(
                today_tasks, drift_analyzer)
            realism_score = realism['score']

            if realism_score >= 75:
                realism_status = "✅ Realistic"
                realism_color = "#10b981"
            elif realism_score >= 50:
                realism_status = "⚠️ Tight"
                realism_color = "#f59e0b"
            else:
                realism_status = "🔴 Overloaded"
                realism_color = "#ef4444"
        else:
            realism_score = 100
            realism_status = "N/A"
            realism_color = "#64748b"

        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Schedule Realism</div>
            <div class="feature-value" style="color: {realism_color};">{realism_score:.0f}/100</div>
            <div class="feature-desc">{realism_status}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("See Details", key="realism_btn", use_container_width=True):
            st.session_state.show_realism_detail = True
            st.rerun()

    with col2:
        completed_with_data = [
            t for t in st.session_state.tasks if t.completed and t.actual_minutes]

        if len(completed_with_data) >= 5:
            tracker = PersonalProductivityRhythmTracker()
            summary = tracker.summarize_rhythm(completed_with_data)
            peak_hour = summary['best_focus_hour']
            rhythm_status = f"Peak: {peak_hour}:00"
            rhythm_color = "#667eea"
            desc = "Your optimal time"
        else:
            rhythm_status = f"{len(completed_with_data)}/5"
            rhythm_color = "#64748b"
            desc = "Complete 5 tasks"

        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">⏰</div>
            <div class="feature-title">Productivity Rhythm</div>
            <div class="feature-value" style="color: {rhythm_color};">{rhythm_status}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("View Rhythm", key="rhythm_btn", use_container_width=True):
            st.session_state.active_page = "Analytics"
            st.rerun()

    with col3:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">➕</div>
            <div class="feature-title">Quick Actions</div>
            <div class="feature-value" style="color: #06b6d4;">Add Task</div>
            <div class="feature-desc">Create new task</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Add Task", key="add_task_btn", use_container_width=True, type="primary"):
            st.session_state.active_page = "Add Task"
            st.rerun()


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
    st.info("Task history here")


def render_analytics():
    st.title("📈 Analytics")
    st.caption("Productivity patterns")
    st.markdown("---")

    completed = [t for t in st.session_state.tasks if t.completed and t.actual_minutes]
    
    if len(completed) < 5:
        st.warning(f"Need 5 completed tasks for analytics. You have {len(completed)}.")
        return

    # EXISTING ANALYTICS
    tracker = PersonalProductivityRhythmTracker()
    summary = tracker.summarize_rhythm(completed)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Peak Hour", f"{summary['best_focus_hour']}:00")
    with col2:
        st.metric("Worst Hour", f"{summary['worst_drift_hour']}:00")

    st.markdown("---")
    
    # Existing focus chart
    fig = px.bar(summary["hourly_focus"], x="hour", y="focus_level", 
                 color="focus_level", color_continuous_scale="Viridis")
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ADD THE HEATMAP HERE ← NEW!
    render_productivity_heatmap()

    st.markdown("---")


     # 3D SURFACE - ADD THIS
    render_3d_focus_surface()
    
    st.markdown("---")
    
    # PRIORITY MATRIX - ADD THIS
    render_priority_matrix()


    st.title("📈 Analytics")
    st.info("Analytics here")


def render_settings():
    st.title("⚙️ Settings")
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
