import asyncio
import json
import httpx

API_URL = "https://api-drive.mypikpak.com/drive/v1/files"


def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)


async def offline_download(client, pat, magnet_link):
    headers = {
        "Authorization": "Bearer " + pat,
        "Content-Type": "application/json",
        "User-Agent": "pikpak-cli/1.0.0",
    }
    data = {
        "kind": "drive#file",
        "upload_type": "UPLOAD_TYPE_URL",
        "url": {"url": magnet_link},
        "folder_type": "DOWNLOAD",
    }
    resp = await client.post(API_URL, json=data, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    raise Exception(f"offline download failed: {resp.status_code} {resp.text[:200]}")


async def download_from_config():
    config = load_config()
    pat = config["pikpak_access_token"]
    proxy = config.get("proxy")

    client_args = {}
    if proxy:
        client_args["proxy"] = proxy

    with open('hash.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    try:
        with open('downloaded_hashes.json', 'r', encoding='utf-8') as f:
            downloaded_hashes = json.load(f)
    except FileNotFoundError:
        downloaded_hashes = []

    async with httpx.AsyncClient(**client_args) as client:
        for item in data:
            magnet_link = item['magnet_link']
            if magnet_link in downloaded_hashes:
                print("Skipping already downloaded magnet link:", magnet_link)
                continue

            print("Downloading from magnet link:", magnet_link)
            try:
                result = await offline_download(client, pat, magnet_link)
                print("Download result:", result)
                downloaded_hashes.append(magnet_link)
            except Exception as e:
                print(f"Failed to download magnet link: {magnet_link}. Error: {e}")
            finally:
                print("=" * 30, end="\n\n")

    with open('downloaded_hashes.json', 'w', encoding='utf-8') as f:
        json.dump(downloaded_hashes, f, indent=4)


if __name__ == "__main__":
    asyncio.run(download_from_config())
