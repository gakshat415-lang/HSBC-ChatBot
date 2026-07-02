import streamlit as st
import datetime
import os
import sys

# Ensure correct encodings and path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ["PYTHONIOENCODING"] = "utf-8"

# Mock xxhash for Windows
import hashlib
class mock_xxhash:
    class xxh3_128:
        def __init__(self, data): self.data = data
        def digest(self): return hashlib.md5(self.data).digest()
sys.modules['xxhash'] = mock_xxhash

import uuid
from src.guardrails import check_guardrails
from src.chain import ask

def get_scrape_date():
    return "2026-07-02"

# ─── Page Config ──────────────────────────────────────────
st.set_page_config(
    page_title="HSBC Fund Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS based on Stitch DESIGN.md ─────────────────
st.markdown("""
<style>
/* Import Inter font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, .stApp, p, span, h1, h2, h3, h4, h5, h6, div[data-testid="stMarkdownContainer"] {
    font-family: 'Inter', sans-serif;
}

/* Sidebar Styling (Deep Navy) */
[data-testid="stSidebar"] {
    background-color: #0A1628 !important; 
    border-right: 1px solid #1A1A2E;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Main Area Background */
.stApp {
    background-color: #FFFFFF; 
}

/* Primary Header */
h1 {
    color: #1A1A2E !important;
    font-weight: 700 !important;
}

/* Warning Banner / Disclaimer */
.stAlert {
    background-color: #FFF3CD !important;
    color: #856404 !important;
    border-radius: 8px !important;
    border: 1px solid #FFEeba !important;
}

/* Example Question Buttons */
div.stButton > button {
    background-color: #FFFFFF !important;
    color: #DB0011 !important;
    border: 1px solid #DB0011 !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease-in-out;
}
div.stButton > button:hover {
    background-color: #DB0011 !important;
    color: #FFFFFF !important;
    border-color: #AF000D !important;
}

/* "New Chat" Sidebar Button (isolated in a column) */
[data-testid="stSidebar"] [data-testid="column"] div.stButton > button {
    background-color: transparent !important;
    color: #FFFFFF !important;
    border: 1px solid #4A556A !important;
    justify-content: center !important;
}
[data-testid="stSidebar"] [data-testid="column"] div.stButton > button:hover {
    background-color: rgba(219, 0, 17, 0.2) !important;
    border: 1px solid #DB0011 !important;
}

/* History Buttons */
[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    border-left: 3px solid #DB0011 !important;
    background-color: rgba(255,255,255,0.05) !important;
    border-radius: 0 4px 4px 0 !important;
    color: #FFFFFF !important;
    border-top: none !important;
    border-right: none !important;
    border-bottom: none !important;
    padding: 8px 11px !important;
}
[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
    background-color: transparent !important;
    color: #BBC7DF !important;
    border: none !important;
    padding: 8px 11px !important;
}
/* Force left alignment on history button text */
[data-testid="stSidebar"] div.stButton > button[kind="primary"] div[data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] div.stButton > button[kind="secondary"] div[data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] div.stButton > button[kind="primary"] p,
[data-testid="stSidebar"] div.stButton > button[kind="secondary"] p {
    text-align: left !important;
    width: 100% !important;
}

/* Chat Input Styling */
[data-testid="stChatInput"] {
    border-radius: 8px !important;
    border: 1px solid #E2E0FC !important;
}
[data-testid="stChatInput"]:focus-within {
    border: 1px solid #DB0011 !important;
    box-shadow: 0px 4px 12px rgba(219, 0, 17, 0.1) !important;
}

/* User Message Bubble */
[data-testid="chatAvatarIcon-user"] {
    background-color: #DB0011 !important;
}

/* Assistant Message Bubble (Light Gray) */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background-color: #F0F0F5 !important;
    border-radius: 12px !important;
    color: #1A1A2E !important;
    padding: 1rem !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) p {
    color: #1A1A2E !important;
}

/* Assistant Avatar */
[data-testid="chatAvatarIcon-assistant"] {
    background-color: #1A1A2E !important; 
}
</style>
""", unsafe_allow_html=True)

# ─── Session Management ───
if "sessions" not in st.session_state:
    st.session_state.sessions = []
    st.session_state.current_session_id = str(uuid.uuid4())
    st.session_state.sessions.append({"id": st.session_state.current_session_id, "title": "New Chat", "messages": []})
    st.session_state.messages = []

def save_current_session():
    for s in st.session_state.sessions:
        if s["id"] == st.session_state.current_session_id:
            s["messages"] = st.session_state.messages.copy()
            break

def switch_session(session_id):
    save_current_session()
    st.session_state.current_session_id = session_id
    for s in st.session_state.sessions:
        if s["id"] == session_id:
            st.session_state.messages = s["messages"].copy()
            break

def create_new_chat():
    save_current_session()
    new_id = str(uuid.uuid4())
    st.session_state.current_session_id = new_id
    st.session_state.sessions.append({"id": new_id, "title": "New Chat", "messages": []})
    st.session_state.messages = []

# ─── Sidebar (1:3 split is roughly handled by wide layout + sidebar) ───
with st.sidebar:
    st.markdown("<h2 style='font-size: 18px; font-weight: 700; margin-bottom: 20px;'>🏦 Fund Assistant</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 0.01])
    with col1:
        if st.button("➕ New Chat", use_container_width=True):
            create_new_chat()
            st.rerun()
    
    st.markdown("<hr style='border-color: #4A556A;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 11px; text-transform: uppercase; font-weight: 600; color: #8E8E93 !important;'>Today</p>", unsafe_allow_html=True)
    
    # Render functional history
    for s in reversed(st.session_state.sessions):
        is_active = (s["id"] == st.session_state.current_session_id)
        btn_type = "primary" if is_active else "secondary"
        if st.button(s["title"], key=f"session_{s['id']}", type=btn_type, use_container_width=True):
            switch_session(s["id"])
            st.rerun()
    
    st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #4A556A;'>", unsafe_allow_html=True)
    st.markdown("👤 Guest User")

# ─── Main Area (75%) ───

st.warning("⚠️ **Facts-only assistant. This is not investment advice. For guidance, visit amfiindia.com**")
st.title("Welcome to HSBC Fund Assistant")

# Welcome Screen (Empty State)
if len(st.session_state.messages) == 0:
    st.markdown("I can answer factual questions about HSBC mutual fund schemes on Groww. Ask me about expense ratios, exit loads, SIP amounts, risk levels, and more.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    examples = [
        "What is the expense ratio of HSBC Midcap Fund?",
        "What is the exit load for HSBC Small Cap Fund?",
        "What is the minimum SIP for HSBC ELSS Fund?"
    ]
    for i, example in enumerate(examples):
        if cols[i].button(example, key=f"example_{i}"):
            st.session_state.pending_query = example

# ─── Render Chat History ───
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ─── Handle User Input ───
user_input = st.chat_input("Ask a question about HSBC mutual funds...")

if "pending_query" in st.session_state:
    user_input = st.session_state.pending_query
    del st.session_state.pending_query

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Update session title if this is the first message
    if len(st.session_state.messages) == 1:
        new_title = user_input[:20] + "..." if len(user_input) > 20 else user_input
        for s in st.session_state.sessions:
            if s["id"] == st.session_state.current_session_id:
                s["title"] = new_title
                break

    # Process via Guardrails
    scrape_date = get_scrape_date()
    guardrail_result = check_guardrails(user_input, scrape_date)

    if not guardrail_result["allowed"]:
        response = f"**[BLOCKED - {guardrail_result['reason'].upper()}]**\n\n{guardrail_result['response']}"
    else:
        with st.spinner("Looking up fund information..."):
            try:
                response = ask(user_input)
            except Exception as e:
                response = f"An error occurred: {e}"

    # Display assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
        
    save_current_session()
    st.rerun()
