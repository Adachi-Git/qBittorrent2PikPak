import asyncio
import json
import httpx
from pikpakapi import PikPakApi, PikpakException

async def download_from_config():
    # 从配置文件中加载用户名、密码和代理位置
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        pikpak_username = config["pikpak_username"]
        pikpak_password = config["pikpak_password"]
        proxy = config.get("proxy")

    # 创建 PikPakApi 实例并登录
    client = PikPakApi(
        username=pikpak_username,
        password=pikpak_password,
        httpx_client_args={
            "proxy": proxy,
            "transport": httpx.AsyncHTTPTransport(retries=3),
        },
    )
    await client.login()

    # 从 JSON 文件中加载数据
    with open('hash.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 加载已下载的磁力链接
    try:
        with open('downloaded_hashes.json', 'r', encoding='utf-8') as f:
            downloaded_hashes = json.load(f)
    except FileNotFoundError:
        downloaded_hashes = []

    # 提取磁力链接并进行下载
    for item in data:
        magnet_link = item['magnet_link']
        if magnet_link in downloaded_hashes:
            print("Skipping already downloaded magnet link:", magnet_link)
            continue
        
        print("Downloading from magnet link:", magnet_link)
        try:
            result = await client.offline_download(magnet_link)
            print("Download result:", result)
            # 只有在成功下载后才将磁力链接添加到已下载的列表中
            downloaded_hashes.append(magnet_link)
        except PikpakException as e:
            print(f"Failed to download magnet link: {magnet_link}. Error: {e}")
        finally:
            print("=" * 30, end="\n\n")

    # 将已下载的磁力链接保存到文件中（只包含成功下载的）
    with open('downloaded_hashes.json', 'w', encoding='utf-8') as f:
        json.dump(downloaded_hashes, f, indent=4)

if __name__ == "__main__":
    asyncio.run(download_from_config())
