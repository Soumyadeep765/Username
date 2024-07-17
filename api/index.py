from fastapi import FastAPI, HTTPException
import aiohttp
import asyncio

BASE_URL = 'https://fragment.com/'
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'

app = FastAPI()

class Telegram:
    def __init__(self) -> None:
        pass

    async def get_user(self, username: str):
        url = BASE_URL + 'username/' + username
        headers = {
            'User-Agent': DEFAULT_USER_AGENT,
            'X-Aj-Referer': f'{BASE_URL}?query={username}',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    response_json = await response.json()
            except Exception as e:
                print(f"Error fetching data: {e}")
                return None
            
            if 'h' not in response_json:
                return 'Available'
            
            h_data = response_json['h']
            status = h_data.split('tm-section-header-status')[1].split('">')[0].strip()
            status_mapping = {
                'tm-status-taken': 'Taken',
                'tm-status-avail': 'Auctioned or for sale',
                'tm-status-unavail': 'Sold'
            }

            return status_mapping.get(status, 'Unknown')

@app.get("/username/{username}")
async def check_username(username: str):
    tg = Telegram()
    status = await tg.get_user(username)
    if status is None:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"username": username, "status": status}
