"""
🌿 Sustainable Shopping Advisor
AI-powered chatbot for eco-friendly product recommendations.
Built with Streamlit + Groq (Llama 3.3 70B)
INT428 Project — LPU
"""

import streamlit as st
from groq_client import chat
from memory import init_memory, add_message, get_last_n, clear_history
from pdf_handler import extract_text_from_pdf, store_pdf_context, get_pdf_context, clear_pdf_context
from prompts import (
    BASE_SYSTEM, SCORER_PROMPT, ALTERNATIVES_PROMPT,
    COMPARISON_PROMPT, CATEGORY_PROMPT, PDF_CONTEXT_PROMPT,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌿 Sustainable Shopping Advisor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.html("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  * { font-family: 'Inter', sans-serif !important; }

  /* Main background */
  .stApp { background: linear-gradient(135deg, #0a1f0a 0%, #0d2b0d 50%, #0a1a0a 100%) !important; }
  .main .block-container { padding-top: 1rem !important; }

  /* Sidebar */
  [data-testid="stSidebar"] { background: linear-gradient(180deg, #051205 0%, #0a1f0a 100%) !important; border-right: 1px solid #1a4d1a; }
  [data-testid="stSidebar"] * { color: #d4edda !important; }
  [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #4caf50 !important; }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] { gap: 6px; background: rgba(255,255,255,0.03); border-radius: 12px; padding: 6px; border: 1px solid rgba(76,175,80,0.2); }
  .stTabs [data-baseweb="tab"] { background: rgba(255,255,255,0.05); border-radius: 8px; padding: 10px 22px; font-weight: 600; color: #a5d6a7 !important; border: 1px solid transparent; transition: all 0.3s ease; }
  .stTabs [data-baseweb="tab"]:hover { background: rgba(76,175,80,0.15); border-color: rgba(76,175,80,0.3); }
  .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #2e7d32, #388e3c) !important; color: white !important; border-color: #4caf50 !important; box-shadow: 0 4px 15px rgba(76,175,80,0.4); }

  /* Chat bubbles */
  .chat-user {
    background: linear-gradient(135deg, #1b5e20, #2e7d32);
    color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0 8px 25%;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    font-size: 0.95rem;
    line-height: 1.5;
  }
  .chat-bot {
    background: rgba(255,255,255,0.06);
    color: #e8f5e9;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 25% 8px 0;
    border-left: 3px solid #4caf50;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    font-size: 0.95rem;
    line-height: 1.6;
    backdrop-filter: blur(10px);
  }

  /* Cards */
  .feature-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(76,175,80,0.25);
    border-radius: 16px;
    padding: 24px;
    margin: 12px 0;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
  }
  .feature-card:hover { border-color: rgba(76,175,80,0.5); box-shadow: 0 8px 32px rgba(76,175,80,0.1); }

  /* Hero */
  .hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #81c784, #4caf50, #a5d6a7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
  }
  .hero-subtitle { color: #81c784; font-size: 1.1rem; font-weight: 300; margin-bottom: 1.5rem; }

  /* Stat badges */
  .stat-badge {
    background: rgba(76,175,80,0.15);
    border: 1px solid rgba(76,175,80,0.3);
    border-radius: 50px;
    padding: 6px 16px;
    color: #a5d6a7;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
    margin: 4px;
  }

  /* Section headers */
  .section-header {
    color: #81c784;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .section-sub { color: #66bb6a; font-size: 0.9rem; margin-bottom: 16px; }

  /* Inputs */
  .stTextInput > div > div > input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(76,175,80,0.35) !important;
    border-radius: 10px !important;
    color: #e8f5e9 !important;
    padding: 10px 14px !important;
  }
  .stTextInput > div > div > input:focus { border-color: #4caf50 !important; box-shadow: 0 0 0 2px rgba(76,175,80,0.2) !important; }

  /* Buttons */
  .stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(135deg, #2e7d32, #388e3c) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 22px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(46,125,50,0.3) !important;
  }
  .stButton > button:hover, .stFormSubmitButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(46,125,50,0.5) !important;
  }

  /* Divider */
  hr { border-color: rgba(76,175,80,0.2) !important; }

  /* Alerts / info */
  .stAlert { border-radius: 10px !important; }
  [data-testid="stAlert"] { background: rgba(76,175,80,0.1) !important; border: 1px solid rgba(76,175,80,0.25) !important; color: #a5d6a7 !important; border-radius: 10px !important; }

  /* Spinner */
  .stSpinner > div { border-top-color: #4caf50 !important; }

  /* Selectbox */
  .stSelectbox [data-baseweb="select"] > div { background: rgba(255,255,255,0.07) !important; border-color: rgba(76,175,80,0.35) !important; color: #e8f5e9 !important; border-radius: 10px !important; }

  /* Sliders */
  [data-testid="stSlider"] [role="slider"] { background: #4caf50 !important; }
  [data-testid="stSlider"] [data-testid="stTickBar"] { background: rgba(76,175,80,0.3) !important; }

  /* File uploader */
  [data-testid="stFileUploader"] { background: rgba(255,255,255,0.04) !important; border: 1px dashed rgba(76,175,80,0.35) !important; border-radius: 10px !important; }

  /* Sidebar param box */
  .param-box {
    background: rgba(76,175,80,0.1);
    border: 1px solid rgba(76,175,80,0.25);
    border-radius: 10px;
    padding: 12px;
    margin: 8px 0;
  }

  /* Footer */
  .footer {
    text-align: center;
    color: rgba(165,214,167,0.5);
    font-size: 0.8rem;
    padding: 20px 0 10px;
    border-top: 1px solid rgba(76,175,80,0.15);
    margin-top: 40px;
  }
</style>
""")

# ── Session state ─────────────────────────────────────────────────────────────
for key in ["chat_history", "scorer_history", "alt_history", "compare_history", "pdf_history"]:
    init_memory(key)
if "pdf_loaded" not in st.session_state:
    st.session_state["pdf_loaded"] = False

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("assets/hero_banner.png", use_container_width=True)
    st.markdown("## 🌿 Eco Advisor")
    st.markdown("<span style='color:#66bb6a;font-size:0.85rem;'>INT428 · LPU · Powered by Groq</span>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### ⚙️ Model Settings")
    st.markdown('<div class="param-box">', unsafe_allow_html=True)
    temperature = st.slider("🌡️ Temperature", 0.0, 1.0, 0.4, 0.05,
        help="Low = factual | High = creative")
    top_p = st.slider("🎯 Top-p (Nucleus Sampling)", 0.1, 1.0, 0.9, 0.05,
        help="Lower = focused | Higher = diverse")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Parameter Guide")
    temp_label = "🔵 Factual mode" if temperature < 0.4 else "🟡 Balanced" if temperature < 0.7 else "🔴 Creative"
    topp_label  = "🔵 Focused"     if top_p < 0.5      else "🟡 Balanced" if top_p < 0.8      else "🔴 Broad"
    st.info(f"**Temperature:** {temperature}  \n{temp_label}")
    st.info(f"**Top-p:** {top_p}  \n{topp_label}")

    st.markdown("---")
    st.markdown("### 🌐 Language")
    lang = st.selectbox("Response Language", ["English", "Hindi", "Bilingual (Hindi + English)"])

    st.markdown("---")
    st.markdown("### 📄 Upload Document")
    uploaded_pdf = st.file_uploader("Upload PDF for Q&A", type=["pdf"])
    if uploaded_pdf:
        with st.spinner("Extracting text..."):
            pdf_text = extract_text_from_pdf(uploaded_pdf)
            store_pdf_context(pdf_text)
        st.success(f"✅ PDF loaded! ({len(pdf_text)} chars)")
    if st.session_state.get("pdf_loaded") and st.button("🗑️ Clear PDF"):
        clear_pdf_context()
        st.rerun()

    st.markdown("---")
    st.markdown("<small style='color:#66bb6a;'>**Model:** Llama 3.3 70B via Groq  \n**Type:** Generative LLM</small>", unsafe_allow_html=True)

# ── Language suffix ───────────────────────────────────────────────────────────
LANG_INSTRUCTIONS = {
    "English": "",
    "Hindi": "\n\nIMPORTANT: Respond entirely in Hindi (Devanagari script).",
    "Bilingual (Hindi + English)": "\n\nIMPORTANT: Respond bilingually — English first, then Hindi translation below separated by a divider.",
}
lang_suffix = LANG_INSTRUCTIONS[lang]

# ── Helpers ───────────────────────────────────────────────────────────────────
def render_chat(history_key: str):
    history = get_last_n(20, history_key)
    if not history:
        st.markdown("<div style='text-align:center;color:rgba(165,214,167,0.4);padding:30px 0;font-size:0.9rem;'>No messages yet. Start the conversation below! 🌱</div>", unsafe_allow_html=True)
        return
    for msg in history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bot">🌿 {msg["content"]}</div>', unsafe_allow_html=True)

def send_message(user_input: str, history_key: str, system: str) -> str:
    add_message("user", user_input, history_key)
    history = get_last_n(10, history_key)
    reply = chat(
        messages=history[:-1] + [{"role": "user", "content": user_input}],
        system_prompt=system + lang_suffix,
        temperature=temperature,
        top_p=top_p,
    )
    add_message("assistant", reply, history_key)
    return reply

# ── Hero Header ───────────────────────────────────────────────────────────────
col_hero_img, col_hero_text = st.columns([1, 2])
with col_hero_img:
    st.image("assets/hero_banner.png", use_container_width=True)
with col_hero_text:
    st.markdown('<div class="hero-title">🌿 Sustainable Shopping Advisor</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">AI-powered guide for eco-friendly purchasing decisions</div>', unsafe_allow_html=True)
    st.markdown("""
    <div>
      <span class="stat-badge">🤖 Llama 3.3 70B</span>
      <span class="stat-badge">⚡ Powered by Groq</span>
      <span class="stat-badge">🌍 Eco Intelligence</span>
      <span class="stat-badge">🇮🇳 Hindi + English</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 Chat Advisor", "📊 Product Scorer",
    "♻️ Find Alternatives", "⚖️ Compare Products", "📄 Document Q&A",
])

# ═══════════════════════════════════════════
# TAB 1 — Chat Advisor
# ═══════════════════════════════════════════
with tab1:
    c1, c2 = st.columns([1, 3])
    with c1:
        st.image("assets/chat_icon.png", use_container_width=True)
    with c2:
        st.markdown('<div class="section-header">💬 Ask the Eco Advisor</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Ask anything about sustainable shopping, eco-labels, green products, or environmental impact.</div>', unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            clear_history("chat_history"); st.rerun()

    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    render_chat("chat_history")
    st.markdown('</div>', unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        ci, cb = st.columns([5, 1])
        with ci:
            user_input = st.text_input("Your question", placeholder="e.g. What are the most eco-friendly laundry detergents? / क्या जैविक कपास टिकाऊ है?", label_visibility="collapsed")
        with cb:
            submitted = st.form_submit_button("Send 🌿")
    if submitted and user_input.strip():
        with st.spinner("Thinking..."):
            send_message(user_input.strip(), "chat_history", BASE_SYSTEM)
        st.rerun()
    elif submitted:
        st.warning("Please enter a message.")

# ═══════════════════════════════════════════
# TAB 2 — Product Sustainability Scorer
# ═══════════════════════════════════════════
with tab2:
    c1, c2 = st.columns([1, 3])
    with c1:
        st.image("assets/scorer_icon.png", use_container_width=True)
    with c2:
        st.markdown('<div class="section-header">📊 Product Sustainability Scorer</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Enter any product name to get a detailed eco-sustainability analysis and score out of 10.</div>', unsafe_allow_html=True)
        if st.button("🗑️ Clear", key="clear_scorer"):
            clear_history("scorer_history"); st.rerun()

    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    render_chat("scorer_history")
    st.markdown('</div>', unsafe_allow_html=True)

    with st.form("scorer_form", clear_on_submit=True):
        ca, cb = st.columns([5, 1])
        with ca:
            product_input = st.text_input("Product name", placeholder="e.g. Dove soap, Lays chips, H&M jeans, Nescafe coffee...", label_visibility="collapsed")
        with cb:
            score_btn = st.form_submit_button("Score 📊")
    if score_btn and product_input.strip():
        with st.spinner("Analyzing sustainability..."):
            send_message(f"Score the sustainability of this product: {product_input.strip()}", "scorer_history", SCORER_PROMPT)
        st.rerun()
    elif score_btn:
        st.warning("Please enter a product name.")

# ═══════════════════════════════════════════
# TAB 3 — Find Sustainable Alternatives
# ═══════════════════════════════════════════
with tab3:
    c1, c2 = st.columns([1, 3])
    with c1:
        st.image("assets/alternatives_icon.png", use_container_width=True)
    with c2:
        st.markdown('<div class="section-header">♻️ Find Sustainable Alternatives</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Enter a product you currently use and get 3 curated eco-friendly alternatives.</div>', unsafe_allow_html=True)
        if st.button("🗑️ Clear", key="clear_alt"):
            clear_history("alt_history"); st.rerun()

    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    render_chat("alt_history")
    st.markdown('</div>', unsafe_allow_html=True)

    with st.form("alt_form", clear_on_submit=True):
        ca, cb = st.columns([5, 1])
        with ca:
            alt_input = st.text_input("Product to replace", placeholder="e.g. Plastic water bottles, Zara fast fashion, Styrofoam cups...", label_visibility="collapsed")
        with cb:
            alt_btn = st.form_submit_button("Find ♻️")
    if alt_btn and alt_input.strip():
        with st.spinner("Finding eco alternatives..."):
            send_message(f"Find me sustainable alternatives to: {alt_input.strip()}", "alt_history", ALTERNATIVES_PROMPT)
        st.rerun()
    elif alt_btn:
        st.warning("Please enter a product.")

# ═══════════════════════════════════════════
# TAB 4 — Compare Two Products
# ═══════════════════════════════════════════
with tab4:
    c1, c2 = st.columns([1, 3])
    with c1:
        st.image("assets/compare_icon.png", use_container_width=True)
    with c2:
        st.markdown('<div class="section-header">⚖️ Compare Products — Sustainability</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Compare two products side-by-side to see which is more eco-friendly and why.</div>', unsafe_allow_html=True)
        if st.button("🗑️ Clear", key="clear_compare"):
            clear_history("compare_history"); st.rerun()

    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    render_chat("compare_history")
    st.markdown('</div>', unsafe_allow_html=True)

    with st.form("compare_form", clear_on_submit=True):
        ca, cb, cc = st.columns([3, 3, 1])
        with ca:
            product_a = st.text_input("Product A", placeholder="e.g. Coca-Cola plastic bottle")
        with cb:
            product_b = st.text_input("Product B", placeholder="e.g. Bisleri glass bottle")
        with cc:
            compare_btn = st.form_submit_button("Compare ⚖️")
    if compare_btn and product_a.strip() and product_b.strip():
        with st.spinner("Comparing sustainability..."):
            send_message(f"Compare these two products for sustainability:\nProduct A: {product_a.strip()}\nProduct B: {product_b.strip()}", "compare_history", COMPARISON_PROMPT)
        st.rerun()
    elif compare_btn:
        st.warning("Please enter both products.")

# ═══════════════════════════════════════════
# TAB 5 — Document Q&A
# ═══════════════════════════════════════════
with tab5:
    c1, c2 = st.columns([1, 3])
    with c1:
        st.image("assets/document_icon.png", use_container_width=True)
    with c2:
        st.markdown('<div class="section-header">📄 Document-Based Q&A</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Upload a PDF (sustainability report, product manual, eco certification) and ask questions about its content.</div>', unsafe_allow_html=True)

    if not st.session_state.get("pdf_loaded"):
        st.markdown('<div class="feature-card" style="text-align:center;padding:40px;">', unsafe_allow_html=True)
        st.markdown("📎 **Upload a PDF document using the sidebar** to enable Document Q&A.")
        st.markdown("*Supports sustainability reports, product manuals, eco certification documents and more.*")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("✅ Document loaded — ask your questions below!")
        if st.button("🗑️ Clear", key="clear_pdf"):
            clear_history("pdf_history"); st.rerun()

        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        render_chat("pdf_history")
        st.markdown('</div>', unsafe_allow_html=True)

        with st.form("pdf_form", clear_on_submit=True):
            ca, cb = st.columns([5, 1])
            with ca:
                pdf_question = st.text_input("Ask about the document", placeholder="e.g. What eco certifications are mentioned? Summarize sustainability claims...", label_visibility="collapsed")
            with cb:
                pdf_btn = st.form_submit_button("Ask 📄")
        if pdf_btn and pdf_question.strip():
            pdf_context = get_pdf_context()
            with st.spinner("Reading document and answering..."):
                send_message(pdf_question.strip(), "pdf_history", PDF_CONTEXT_PROMPT.format(doc_text=pdf_context))
            st.rerun()
        elif pdf_btn:
            st.warning("Please enter a question.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  🌿 Sustainable Shopping Advisor &nbsp;|&nbsp; INT428 &nbsp;|&nbsp; LPU &nbsp;|&nbsp;
  Built with Streamlit + Groq (Llama 3.3 70B) &nbsp;|&nbsp;
  <span style="color:#4caf50;">♻️ Making the world greener, one purchase at a time.</span>
</div>
""", unsafe_allow_html=True)



