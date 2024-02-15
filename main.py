# main.py
import asyncio
from add_torrent import download_from_config
from get_torrent_list import login_and_get_torrent_list

def main():
    # 获取种子列表并保存到 hash.json
    login_and_get_torrent_list("config.json")
    
    # 下载种子文件
    asyncio.run(download_from_config())

if __name__ == "__main__":
    main()
