import json
import requests
import re

def login_and_get_torrent_list(config_file):
    def login_qbittorrent(qbittorrent_username, qbittorrent_password, url):
        login_url = f"{url}/api/v2/auth/login"
        login_data = {'username': qbittorrent_username, 'password': qbittorrent_password}
        headers = {'Referer': url}
        
        try:
            response = requests.post(login_url, data=login_data, headers=headers)
            if response.status_code == 200:
                return response.cookies['SID']
            else:
                print("Failed to login. Status code:", response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            return None
    
    def get_torrent_list(session_id, url, state='downloading', category=None, tag=None, sort=None, reverse=False, limit=None, offset=None, hashes=None):
        torrent_list_url = f"{url}/api/v2/torrents/info"
        params = {
            'filter': state,
            'category': category,
            'tag': tag,
            'sort': sort,
            'reverse': reverse,
            'limit': limit,
            'offset': offset,
            'hashes': hashes
        }
        headers = {'Referer': url}
        cookies = {'SID': session_id}

        try:
            response = requests.get(torrent_list_url, params=params, headers=headers, cookies=cookies)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get torrent list with state '{state}'. Status code:", response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            return None
    
    # 从配置文件中读取用户名、密码和 qbittorrent URL
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Config file not found.")
        return
    
    username = config.get('username')
    password = config.get('password')
    qb_url = config.get('qb_url')
    
    # 登录到 qBittorrent
    session_id = login_qbittorrent(username, password, qb_url)
    if not session_id:
        print("Login failed.")
        return
    
    # 获取下载中的种子列表
    downloading_torrent_list = get_torrent_list(session_id, qb_url, state='downloading')
    if downloading_torrent_list:
        result = []
        for torrent in downloading_torrent_list:
            magnet_link = torrent['magnet_uri']
            simplified_magnet_link = re.sub(r'&dn=.*', '', magnet_link)  # 移除 &dn= 及其后的内容
            torrent_info = {
                "name": torrent['name'],
                "magnet_link": simplified_magnet_link,
                "hash": torrent['hash']
            }
            result.append(torrent_info)
        
        # 将哈希值保存到 hash.json 文件中
        with open('hash.json', 'w') as hash_file:
            json.dump(result, hash_file, indent=4)
        
        print("Downloading torrents saved to hash.json.")
    else:
        print("Failed to get downloading torrent list.")