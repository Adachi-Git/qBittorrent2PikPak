# qBittorrent2PikPak

一个将 qBittorrent 中的种子批量发送到 PikPak 离线下载的自动化工具。

## 功能

- 从 qBittorrent 获取指定状态的种子（磁力链接）
- 批量提交到 PikPak 离线下载
- 已下载去重（`downloaded_hashes.json`）

## 前置准备

- 已开启 Web UI 的 qBittorrent 客户端
- PikPak 账号及个人访问令牌（PAT）

### 创建 PikPak 个人访问令牌（PAT）

1. 登录 PikPak，进入「账号与安全 → 已连接的应用 → 个人访问令牌」
2. 点击「创建令牌」，输入名称、选择有效期（30 天～1 年，默认 90 天）
3. **务必勾选「Cloud Download」权限**（离线下载必需），其余按需勾选
4. 创建后复制令牌——**令牌只显示一次**，丢失需重新生成

## 安装

```bash
git clone https://github.com/Adachi-Git/qBittorrent2PikPak.git
cd qBittorrent2PikPak
pip install -r requirements.txt
```

## 配置

编辑 `config.json`：

| 字段 | 说明 |
|---|---|
| `qbittorrent_username` | qBittorrent Web UI 用户名 |
| `qbittorrent_password` | qBittorrent Web UI 密码 |
| `qb_url` | Web UI 地址，如 `http://localhost:8080` |
| `pikpak_access_token` | 上面创建的 PAT |
| `state` | 种子状态过滤，如 `downloading` / `seeding` / `all` |
| `proxy` | 代理地址（可选），如 `http://127.0.0.1:1080` |

## 使用

1. qBittorrent 开启 Web UI（设置 → Web UI → 启用 Web UI，确认端口 8080）
2. 将目标种子置于 `downloading` 状态（如用 RSS 下载、取消自动开始）
3. 运行：

```bash
python main.py
```

脚本流程：登录 qBittorrent → 获取指定状态种子 → 批量提交 PikPak 离线下载。

运行产物：

- `hash.json`：从 qBittorrent 提取的种子列表
- `downloaded_hashes.json`：已成功提交的磁力链接（用于去重，重复运行自动跳过）

## 注意事项

- **免费版每日离线转存有次数上限**，用尽会报 `task_daily_create_limit`，需等次日重置或开通 Premium
- PAT 有有效期（最长 1 年），过期后需重新创建并更新 `config.json`
- PAT 等同账号权限，请妥善保管；`config.json` 已在 `.gitignore` 中，不会被提交
- 本项目仅供学习研究，请遵守 PikPak 使用条款

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
