import streamlit as st
import requests
import time

# --- Page Config ---
st.set_page_config(
    page_title="PyTurbo AI | Advanced Python Optimizer",
    page_icon="�",
    layout="wide",
)

# --- Enhanced Glassmorphic CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Fira+Code:wght@400;500&display=swap');

    :root {
        --primary: #c084fc;
        --secondary: #38bdf8;
        --bg: #030712;
        --card-bg: rgba(255, 255, 255, 0.03);
        --border: rgba(255, 255, 255, 0.1);
    }

    .stApp {
        background-color: var(--bg);
        background-image: 
            radial-gradient(at 0% 0%, rgba(192, 132, 252, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(56, 189, 248, 0.15) 0px, transparent 50%);
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Auth Container */
    .auth-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 3rem;
        max-width: 450px;
        margin: 100px auto;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    /* Hero Header */
    .hero {
        text-align: center;
        padding: 4rem 0 2rem 0;
    }

    .hero h1 {
        font-weight: 800;
        font-size: 4.5rem;
        background: linear-gradient(135deg, #c084fc 0%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
        margin-bottom: 0;
    }

    .hero p {
        color: #94a3b8;
        font-size: 1.25rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        font-weight: 600;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background: rgba(3, 7, 18, 0.95) !important;
        border-right: 1px solid var(--border);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #c084fc 0%, #818cf8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 700 !important;
        width: 100%;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -5px rgba(192, 132, 252, 0.5);
    }

    /* Cards */
    .feature-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        padding: 2rem;
        border-radius: 20px;
        height: 100%;
        transition: border 0.3s ease;
    }
    .feature-card:hover {
        border-color: var(--primary);
    }

    /* Code Inputs */
    .stTextArea textarea {
        background: #0f172a !important;
        border: 1px solid var(--border) !important;
        font-family: 'Fira Code', monospace !important;
        color: #e2e8f0 !important;
        border-radius: 16px !important;
    }

    /* Navigation */
    .nav-link {
        color: #94a3b8;
        text-decoration: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
    }
    .nav-link.active {
        background: var(--card-bg);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'auth_state' not in st.session_state:
    st.session_state.auth_state = {'authenticated': False, 'user': None}
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- API Interaction ---
BACKEND_URL = "http://127.0.0.1:8000"

def login_user(username, password):
    try:
        res = requests.post(f"{BACKEND_URL}/login", json={"username": username, "password": password})
        return res.status_code == 200, res.json()
    except: return False, {"detail": "Server Offline"}

def signup_user(username, password):
    try:
        res = requests.post(f"{BACKEND_URL}/signup", json={"username": username, "password": password})
        return res.status_code == 200, res.json()
    except: return False, {"detail": "Server Offline"}

# --- Auth Pages ---
def show_login():
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Welcome Back</h2>", unsafe_allow_html=True)
    u = st.text_input("Username", key="login_u")
    p = st.text_input("Password", type="password", key="login_p")
    if st.button("SIGN IN"):
        success, data = login_user(u, p)
        if success:
            st.session_state.auth_state = {'authenticated': True, 'user': u}
            st.rerun()
        else:
            st.error(data.get('detail', 'Login Failed'))
    
    st.markdown("<p style='text-align: center; margin-top: 1rem; color: #64748b;'>New to PyTurbo? <a href='javascript:void(0)' onclick='window.location.reload()'>Create account</a></p>", unsafe_allow_html=True)
    if st.button("GO TO SIGN UP"):
        st.session_state.page = 'signup'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_signup():
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Join PyTurbo</h2>", unsafe_allow_html=True)
    u = st.text_input("Choose Username", key="reg_u")
    p = st.text_input("Strong Password", type="password", key="reg_p")
    p2 = st.text_input("Confirm Password", type="password", key="reg_p2")
    
    if st.button("CREATE ACCOUNT"):
        if p != p2: st.error("Passwords do not match")
        else:
            success, data = signup_user(u, p)
            if success:
                st.success("Account created! Redirecting to login...")
                time.sleep(1)
                st.session_state.page = 'login'
                st.rerun()
            else: st.error(data.get('detail', 'Signup Failed'))
    
    if st.button("BACK TO LOGIN"):
        st.session_state.page = 'login'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main Dashboard ---
def show_dashboard():
    # Hero
    st.markdown("""
    <div class="hero">
        <p>Advanced Python Codebase Optimizer</p>
        <h1>PyTurbo AI</h1>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown(f"### 🛡️ User: {st.session_state.auth_state['user']}")
        api_key_input = st.text_input("OpenAI Key", type="password", help="Needed for AI processing")
        model = st.selectbox("Optimizing Model", ["gpt-4o", "gpt-4-turbo"])
        
        st.divider()
        if st.button("LOGOUT"):
            st.session_state.auth_state = {'authenticated': False, 'user': None}
            st.rerun()

    # Workspace
    col_in, col_out = st.columns([1, 1])

    with col_in:
        st.markdown("### 📝 Input Python Code")
        code = st.text_area("Function to optimize...", height=500, placeholder="def slow_function(n):\n    ...")
        optimize_btn = st.button("⚡ TURBO-OPTIMIZE PYTHON")

    with col_out:
        st.markdown("### 🚀 Optimized Output")
        if optimize_btn:
            if not api_key_input:
                st.error("Missing OpenAI API Key in sidebar")
            elif not code:
                st.warning("Please enter some Python code")
            else:
                with st.spinner("🚀 Rewriting code for maximum performance..."):
                    try:
                        res = requests.post(f"{BACKEND_URL}/optimize", 
                            json={"code": code, "model": model},
                            headers={"Authorization": f"Bearer {api_key_input}"})
                        
                        if res.status_code == 200:
                            result = res.json()['result']
                            st.markdown(result)
                        else:
                            st.error(res.json().get('detail', 'Engine Error'))
                    except Exception as e:
                        st.error(f"Engine connection failed: {str(e)}")
        else:
            st.info("Output will appear here after optimization.")

# --- Router ---
if not st.session_state.auth_state['authenticated']:
    if st.session_state.page == 'login': show_login()
    else: show_signup()
else:
    show_dashboard()

st.markdown("<p style='text-align: center; color: #475569; margin-top: 5rem;'>PyTurbo v2.0 | Pure Python Optimization Engine | Secure Glass Architecture</p>", unsafe_allow_html=True)
