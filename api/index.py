from fastapi import FastAPI, HTTPException
import aiohttp
import logging

BASE_URL = 'https://fragment.com/'
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'

app = FastAPI()
logging.basicConfig(level=logging.INFO)

class Telegram:
    async def get_user(self, username: str):
        url = f"{BASE_URL}username/{username}"
        headers = {
            'User-Agent': DEFAULT_USER_AGENT,
            'X-Aj-Referer': f"{BASE_URL}?query={username}",
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
            except aiohttp.ClientError as e:
                logging.error(f"HTTP error fetching data: {e}")
                return None
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
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
        logging.error("Failed to fetch user data")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"username": username, "status": status}
