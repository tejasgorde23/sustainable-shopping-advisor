"""
PDF handler — extracts text from uploaded PDFs using PyMuPDF (fitz).
Used for document-based Q&A feature.
"""

import fitz  # PyMuPDF
import streamlit as st


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract all text from a Streamlit UploadedFile (PDF).

    Args:
        uploaded_file: Streamlit file uploader object

    Returns:
        Extracted text as a single string, truncated to ~8000 chars for token safety.
    """
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    full_text = []
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            full_text.append(f"[Page {page_num + 1}]\n{text.strip()}")

    doc.close()

    combined = "\n\n".join(full_text)

    # Truncate to ~8000 chars to stay within token limits while keeping useful context
    if len(combined) > 8000:
        combined = combined[:8000] + "\n\n[Document truncated for length. Showing first ~8000 characters.]"

    return combined


def store_pdf_context(text: str):
    """Store extracted PDF text in session state."""
    st.session_state["pdf_context"] = text
    st.session_state["pdf_loaded"] = True


def get_pdf_context() -> str | None:
    """Retrieve stored PDF context."""
    return st.session_state.get("pdf_context", None)


def clear_pdf_context():
    """Remove stored PDF context."""
    st.session_state["pdf_context"] = None
    st.session_state["pdf_loaded"] = False
