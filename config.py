import os
from typing import Optional

import streamlit as st


def _from_streamlit_secrets(key: str) -> Optional[str]:
    """Return a value from Streamlit secrets if present."""
    try:
        if key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        # If Streamlit secrets is unavailable in current runtime, ignore.
        return None
    return None


def get_setting(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Resolve config from Streamlit secrets first, then environment variables.
    """
    secret_value = _from_streamlit_secrets(key)
    if secret_value:
        return secret_value

    env_value = os.getenv(key)
    if env_value is not None and env_value.strip():
        return env_value.strip()

    return default
