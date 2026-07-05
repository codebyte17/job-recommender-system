import streamlit as st

# Rotates through these while waiting — feels alive instead of a static spinner
LOADING_MESSAGES = [
    "Reading your CV...",
    "Extracting your skills...",
    "Matching you with jobs...",
    "Ranking the best fits...",
]


def render_loader():
    """
    Renders a rotating search icon with a cycling status message,
    directly below the upload row. Picks the next message based on
    a counter stored in session_state so it advances every rerun.
    """
    if "loader_tick" not in st.session_state:
        st.session_state.loader_tick = 0

    message = LOADING_MESSAGES[st.session_state.loader_tick % len(LOADING_MESSAGES)]
    st.session_state.loader_tick += 1

    st.markdown(
        f"""
        <style>
            @keyframes spin {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}
            .loader-wrap {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 2.2rem 0 1.6rem 0;
            }}
            .loader-icon {{
                font-size: 2.4rem;
                animation: spin 1.4s linear infinite;
                margin-bottom: 0.6rem;
            }}
            .loader-text {{
                color: #4b5563;
                font-size: 0.95rem;
                font-weight: 500;
            }}
        </style>

        <div class="loader-wrap">
            <div class="loader-icon">🔎</div>
            <div class="loader-text">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )