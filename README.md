# qBittorrent2PikPak

qBittorrent2PikPak，一个用于将 qBittorrent 的种子发送到 PikPak 下载任务的自动化工具。

## 功能

- 从状态为 下载 的列表中获取种子信息[可自行修改 get_torrent_list.py 调整种子来源]
- 使用 PikPak API 离线下载种子

## 安装

1. 克隆此存储库：

    ```bash
    git clone https://github.com/Adachi-Git/qBittorrent2PikPak.git
    ```

2. 安装依赖项：

    ```bash
    cd Torrent2PikPak
    pip install -r requirements.txt
    ```

## 使用

1. 在 `config.json` 文件中填写您的 PikPak 和其他相关信息
2. 打开 qBittorrent 设置中的的 WebUI 功能
3. 使用 qBittorrent 自带的 RSS 下载功能，取消自动开始下载，即把下载任务存放在“下载”状态，脚本执行会从 下载 列表获取磁链[可自行修改 get_torrent_list.py 调整种子来源]
4. 运行 `main.py` 开始运行项目：

    ```bash
    python main.py
    ```
   

## 注意事项

- 本项目仅供学习和研究使用，请勿用于非法用途。
- 使用前请确保您已经阅读并理解 PikPak 的使用条款。

## 贡献

欢迎对此项目提出问题、建议和改进。您可以通过提出 Issue 或提交 Pull Request 来贡献。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
