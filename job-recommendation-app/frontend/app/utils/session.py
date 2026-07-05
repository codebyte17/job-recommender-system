import streamlit as st

def save_task(task_id: str):
    st.session_state["task_id"] = task_id

def get_task() -> str | None:
    return st.session_state.get("task_id")