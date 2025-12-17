from playwright.sync_api import sync_playwright
from app import download_hls
from patch_local import patch
import uuid
from client import Client

m3u8_urls = []

client = Client()

def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]

        def on_request(req):
            if ".m3u8" in req.url:
                m3u8_urls.append(req.url)
                print(f"FOUND {req.url}")

        page.on("request", on_request)

        # page.goto(web)

        page.wait_for_timeout(18000)

        browser.close()

        for url in m3u8_urls:
            # Spamming time 💀💀💀💀
            mv_ID = str(uuid.uuid4())
            download_hls(client, mv_ID, url)
            patch(mv_ID)


if __name__ == '__main__':
    # movie_url = input("Enter movie url: ")
    run()
    print(''.join(m3u8_urls))