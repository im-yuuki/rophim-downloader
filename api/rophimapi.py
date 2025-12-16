from client import Client
from typing import Optional
from logging import debug, warning
from utils.origin import set_origin_header

API_URL_PREFIX = "https://rophimapi.net/v1/"

def get_embed_link(client: Client, movie_id: str, origin: Optional[str] = None) -> str:
    url = f"{API_URL_PREFIX}player/getLink?movie_id={movie_id}"
    res = client.get_json(url, headers=set_origin_header(origin))
    if res is None:
        raise Exception("Failed to get embed link: No response")
    if res.get("status") != True:
        warning(f"Server returned error: {res.get('message')}")
    if res.get("result") is None:
        raise Exception("Failed to get embed link: No result in response")
    debug(f"Embed link retrieved: {res['result']}")
    return res["result"]
