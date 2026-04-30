"""
Session-based conversation memory for the Sustainable Shopping Advisor.
Uses Streamlit session_state to persist history within a session.
"""

import streamlit as st


def init_memory(key: str = "chat_history"):
    """Initialize conversation history in session state if not present."""
    if key not in st.session_state:
        st.session_state[key] = []


def add_message(role: str, content: str, key: str = "chat_history"):
    """Append a message to the conversation history."""
    st.session_state[key].append({"role": role, "content": content})


def get_history(key: str = "chat_history") -> list[dict]:
    """Return the full conversation history."""
    return st.session_state.get(key, [])


def clear_history(key: str = "chat_history"):
    """Reset conversation history."""
    st.session_state[key] = []


def get_last_n(n: int = 10, key: str = "chat_history") -> list[dict]:
    """
    Return last N messages to keep context window manageable.
    Default: last 10 messages (~5 turns).
    """
    history = st.session_state.get(key, [])
    return history[-n:] if len(history) > n else history
