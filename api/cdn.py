from typing import Optional
from client import Client
from logging import debug, warning
from utils.origin import set_origin_header

def get_data(client: Client, playlist_url: str, origin: Optional[str] = None) -> Optional[str]:
    res = client.get_blob(playlist_url, headers=set_origin_header(origin))
    if res is None:
        warning("Failed to retrieve master playlist")
        return None
    playlist_content = res.decode("utf-8")
    debug("Master playlist retrieved successfully")
    return playlist_content

def get_binary_data(client: Client, url: str, origin: Optional[str] = None) -> Optional[bytes]:
    res = client.get_blob(url, headers=set_origin_header(origin))
    if res is None:
        warning(f"Failed to retrieve binary data from {url}")
        return None
    debug(f"Binary data retrieved successfully from {url}")
    return res