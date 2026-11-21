import json
import requests
import re

def login_and_get_torrent_list(config_file):
    def login_qbittorrent(qbittorrent_username, qbittorrent_password, url):
        login_url = f"{url}/api/v2/auth/login"
        login_data = {'username': qbittorrent_username, 'password': qbittorrent_password}
        headers = {'Referer': url}
        session = requests.Session()

        try:
            response = session.post(login_url, data=login_data, headers=headers)
            if response.status_code in (200, 204):
                return session
            else:
                print("Failed to login. Status code:", response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            return None

    def get_torrent_list(session, url, state, category=None, tag=None, sort=None, reverse=False, limit=None, offset=None, hashes=None):
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

        try:
            response = session.get(torrent_list_url, params=params, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get torrent list with state '{state}'. Status code:", response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            return None

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Config file not found.")
        return

    username = config.get('qbittorrent_username')
    password = config.get('qbittorrent_password')
    qb_url = config.get('qb_url')
    state = config.get('state', 'downloading')

    session = login_qbittorrent(username, password, qb_url)
    if not session:
        print("Login failed.")
        return

    torrent_list = get_torrent_list(session, qb_url, state=state)
    if torrent_list:
        result = []
        for torrent in torrent_list:
            magnet_link = torrent['magnet_uri']
            simplified_magnet_link = re.sub(r'&dn=.*', '', magnet_link)
            torrent_info = {
                "name": torrent['name'],
                "magnet_link": simplified_magnet_link,
                "hash": torrent['hash']
            }
            result.append(torrent_info)

        with open('hash.json', 'w') as hash_file:
            json.dump(result, hash_file, indent=4)

        print(f"Torrents with state '{state}' saved to hash.json.")
    else:
        print(f"Failed to get torrent list with state '{state}'.")

if __name__ == "__main__":
    login_and_get_torrent_list('config.json')
