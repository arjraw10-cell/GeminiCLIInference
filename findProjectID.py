from dotenv import load_dotenv
import requests
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

CODE_ASSIST_ENDPOINT = "https://cloudcode-pa.googleapis.com"
CODE_ASSIST_API_VERSION = "v1internal"


def refresh_access_token() -> str:
    r = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN,
            "grant_type": "refresh_token",
        },
    )
    r.raise_for_status()
    return r.json()["access_token"]


def get_project_id(access_token: str) -> str:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "User-Agent": "google-api-nodejs-client/9.15.1",
    }
    body = {}

    r = requests.post(
        f"{CODE_ASSIST_ENDPOINT}/{CODE_ASSIST_API_VERSION}:loadCodeAssist",
        headers=headers,
        json=body,
    )

    if not r.ok:
        print(f"loadCodeAssist error {r.status_code}: {r.text}")
        r.raise_for_status()

    data = r.json()

    project = data.get("cloudaicompanionProject")
    if isinstance(project, str) and project:
        _project_id = project
        return _project_id
    if isinstance(project, dict) and project.get("id"):
        _project_id = project["id"]
        return _project_id

    raise RuntimeError(f"Could not determine project ID. Full response: {data}")


print(get_project_id(refresh_access_token()))
