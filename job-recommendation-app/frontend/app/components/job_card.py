import streamlit as st


def render_job_list_item(job: dict, index: int, is_selected: bool) -> bool:
    """
    Renders one compact row in the left-hand job list (30% column).
    Shows only title, company, location, and match % — no description.

    Returns True if this row was clicked.
    """
    score_pct = round(job.get("score", 0) * 100)

    container_style = "background-color: var(--secondary-background-color);" if is_selected else ""
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="{container_style} padding: 6px 4px;">
                <p style="margin:0; font-size:17px; font-weight:600;">{job.get('title', 'Untitled role')}</p>
                <p style="margin:4px 0 0; font-size:14px; color:#6b7280;">
                    {job.get('company', 'Unknown company')} | {job.get('job_type', 'Remote')}
                </p>
                <p style="margin:6px 0 0; font-size:14px; color:#4F46E5; font-weight:600;">
                    {score_pct}% match
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        clicked = st.button(
            "View details",
            key=f"job_select_{index}",
            use_container_width=True,
        )

    return clicked


def render_job_detail(job: dict | None):
    """
    Renders the full job description in the right-hand pane (70% column).
    Shown when a job is selected from the list on the left.
    """
    if job is None:
        st.info("Select a job from the list to see full details here.")
        return

    score_pct = round(job.get("score", 0) * 100)

    st.subheader(job.get("title", "Untitled role"))
    st.caption(
        f"{job.get('company', 'Unknown company')} · "
        f"{job.get('job_type', 'Remote')} · "
        f"{score_pct}% match"
    )
    st.divider()
    st.markdown(
        f"<div style='font-size:16px; line-height:1.8;'>{job.get('clean_description', 'No description provided.')}</div>",
        unsafe_allow_html=True,
    )

    skills = job.get("required_skills", [])
    if skills:
        st.markdown("&nbsp;")
        st.markdown("**Required skills**")
        st.write(", ".join(skills))


def render_job_split_view(jobs: list[dict]):
    """
    Renders the full master-detail layout:
      - left 30%: scrollable list of compact job rows
      - right 70%: full description of the selected job

    Uses st.container(height=...) — Streamlit's native scrollable
    container — rather than custom CSS/vh math, which does not reliably
    measure the real viewport inside Streamlit's embedded iframe.

    Selection is tracked in st.session_state["selected_job_index"].
    """
    if "selected_job_index" not in st.session_state:
        st.session_state.selected_job_index = 0

    if "pane_height" not in st.session_state:
        st.session_state.pane_height = 750

    with st.expander("Adjust panel height", expanded=False):
        st.session_state.pane_height = st.slider(
            "Height (px)",
            min_value=400,
            max_value=1400,
            value=st.session_state.pane_height,
            step=50,
            help="If there's empty space below the panels, increase this. "
                 "If the page scrolls, decrease it.",
        )

    PANE_HEIGHT = st.session_state.pane_height

    list_col, detail_col = st.columns([3, 7], gap="large")
    print(jobs)

    with list_col:
        list_container = st.container(height=PANE_HEIGHT, border=False)
        with list_container:
            for idx, job in enumerate(jobs):
                is_selected = idx == st.session_state.selected_job_index
                clicked = render_job_list_item(job, idx, is_selected)
                if clicked:
                    st.session_state.selected_job_index = idx
                    st.rerun()

    with detail_col:
        detail_container = st.container(height=PANE_HEIGHT, border=True)
        with detail_container:
            if jobs:
                selected = jobs[st.session_state.selected_job_index]
                render_job_detail(selected)
            else:
                render_job_detail(None)