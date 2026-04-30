# 🌿 Sustainable Shopping Advisor
**AI-powered chatbot for eco-friendly product recommendations**
> INT428 Project — LPU | Team LUNATICS

---

## 📌 Project Overview

The Sustainable Shopping Advisor is a domain-specific generative AI chatbot that helps users make environmentally responsible purchasing decisions. Powered by **Llama 3.3 70B** via **Groq API** and built with **Streamlit**.

### Features
| Feature | Description |
|---|---|
| 💬 Chat Advisor | General eco-shopping Q&A with session memory |
| 📊 Product Scorer | Rates any product on sustainability (1-10) |
| ♻️ Find Alternatives | Suggests 3 eco-friendly alternatives to harmful products |
| ⚖️ Compare Products | Side-by-side sustainability comparison |
| 📄 Document Q&A | Upload PDF → Ask questions about its eco claims |
| 🌐 Multilingual | English, Hindi, or Bilingual responses |
| ⚙️ Model Controls | Adjustable Temperature & Top-p in sidebar |

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+
- Groq API Key (free at [console.groq.com](https://console.groq.com/keys))

### Steps

```bash
# 1. Clone / unzip the project
cd sustainable-advisor

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your API key
# Edit .env file and replace with your actual key:
# GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx

# 5. Run the app
streamlit run app.py
```

App opens at: `http://localhost:8501`

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this folder to a **GitHub repo** (public or private)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New App** → select your repo → set `app.py` as the main file
4. In **Advanced Settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxx"
   ```
5. Click **Deploy** — you'll get a public URL like `https://yourname-eco-advisor.streamlit.app`

> ⚠️ Do NOT commit `.env` to GitHub. The Streamlit Secrets system replaces it.

---

## 🔧 Model Configuration (INT428 Evaluation)

| Parameter | Value | Effect |
|---|---|---|
| **Temperature** | 0.0–1.0 (default 0.4) | Low = factual, High = creative |
| **Top-p** | 0.1–1.0 (default 0.9) | Lower = safer/focused responses |
| **Model** | `llama-3.3-70b-versatile` | Via Groq API |
| **Max Tokens** | 1024 | Per response |
| **Memory** | Session-based (last 10 messages) | Context window management |

---

## 📁 Project Structure

```
sustainable-advisor/
├── app.py              # Main Streamlit application
├── groq_client.py      # Groq API wrapper (configurable params)
├── memory.py           # Session-based conversation memory
├── pdf_handler.py      # PDF text extraction (PyMuPDF)
├── prompts.py          # Domain-specific system prompts
├── requirements.txt    # Python dependencies
├── .env                # API keys (local only, not committed)
└── README.md           # This file
```

---

## 📚 Domain Knowledge Sources
- EPA Safer Choice Program
- Ellen MacArthur Foundation (Circular Economy)
- GoodGuide / EWG (Environmental Working Group)
- FSC, Fair Trade, Energy Star, B Corp, USDA Organic certification standards
- Rainforest Alliance & EU Ecolabel guidelines

---

## 🏫 Submission Details
- **Course:** INT428
- **University:** Lovely Professional University
- **Team:** LUNATICS
- **Chatbot Type:** Generative (LLM-based)
- **API Used:** Groq API
- **Model:** Llama 3.3 70B Versatile
