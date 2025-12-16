import cloudscraper25 as cloudscraper
from logging import debug, info, warning, error
from os import getenv
from typing import Optional

class Client:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper(
            enable_stealth=True,
            stealth_options={
                'min_delay': 0.1,
                'max_delay': 0.5,
                'human_like_delays': True,
                'randomize_headers': True,
                'browser_quirks': True
            }
        )
        debug("Set custom user agent")
        # update with a mapping so the type checker accepts the argument
        self.scraper.headers.update({
            "sec-ch-ua-platform": "Android",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?1",
            "origin": "https://goatembed.com",
            "referer": "https://goatembed.com/",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty"
        })

    def get_json(self, url: str, headers: Optional[dict] = None) -> Optional[dict]:
        new_headers = {}
        # if headers is not None:s
        #     new_headers.update(headers)
        # if self.user_agent is not None:
        #     new_headers["User-Agent"] = self.user_agent

        try:
            response = self.scraper.get(url)
            debug(f"GET {url}: {response.status_code}")
            if response.status_code != 200:
                warning(f"HTTP status: {response.status_code}")
            # response.raise_for_status()
            return response.json()
        except Exception as e:
            error(f"Request failed: {e}")
            return None

    def get_blob(self, url: str, headers: Optional[dict] = None) -> Optional[bytes]:
        new_headers = {}
        # if headers is not None:
        #     new_headers.update(headers)
        # if self.user_agent is not None:
        #     new_headers["User-Agent"] = self.user_agent

        try:
            response = self.scraper.get(url)
            debug(f"GET {url}: {response.status_code}")
            if response.status_code != 200:
                warning(f"HTTP status: {response.status_code}")
            # response.raise_for_status()
            return response.content
        except Exception as e:
            error(f"Request failed: {e}")
            return None
