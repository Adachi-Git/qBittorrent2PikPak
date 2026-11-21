import asyncio
import json
import os
import httpx
from pikpakapi import PikPakApi, PikpakException

TOKEN_FILE = "pikpak_token.json"


def load_encoded_token():
    try:
        with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("encoded_token")
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_encoded_token(client):
    token = getattr(client, "encoded_token", None)
    if token:
        with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
            json.dump({"encoded_token": token}, f)


async def build_client(config):
    pikpak_username = config["pikpak_username"]
    pikpak_password = config["pikpak_password"]
    proxy = config.get("proxy")

    httpx_client_args = {
        "transport": httpx.AsyncHTTPTransport(retries=3),
    }
    if proxy:
        httpx_client_args["proxy"] = proxy

    encoded_token = load_encoded_token()

    # 有缓存 token：尝试刷新，失败则回退到登录
    if encoded_token:
        client = PikPakApi(encoded_token=encoded_token, httpx_client_args=httpx_client_args)
        try:
            await client.refresh_access_token()
            save_encoded_token(client)
            return client
        except Exception:
            pass  # 刷新失败，走下面的登录流程

    # 无 token 或刷新失败：用账号密码登录
    client = PikPakApi(
        username=pikpak_username,
        password=pikpak_password,
        httpx_client_args=httpx_client_args,
    )
    await client.login()
    save_encoded_token(client)
    return client


async def download_from_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    client = await build_client(config)

    with open('hash.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    try:
        with open('downloaded_hashes.json', 'r', encoding='utf-8') as f:
            downloaded_hashes = json.load(f)
    except FileNotFoundError:
        downloaded_hashes = []

    for item in data:
        magnet_link = item['magnet_link']
        if magnet_link in downloaded_hashes:
            print("Skipping already downloaded magnet link:", magnet_link)
            continue

        print("Downloading from magnet link:", magnet_link)
        try:
            result = await client.offline_download(magnet_link)
            print("Download result:", result)
            downloaded_hashes.append(magnet_link)
        except PikpakException as e:
            print(f"Failed to download magnet link: {magnet_link}. Error: {e}")
        finally:
            print("=" * 30, end="\n\n")

    with open('downloaded_hashes.json', 'w', encoding='utf-8') as f:
        json.dump(downloaded_hashes, f, indent=4)


if __name__ == "__main__":
    asyncio.run(download_from_config())
