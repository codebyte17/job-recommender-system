import os
import requests

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/api")


def upload_cv(file):
    """
    Upload a CV to the FastAPI backend.

    Args:
        file: Streamlit UploadedFile object

    Returns:
        dict: JSON response from the backend
    """

    url = f"{BASE_URL}/upload-cv"

    files = {
        "file": (
            file.name,
            file.getvalue(),
            file.type or "application/octet-stream",
        )
    }

    try:
        response = requests.post(
            url,
            files=files,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
        }


def get_status(task_id: str):
    """
    Get processing status of an uploaded CV.
    """

    url = f"{BASE_URL}/status/{task_id}"

    try:
        response = requests.get(
            url,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
        }