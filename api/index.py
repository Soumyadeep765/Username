from fastapi import FastAPI, Query, HTTPException, Request
from pydantic import BaseModel
import requests
import random
import string

app = FastAPI()

class UsernameRequest(BaseModel):
    username: str = None

def generate_random_username(length=6):
    """Generate a random username."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def check_username_validity(username):
    """Check the validity of the provided username."""
    url = f"https://t.me/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        response_text = response.text
        if "</div>\n<div class=\"tgme_page_description\">\n  If you have <strong>Telegram</strong>, you can contact <a class=\"tgme_username_link\" href=\"tg:resolve?domain=" in response_text:
            return False
        elif f"<div class=\"tgme_page_extra\">\n  @{username}\n</div>" in response_text or f"<div class=\"tgme_page_context_link_wrap\"><a class=\"tgme_page_context_link\" href=\"/s/{username}\">Preview channel</a></div>" in response_text:
            return True
        else:
            return False
    else:
        return False

@app.get("/username")
@app.post("/username")
async def get_username(request: Request, data: UsernameRequest = None):
    """Check if a username is available or generate a random username."""
    if request.method == "POST":
        if data and data.username:
            username = data.username
        else:
            username = generate_random_username()
    else:
        username = Query(None, description="Username to check")

    if username is None:
        username = generate_random_username()

    available = check_username_validity(username)

    return {
        "available": available,
        "username": username,
        "credit": "@Teleservices_Api"
    }
