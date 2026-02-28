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


def generate(
    contents: list, model: str = "gemini-3-flash-preview", system: str = None
) -> str:
    access_token = refresh_access_token()
    project_id = os.getenv("PROJECT_ID")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "User-Agent": "google-api-nodejs-client/9.15.1",
    }

    request_body = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 65536,
        },
    }

    if system:
        request_body["systemInstruction"] = {"parts": [{"text": system}]}

    body = {
        "model": model,
        "project": project_id,
        "request": request_body,
    }

    url = f"{CODE_ASSIST_ENDPOINT}/{CODE_ASSIST_API_VERSION}:generateContent"
    r = requests.post(url, headers=headers, json=body)

    if not r.ok:
        print(f"generateContent error {r.status_code}: {r.text}")
        r.raise_for_status()

    return r.json()["response"]["candidates"][0]["content"]["parts"][0]["text"]


if __name__ == "__main__":
    print(generate([{"role": "user", "parts": [{"text": "Hello, how are you?"}]}]))
