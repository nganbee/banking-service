import streamlit as st
import requests
import json
import os

# ==========================================
# CONFIGURATION & PAGE SETUP
# ==========================================
st.set_page_config(
    page_title="Banking AI Agent",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CUSTOM CSS INJECTION (PREMIUM DESIGN)
# ==========================================
def inject_custom_css():
    st.markdown("""
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

        /* Global Font & Background */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: #f8fafc;
        }

        /* Chat Container Styling */
        [data-testid="stChatMessage"] {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: transform 0.2s ease;
        }
        
        [data-testid="stChatMessage"]:hover {
            transform: translateY(-2px);
            background-color: rgba(255, 255, 255, 0.08);
        }

        /* Avatar Styling */
        [data-testid="stChatMessageAvatarUser"] {
            background-color: #3b82f6;
        }
        [data-testid="stChatMessageAvatarAssistant"] {
            background-color: #8b5cf6;
        }

        /* Header Styling */
        .main-header {
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .main-header h1 {
            background: linear-gradient(to right, #60a5fa, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .main-header p {
            color: #94a3b8;
            font-size: 1.1rem;
        }

        /* Decision Badge */
        .decision-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 1rem;
            background: rgba(139, 92, 246, 0.2);
            color: #c084fc;
            border: 1px solid rgba(139, 92, 246, 0.3);
        }
        
        /* Input Area Styling */
        [data-testid="stChatInput"] {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0,0,0,0.1);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.2);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255,255,255,0.3);
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# STATE MANAGEMENT
# ==========================================
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI Banking Assistant. How can I help you today?", "decision": None, "trace": []}
        ]

# ==========================================
# API INTERACTION (STREAMING)
# ==========================================
def call_backend_stream(message: str, status_container):
    _base = os.getenv("API_BASE_URL", "http://localhost:8000")
    API_URL = f"{_base}/stream-agent"
    
    try:
        response = requests.post(
            API_URL,
            json={"message": message},
            stream=True,
            timeout=120
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    data_str = decoded_line[6:]
                    data = json.loads(data_str)
                    
                    if data.get("status") == "running":
                        status_container.update(label=f"Running: **{data['node']}**...", state="running")
                    
                    elif data.get("status") == "completed":
                        return data.get("response", "No response"), data.get("decision", "unknown"), data.get("trace", [])
                        
        return "**Error:** Stream ended unexpectedly.", "error", []
        
    except requests.exceptions.ConnectionError:
        return "**Error:** Could not connect to the Backend API. Make sure it is running on port 8000.", "error", []
    except Exception as e:
        return f"**Error:** {str(e)}", "error", []

# ==========================================
# MAIN APP LAYOUT
# ==========================================
def main():
    inject_custom_css()
    init_session_state()

    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🏦 Banking Agentic Workflow</h1>
            <p>Smart Customer Service Powered by LLM & gRPC</p>
        </div>
    """, unsafe_allow_html=True)

    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("trace"):
                with st.status("Agent Execution Nodes", state="complete"):
                    for step in msg["trace"]:
                        st.markdown(f"- {step}")
            
            st.markdown(msg["content"])
            
            # Display decision
            if msg.get("decision") and msg.get("decision") != "unknown":
                st.markdown(f'<div class="decision-badge">Route: {msg["decision"]}</div>', unsafe_allow_html=True)

    # Chat Input
    if prompt := st.chat_input("Type your message here... (e.g., 'I lost my credit card')"):
        
        # 1. Display User Message
        st.session_state.messages.append({"role": "user", "content": prompt, "decision": None, "trace": []})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Call API & Display Agent Message (Streaming)
        with st.chat_message("assistant"):
            # Initialize Status Spinner
            status_container = st.status("Starting Agentic Workflow...", expanded=True)
            
            # Run streaming function
            response_text, decision, trace = call_backend_stream(prompt, status_container)
            
            # After execution, update spinner label and show details
            if trace:
                status_container.update(label="Agent Execution Nodes", state="complete")
                for step in trace:
                    status_container.markdown(f"- {step}")
            else:
                status_container.update(label="Execution Error", state="error")
                        
            st.markdown(response_text)
            
            if decision and decision != "unknown":
                st.markdown(f'<div class="decision-badge">Route: {decision}</div>', unsafe_allow_html=True)
            
            # Save state
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_text, 
                "decision": decision,
                "trace": trace
            })

if __name__ == "__main__":
    main()
