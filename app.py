import streamlit as st
from verity import verify

# ----------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------
st.set_page_config(
    page_title="FakeCheck · Verity",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------
# Claymorphism CSS
# ----------------------------------------------------------------
CLAY_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #F4F1FA 0%, #EDE8F8 100%);
    }

    #MainMenu, footer, header {visibility: hidden;}

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* ---------- Hero ---------- */
    .hero {
        text-align: center;
        margin-bottom: 2.5rem;
        padding: 2rem 1rem;
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: -2px;
        background: linear-gradient(135deg, #8B7CF6 0%, #B794F6 50%, #F6AD55 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1.1;
    }

    .hero-sub {
        color: #6B6389;
        font-size: 1.15rem;
        font-weight: 600;
        margin-top: 0.75rem;
        letter-spacing: 0.2px;
    }

    /* ---------- Clay card ---------- */
    .clay-card {
        background: #F4F1FA;
        border-radius: 32px;
        padding: 2rem 2.5rem;
        box-shadow:
            8px 8px 20px rgba(139, 124, 246, 0.15),
            -8px -8px 20px rgba(255, 255, 255, 0.95),
            inset 2px 2px 6px rgba(255, 255, 255, 0.6),
            inset -2px -2px 6px rgba(139, 124, 246, 0.06);
        margin-bottom: 1.75rem;
        border: 1px solid rgba(255, 255, 255, 0.7);
    }

    /* ---------- Clay input ---------- */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #F4F1FA !important;
        border: none !important;
        border-radius: 22px !important;
        padding: 1.1rem 1.4rem !important;
        font-size: 1rem !important;
        font-family: 'Nunito', sans-serif !important;
        color: #2D2A45 !important;
        box-shadow:
            inset 5px 5px 12px rgba(139, 124, 246, 0.12),
            inset -5px -5px 12px rgba(255, 255, 255, 0.95) !important;
        transition: all 0.2s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        box-shadow:
            inset 5px 5px 12px rgba(139, 124, 246, 0.18),
            inset -5px -5px 12px rgba(255, 255, 255, 0.95),
            0 0 0 3px rgba(139, 124, 246, 0.2) !important;
    }

    .stTextInput label, .stTextArea label {
        color: #6B6389 !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ---------- Clay button ---------- */
    .stButton > button {
        background: linear-gradient(135deg, #8B7CF6 0%, #A78BFA 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 22px !important;
        padding: 0.9rem 2.5rem !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        font-family: 'Nunito', sans-serif !important;
        letter-spacing: 0.3px;
        width: 100%;
        box-shadow:
            6px 6px 16px rgba(139, 124, 246, 0.35),
            -4px -4px 12px rgba(255, 255, 255, 0.9),
            inset 1px 1px 2px rgba(255, 255, 255, 0.5);
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:
            8px 8px 20px rgba(139, 124, 246, 0.4),
            -4px -4px 12px rgba(255, 255, 255, 0.9),
            inset 1px 1px 2px rgba(255, 255, 255, 0.5);
    }

    .stButton > button:active {
        transform: translateY(1px);
        box-shadow:
            inset 5px 5px 12px rgba(0, 0, 0, 0.15),
            inset -5px -5px 12px rgba(255, 255, 255, 0.2);
    }

    /* ---------- Verdict badges ---------- */
    .verdict-wrap {
        text-align: center;
        padding: 1rem 0 1.5rem 0;
    }

    .verdict-badge {
        display: inline-block;
        padding: 0.9rem 2.5rem;
        border-radius: 26px;
        font-size: 1.6rem;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-family: 'Nunito', sans-serif;
    }

    .verdict-real {
        background: linear-gradient(135deg, #C6F6D5 0%, #9AE6B4 100%);
        color: #22543D;
        box-shadow:
            6px 6px 16px rgba(72, 187, 120, 0.3),
            -4px -4px 12px rgba(255, 255, 255, 0.9),
            inset 2px 2px 6px rgba(255, 255, 255, 0.7),
            inset -2px -2px 6px rgba(72, 187, 120, 0.15);
    }

    .verdict-fake {
        background: linear-gradient(135deg, #FED7D7 0%, #FC8181 100%);
        color: #742A2A;
        box-shadow:
            6px 6px 16px rgba(245, 101, 101, 0.3),
            -4px -4px 12px rgba(255, 255, 255, 0.9),
            inset 2px 2px 6px rgba(255, 255, 255, 0.7),
            inset -2px -2px 6px rgba(245, 101, 101, 0.15);
    }

    .verdict-unknown {
        background: linear-gradient(135deg, #FEFCBF 0%, #F6E05E 100%);
        color: #744210;
        box-shadow:
            6px 6px 16px rgba(236, 201, 75, 0.35),
            -4px -4px 12px rgba(255, 255, 255, 0.9),
            inset 2px 2px 6px rgba(255, 255, 255, 0.7),
            inset -2px -2px 6px rgba(236, 201, 75, 0.15);
    }

    /* ---------- Confidence pill ---------- */
    .confidence-pill {
        display: inline-block;
        background: #EBE6F7;
        border-radius: 18px;
        padding: 0.6rem 1.5rem;
        margin: 0.25rem;
        font-weight: 800;
        color: #4C4382;
        box-shadow:
            inset 3px 3px 8px rgba(139, 124, 246, 0.12),
            inset -3px -3px 8px rgba(255, 255, 255, 0.9);
    }

    /* ---------- Reasoning card ---------- */
    .reasoning-box {
        background: #F4F1FA;
        border-radius: 24px;
        padding: 1.5rem 2rem;
        font-size: 1.02rem;
        line-height: 1.7;
        color: #3A3458;
        box-shadow:
            inset 5px 5px 14px rgba(139, 124, 246, 0.1),
            inset -5px -5px 14px rgba(255, 255, 255, 0.95);
    }

    /* ---------- Source links ---------- */
    .source-item {
        background: #F4F1FA;
        border-radius: 18px;
        padding: 0.9rem 1.3rem;
        margin: 0.5rem 0;
        box-shadow:
            4px 4px 12px rgba(139, 124, 246, 0.12),
            -3px -3px 10px rgba(255, 255, 255, 0.9);
        transition: all 0.15s ease;
    }

    .source-item:hover {
        transform: translateX(4px);
        box-shadow:
            6px 6px 16px rgba(139, 124, 246, 0.18),
            -3px -3px 10px rgba(255, 255, 255, 0.9);
    }

    .source-item a {
        color: #6B5AC9 !important;
        text-decoration: none !important;
        font-weight: 700;
        font-size: 0.95rem;
    }

    .source-title {
        color: #2D2A45;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.2rem;
    }

    /* ---------- Section labels ---------- */
    .section-label {
        font-size: 0.8rem;
        font-weight: 800;
        color: #8B7CF6;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 1.5rem 0 0.75rem 0;
    }

    .stSpinner > div {
        border-top-color: #8B7CF6 !important;
    }

    .chip {
        display: inline-block;
        background: #F4F1FA;
        border-radius: 14px;
        padding: 0.5rem 1rem;
        margin: 0.2rem 0.3rem;
        font-size: 0.85rem;
        color: #5B5288;
        font-weight: 600;
        box-shadow:
            3px 3px 8px rgba(139, 124, 246, 0.12),
            -2px -2px 6px rgba(255, 255, 255, 0.9);
        cursor: pointer;
        transition: all 0.15s;
    }
    .chip:hover {
        transform: translateY(-1px);
        color: #8B7CF6;
    }
</style>
"""

st.markdown(CLAY_CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------
# Hero
# ----------------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1 class="hero-title">FakeCheck</h1>
    <p class="hero-sub">Paste a claim. Verity searches the web, weighs the evidence, and tells you what's real.</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# Input card
# ----------------------------------------------------------------
st.markdown('<div class="clay-card">', unsafe_allow_html=True)

claim = st.text_area(
    "Enter your claim",
    placeholder="e.g. Petrol price was reduced by 50 rupees in Pakistan",
    height=100,
    key="claim_input",
)

st.markdown("<br>", unsafe_allow_html=True)
verify_clicked = st.button("🔍  Verify Claim", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Example chips
st.markdown('<div class="section-label">Try an example</div>', unsafe_allow_html=True)
examples = [
    "Petrol price was reduced by 50 rupees in Pakistan",
    "PTI won the 2024 general elections in Pakistan",
    "The earth is flat",
]
cols = st.columns(len(examples))
for i, ex in enumerate(examples):
    with cols[i]:
        if st.button(ex, key=f"ex_{i}", use_container_width=True):
            st.session_state["claim_input"] = ex
            st.rerun()

# ----------------------------------------------------------------
# Run verification
# ----------------------------------------------------------------
if verify_clicked and claim.strip():
    with st.spinner("Verity is searching the web and weighing the evidence..."):
        result = verify(claim.strip())

    st.markdown("<br>", unsafe_allow_html=True)

    verdict = result["verdict"]
    badge_class = {
        "REAL": "verdict-real",
        "FAKE": "verdict-fake",
        "UNVERIFIABLE": "verdict-unknown",
    }.get(verdict, "verdict-unknown")

    # Verdict + confidence
    st.markdown(f"""
    <div class="clay-card">
        <div class="verdict-wrap">
            <span class="verdict-badge {badge_class}">{verdict}</span>
            <div style="margin-top:1.2rem;">
                <span class="confidence-pill">Confidence: {result['confidence']*100:.0f}%</span>
                <span class="confidence-pill">Sources: {result['evidence_count']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Reasoning
    st.markdown('<div class="section-label">Reasoning</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="reasoning-box">{result["reasoning"]}</div>', unsafe_allow_html=True)

    # Sources
    if result["all_sources"]:
        st.markdown('<div class="section-label">Sources Verity consulted</div>', unsafe_allow_html=True)
        for src in result["all_sources"]:
            st.markdown(f"""
            <div class="source-item">
                <div class="source-title">{src['title']}</div>
                <a href="{src['url']}" target="_blank">{src['url']}</a>
            </div>
            """, unsafe_allow_html=True)

elif verify_clicked:
    st.warning("Please enter a claim first.")

# ----------------------------------------------------------------
# Footer
# ----------------------------------------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#A29BC0; font-size:0.85rem; font-weight:600;">
    FakeCheck · Verity Agent · FYP 2026 · Mubbshra Iqbal & Neha Javeed
</div>
""", unsafe_allow_html=True)
