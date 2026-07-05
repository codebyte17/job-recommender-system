import streamlit as st


def render_dismissible_success(message: str, state_key: str):
    """
    A success banner with a real X button in the top-right corner.
    Once dismissed, it stays hidden until reset_dismissible() is called
    (e.g. when a fresh CV is uploaded and new results come in).

    Built from a styled container + button since st.success has no
    built-in close affordance.
    """
    dismissed_key = f"{state_key}_dismissed"
    if dismissed_key not in st.session_state:
        st.session_state[dismissed_key] = False

    if st.session_state[dismissed_key]:
        return

    st.markdown(
        """
        <style>
            .success-banner-wrap div[data-testid="stHorizontalBlock"] {
                background-color: rgba(34, 139, 87, 0.15);
                border: 1px solid rgba(34, 139, 87, 0.4);
                border-radius: 8px;
                padding: 0.6rem 1rem;
                align-items: center;
                margin-bottom: 0.5rem;
            }
            .success-banner-wrap button {
                border: none !important;
                background: transparent !important;
                color: #888 !important;
                font-size: 1.1rem !important;
                padding: 0 !important;
                height: auto !important;
                min-height: 0 !important;
                line-height: 1 !important;
            }
            .success-banner-wrap button:hover {
                color: #e24b4a !important;
                background: transparent !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="success-banner-wrap">', unsafe_allow_html=True)
    col_msg, col_close = st.columns([30, 1], vertical_alignment="center")
    with col_msg:
        st.markdown(f"**{message}**")
    with col_close:
        if st.button("✕", key=f"{state_key}_close_btn"):
            st.session_state[dismissed_key] = True
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def reset_dismissible(state_key: str):
    """Call this whenever fresh results come in, so the banner reappears."""
    st.session_state[f"{state_key}_dismissed"] = False