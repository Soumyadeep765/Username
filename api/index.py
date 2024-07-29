from fastapi import FastAPI, HTTPException, Query, Request
from pydantic import BaseModel
import requests
import random
import string

app = FastAPI()

class UsernameRequest(BaseModel):
    username: str = None

def generate_random_username(length=8):
    """Generate a random username with diverse characters."""
    characters = string.ascii_letters + string.digits + '_'
    return ''.join(random.choices(characters, k=length))

def check_username_validity(username):
    """Check if the provided username is available."""
    url = f"https://t.me/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        response_text = response.text
        if "<div class=\"tgme_page_description\">" in response_text:
            return False
        else:
            return True
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

    if username:
        available = check_username_validity(username)
    else:
        username = generate_random_username()
        available = not check_username_validity(username)

    return {
        "available": available,
        "username": username,
        "credit": "@Teleservices_Api"
    }
