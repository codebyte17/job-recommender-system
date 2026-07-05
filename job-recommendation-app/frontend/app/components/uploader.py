import streamlit as st


def render_upload_row(disabled: bool = False):
    """
    Renders the upload area: a wide file-uploader, an 'Upload' button,
    and a 'Clear' button — all in one row.

    The file-uploader's widget key is derived from a counter in
    session_state. Bumping that counter forces Streamlit to mount a
    brand-new uploader instance, which is the only reliable way to make
    an already-selected file disappear from the widget.

    Args:
        disabled: if True, both buttons are disabled (e.g. while processing)

    Returns:
        (uploaded_file, upload_clicked, clear_clicked)
    """
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0

    st.markdown(
        """
        <style>
            [data-testid="stFileUploaderDropzone"] {
                padding: 1.2rem;
                border-radius: 12px;
                border: 2px dashed #c7cad1;
            }
            [data-testid="stFileUploaderDropzone"]:hover {
                border-color: #4F46E5;
            }

            div[data-testid="column"] button {
                height: 3.2rem;
                width: 100%;
                font-size: 1rem;
                font-weight: 600;
                border-radius: 10px;
                margin-top: 1.6rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col_upload, col_submit, col_clear = st.columns([3.5, 1.1, 1.1], vertical_alignment="bottom")

    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload your CV",
            type=["txt"],
            label_visibility="collapsed",
            key=f"cv_uploader_{st.session_state.uploader_key}",
            disabled=disabled,
        )

    with col_submit:
        upload_clicked = st.button(
            "Upload",
            type="primary",
            use_container_width=True,
            key="upload_button",
            disabled=disabled,
        )

    with col_clear:
        clear_clicked = st.button(
            "Clear",
            use_container_width=True,
            key="clear_button",
            disabled=disabled,
        )

    return uploaded_file, upload_clicked, clear_clicked