import time
import streamlit as st

from utils.api_client import upload_cv, get_status
from components.job_card import render_job_split_view
from components.uploader import render_upload_row
from components.loader import render_loader
from components.dismissible_banner import render_dismissible_success, reset_dismissible

st.set_page_config(
    page_title="Job Recommender",
    page_icon="briefcase",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Hide Streamlit's default sidebar nav + menu completely ───────────────────
# Also: center + pin the top section (header + upload row), let only the
# bottom results area scroll on its own.
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stSidebarNav"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }

        .block-container {
            padding-top: 0;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 100%;
        }

        /* Sticky wrapper for header + upload row — stays fixed while
           the page underneath scrolls. Centered with a max width so it
           doesn't stretch edge-to-edge like the results section below. */
        .top-sticky {
            position: sticky;
            top: 0;
            z-index: 999;
            background: var(--background-color, #0e1117);
            padding-top: 2rem;
            padding-bottom: 0.5rem;
        }
        .top-sticky-inner {
            max-width: 900px;
            margin: 0 auto;
        }

        .app-title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
            text-align: center;
        }
        .app-subtitle {
            color: #6b7280;
            text-align: center;
            margin-bottom: 1.8rem;
            font-size: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state defaults ────────────────────────────────────────────────────
if "task_id" not in st.session_state:
    st.session_state.task_id = None
if "status" not in st.session_state:
    st.session_state.status = "idle"          # idle | processing | done | failed
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "error" not in st.session_state:
    st.session_state.error = None
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "loader_tick" not in st.session_state:
    st.session_state.loader_tick = 0

# ── Sticky, centered top section: header + upload row ──────────────────────────
st.markdown('<div class="top-sticky"><div class="top-sticky-inner">', unsafe_allow_html=True)

st.markdown('<div class="app-title">Find your next role</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Upload your CV and get matched with relevant jobs instantly.</div>',
    unsafe_allow_html=True,
)

is_processing = st.session_state.status == "processing"
uploaded_file, upload_clicked, clear_clicked = render_upload_row(disabled=is_processing)

st.markdown('</div></div>', unsafe_allow_html=True)
# ── End sticky top section ──────────────────────────────────────────────────────

# ── Handle clear click — wipes everything back to a fresh state ───────────────
if clear_clicked:
    st.session_state.task_id = None
    st.session_state.status = "idle"
    st.session_state.jobs = []
    st.session_state.error = None
    st.session_state.loader_tick = 0
    st.session_state.uploader_key += 1   # forces a brand-new uploader widget
    st.session_state.selected_job_index = 0
    st.rerun()

# ── Handle upload click ────────────────────────────────────────────────────────
if upload_clicked:
    if uploaded_file is None:
        st.warning("Please choose a .txt CV file first.")
    else:
        with st.spinner(""):
            try:
                response = upload_cv(uploaded_file)
                st.session_state.task_id = response.get("task_id")
                st.session_state.status = "processing"
                st.session_state.jobs = []
                st.session_state.error = None
                st.session_state.selected_job_index = 0
                st.rerun()
            except Exception as e:
                st.session_state.status = "failed"
                st.session_state.error = str(e)

# ── Loader / polling section — appears directly below the sticky top ──────────
if st.session_state.status == "processing":
    render_loader()

    result = get_status(st.session_state.task_id)
    backend_status = result.get("status")

    if backend_status == "done":
        st.session_state.status = "done"
        st.session_state.jobs = result.get("jobs", [])
        reset_dismissible("results_banner")   # banner reappears for new results
        st.rerun()
    elif backend_status == "failed":
        st.session_state.status = "failed"
        st.session_state.error = result.get("error", "Something went wrong.")
        st.rerun()
    else:
        time.sleep(1.5)
        st.rerun()

# ── Failed state ────────────────────────────────────────────────────────────────
elif st.session_state.status == "failed":
    st.error(f"Processing failed: {st.session_state.error}")
    if st.button("Try again"):
        st.session_state.status = "idle"
        st.session_state.task_id = None
        st.session_state.error = None
        st.rerun()

# ── Done state — wide, independently scrollable results area ──────────────────
elif st.session_state.status == "done":
    jobs = st.session_state.jobs
    st.divider()
    render_dismissible_success(f"Found {len(jobs)} matching jobs", state_key="results_banner")

    if not jobs:
        st.info("No matching jobs found. Try a different CV or check back later.")
    else:
        render_job_split_view(jobs)