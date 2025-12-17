from dotenv import load_dotenv
from os import getenv
from logging import DEBUG, basicConfig, info, warning, error
from typing import Optional
from client import Client
from api import cdn
from utils import m3u8
from pathlib import Path
import random
basicConfig(
    level=DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

load_dotenv()

# movie_id: Optional[str] = getenv("MOVIE_ID")
# if not movie_id:
#     error("MOVIE_ID is not set.")
#     exit(1)

web_origin: Optional[str] = getenv("WEB_ORIGIN")
if not web_origin:
    web_origin = "https://rophim.li"

# playlist_url: Optional[str] = getenv("PLAYLIST_URL")
# if not playlist_url:
#     playlist_url = None

# client = Client()

def download_hls(
    client: Client,
    movie_id: str = None,
    playlist_url: str | None = None,
    out_dir: str = "out",
):
    try:
        out_dir = Path(f"{out_dir}/{movie_id}")
        if not out_dir.exists():
            out_dir.mkdir()

        if movie_id is None:
            import string
            movie_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        info("Fetching variant playlist...")
        variant = cdn.get_data(client, playlist_url)
        if variant is None:
            raise Exception("Failed to fetch variant playlist.")

        with open(out_dir / Path(f"{movie_id}_variant.m3u8"), "w", encoding="utf-8") as f:
            f.write(variant)

        variant_data = m3u8.load_playlist(variant)

        i = 0
        if getenv("START_SEGMENT"):
            start_segment = int(getenv("START_SEGMENT", 0))
            if 0 < start_segment <= len(variant_data.segments):
                i = start_segment - 1
                info(f"Resuming from segment {start_segment}...")
            else:
                warning("Invalid START_SEGMENT value, starting from the beginning...")

        while i < len(variant_data.segments):
            segment = variant_data.segments[i]
            info(f"Segment {i + 1}: {segment.uri}")

            if not segment.uri:
                warning(f"No URI found for segment {i + 1}, skipping...")
                i += 1
                continue

            data = cdn.get_binary_data(client, segment.uri)
            if data is None:
                warning(f"Failed to fetch segment {i + 1}, skipping...")
                i += 1
                continue

            with open(out_dir / Path(f"{movie_id}_segment_{i + 1}.ts"), "wb") as f:
                f.write(data)

            i += 1

        info("All segments downloaded successfully.")
        return movie_id

    except Exception as e:
        error(f"An error occurred: {e}")
        raise  # cho file gọi nó tự xử