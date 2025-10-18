try:
    import streamlit as st  # type: ignore
except ImportError:
    import sys
    sys.exit("Missing dependency: 'streamlit'. Install it with: pip install streamlit and then re-run this app.")
import os
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="ChatNova AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.api_keys = {
        'openai': '',
        'anthropic': '',
        'gemini': ''
    }
    st.session_state.selected_provider = 'openai'
    st.session_state.selected_model = 'gpt-5'
    st.session_state.chat_threads = {}
    st.session_state.current_thread = None
    st.session_state.dark_mode = True
    st.session_state.memory_enabled = True

# Custom CSS for cyber/techy branding
st.markdown("""
<style>
    /* Cyber background with animated grid */
    .main {
        background: linear-gradient(to bottom, #0a0a1a 0%, #16213e 100%);
        position: relative;
    }
    
    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 191, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 191, 255, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
        animation: gridMove 20s linear infinite;
    }
    
    @keyframes gridMove {
        0% { transform: translateY(0); }
        100% { transform: translateY(50px); }
    }
    
    .main-header {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.8) 0%, rgba(22, 33, 62, 0.8) 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 2px solid rgba(0, 191, 255, 0.3);
        box-shadow: 
            0 0 40px rgba(0, 191, 255, 0.2),
            inset 0 0 40px rgba(0, 191, 255, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 191, 255, 0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
        filter: drop-shadow(0 0 20px rgba(0, 191, 255, 0.6));
        animation: logoFloat 3s ease-in-out infinite;
    }
    
    @keyframes logoFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .app-title {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00BFFF 0%, #0099CC 50%, #00FFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-shadow: 
            0 0 30px rgba(0, 191, 255, 0.5),
            0 0 60px rgba(0, 191, 255, 0.3);
        animation: titleGlow 2s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }
    
    @keyframes titleGlow {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.3); }
    }
    
    .tagline {
        font-size: 1.3rem;
        color: #00BFFF;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
        position: relative;
        z-index: 1;
    }
    
    .feature-card {
        background: linear-gradient(135deg, rgba(0, 191, 255, 0.15) 0%, rgba(138, 43, 226, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(0, 191, 255, 0.3);
        border-left: 4px solid #00BFFF;
        margin-bottom: 1rem;
        box-shadow: 
            0 0 20px rgba(0, 191, 255, 0.2),
            inset 0 0 20px rgba(0, 191, 255, 0.05);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateX(10px);
        box-shadow: 
            0 0 30px rgba(0, 191, 255, 0.4),
            inset 0 0 30px rgba(0, 191, 255, 0.1);
        border-left-width: 6px;
    }
    
    .feature-card h4 {
        color: #00FFFF;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #00BFFF;
        border-top: 2px solid rgba(0, 191, 255, 0.3);
        margin-top: 3rem;
        text-shadow: 0 0 10px rgba(0, 191, 255, 0.3);
        box-shadow: 0 -5px 20px rgba(0, 191, 255, 0.1);
    }
    
    /* Cyber-styled buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00BFFF 0%, #0099CC 100%);
        border: 2px solid #00BFFF;
        box-shadow: 
            0 0 20px rgba(0, 191, 255, 0.5),
            inset 0 0 20px rgba(255, 255, 255, 0.2);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    
    .stButton > button:hover {
        box-shadow: 
            0 0 40px rgba(0, 191, 255, 0.8),
            inset 0 0 30px rgba(255, 255, 255, 0.3);
        transform: translateY(-3px) scale(1.05);
        border-color: #00FFFF;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a1a 0%, #16213e 100%);
        border-right: 2px solid rgba(0, 191, 255, 0.3);
        box-shadow: 5px 0 20px rgba(0, 191, 255, 0.2);
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #00BFFF;
        text-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
        font-size: 2rem;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        background: rgba(10, 10, 26, 0.8);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00BFFF 0%, #0099CC 100%);
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #00FFFF 0%, #00DDFF 100%);
        box-shadow: 0 0 20px rgba(0, 191, 255, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# Load logo SVG
def load_logo():
    try:
        with open('assets/logo.svg', 'r') as f:
            return f.read()
    except:
        return ""

# Main landing page
def main_page():
    # Header with logo and title
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    
    # Logo
    logo_svg = load_logo()
    if logo_svg:
        st.markdown(f'<div class="logo-container">{logo_svg}</div>', unsafe_allow_html=True)
    
    st.markdown('<h1 class="app-title">ChatNova AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Smart Multi-Model AI Chat for Productivity & Creativity</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Main content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🚀 Welcome to the Future of AI Conversations")
        st.markdown("""
        ChatNova AI combines the power of multiple AI models into one seamless experience. 
        Whether you're creating content, writing code, or conducting research, our intelligent 
        personas adapt to your needs.
        """)
        
        # Start Chat button
        if st.button("🚀 Start Chat", type="primary", use_container_width=True):
            st.switch_page("pages/1_💬_Chat.py")
        
        st.markdown("---")
        
        # Features
        st.markdown("### ✨ Key Features")
        
        features = [
            ("🤖 Multi-AI Integration", "Support for OpenAI GPT, Anthropic Claude, and Google Gemini"),
            ("👥 AI Personas", "Creative Writer, Code Assistant, Business Expert, Research Pro"),
            ("📁 Document Processing", "Upload and chat with PDFs, DOCX, TXT, and CSV files"),
            ("💾 Persistent History", "Create, manage, and switch between multiple chat threads"),
            ("📤 Export Chats", "Download conversations as TXT or PDF files"),
            ("⚙️ Customizable", "Dark/light themes, model selection, and memory settings")
        ]
        
        for title, desc in features:
            st.markdown(f"""
            <div class="feature-card">
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # Sidebar with quick actions
    with st.sidebar:
        st.markdown("### Quick Setup")
        
        # API Key status
        openai_status = "✅" if st.session_state.api_keys['openai'] else "❌"
        anthropic_status = "✅" if st.session_state.api_keys['anthropic'] else "❌"
        gemini_status = "✅" if st.session_state.api_keys['gemini'] else "❌"
        
        st.markdown(f"""
        **API Keys Status:**
        - OpenAI: {openai_status}
        - Anthropic: {anthropic_status}
        - Gemini: {gemini_status}
        """)
        
        if st.button("⚙️ Configure Settings", use_container_width=True):
            st.switch_page("pages/2_⚙️_Settings.py")
        
        st.markdown("---")
        st.markdown("### 📊 Statistics")
        thread_count = len(st.session_state.chat_threads)
        st.metric("Chat Threads", thread_count)

    # Footer
    st.markdown("""
    <div class="footer">
        © 2025 ChatNova AI — Powered by Smart Solutions Organization
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main_page()
