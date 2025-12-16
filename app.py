from dotenv import load_dotenv
from os import getenv
from logging import DEBUG, basicConfig, info, warning, error
from typing import Optional
from client import Client
from api import rophimapi, cdn
from utils import m3u8

basicConfig(
    level=DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

load_dotenv()

movie_id: Optional[str] = getenv("MOVIE_ID")
if not movie_id:
    error("MOVIE_ID is not set.")
    exit(1)

web_origin: Optional[str] = getenv("WEB_ORIGIN")
if not web_origin:
    web_origin = "https://rophim.li"

playlist_url: Optional[str] = getenv("PLAYLIST_URL")
if not playlist_url:
    playlist_url = None

client = Client()

try: 
    if playlist_url is None:
        master_playlist_url = input("Please input .m3u8 master playlist URL: ")
        info("Fetching master playlist...")
        m3u8_master_playlist = cdn.get_data(client, master_playlist_url)
        if m3u8_master_playlist is None:
            raise Exception("Failed to fetch master playlist.")
        with open(f"out/{movie_id}_master.m3u8", "w", encoding="utf-8") as f:
            f.write(m3u8_master_playlist)
        list_stream = m3u8.load_playlist(m3u8_master_playlist)
        selected_variant = m3u8.get_first_variant_playlist(list_stream)
        info(f"Selected stream URI: {selected_variant.uri}")
        if not selected_variant.uri:
            raise Exception("No URI found for selected variant playlist.")
        playlist_url = selected_variant.uri
        
    info("Fetching variant playlist...")
    variant = cdn.get_data(client, playlist_url)
    if variant is None:
        raise Exception("Failed to fetch variant playlist.")
    with open(f"out/{movie_id}_variant.m3u8", "w", encoding="utf-8") as f:
        f.write(variant)
    variant_data = m3u8.load_playlist(variant)
    for i in range(len(variant_data.segments)):
        segment = variant_data.segments[i]
        info(f"Segment {i + 1}: {segment.uri}")
        if not segment.uri:
            warning(f"No URI found for segment {i + 1}, skipping...")
            continue
        data = cdn.get_binary_data(client, segment.uri)
        if data is None:
            warning(f"Failed to fetch segment {i + 1}, skipping...")
            continue
        with open(f"out/{movie_id}_segment_{i + 1}.ts", "wb") as f:
            f.write(data)

except Exception as e:
    error(f"An error occurred: {e}")
    exit(1)
