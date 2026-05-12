# iLink Bot API 细节

## 端点

| 端点 | 方法 | 需要 Token | Content-Type |
|------|------|:---:|------|
| `/ilink/bot/get_bot_qrcode?bot_type=3` | GET | ❌ | `application/octet-stream`（实际是 JSON） |
| `/ilink/bot/get_qrcode_status?qrcode=<hash>` | GET | ❌ | `application/octet-stream`（实际是 JSON） |

## get_bot_qrcode 响应

```json
{
  "qrcode": "7a82f61f1a1e2f95e4e78b75c2a89b40",
  "qrcode_img_content": "https://liteapp.weixin.qq.com/q/7GiQu1?qrcode=7a82f...&bot_type=3",
  "ret": 0
}
```

## get_qrcode_status 响应

状态流转：`wait` → `scaned` → `confirmed` 或 `expired`

```json
// 等待中
{"ret": 0, "status": "wait"}

// 已扫码未确认
{"ret": 0, "status": "scaned"}

// 确认成功（含新 Bot 凭证）
{
  "ret": 0,
  "status": "confirmed",
  "ilink_bot_id": "2b53f435e794@im.bot",
  "bot_token": "2b53f435e794@im.bot:06000033b09...",
  "ilink_user_id": "o9cq80xLB_74e_zHR6fJCVW-gOow@im.wechat",
  "baseurl": "https://ilinkai.weixin.qq.com",
  "qrcode": "..."
}

// 已过期
{"ret": 0, "status": "expired"}
```

## 关键发现

1. **每个 QR 扫码后创建新 Bot**：`ilink_bot_id` 和 `bot_token` 每次不同，不会复用已有 Bot
2. **不可多人共用**：一个 Bot 只能绑定一个微信用户
3. **QR 有效期约 35 秒**：必须秒发秒扫，或用自动刷新脚本
4. **长轮询注意事项**：`get_qrcode_status` 会阻塞 35s 等状态变化。轮询脚本用短超时（5s）+ 外部循环避免永久阻塞
5. **Content-Type 陷阱**：返回体是有效 JSON，但 HTTP 头是 `application/octet-stream`。aiohttp 的 `.json()` 会报 `ContentTypeError`。解决：`resp.text()` → `json.loads(text)`
6. **GET 不需要认证**：`get_bot_qrcode` 和 `get_qrcode_status` 只需要 `iLink-App-Id` 和 `iLink-App-ClientVersion` 头，不需要 token
