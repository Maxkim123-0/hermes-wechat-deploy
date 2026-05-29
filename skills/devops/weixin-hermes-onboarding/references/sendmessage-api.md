# iLink sendmessage API — Cross-Gateway Reference

When calling iLink from outside a running gateway (e.g. cross-profile messages, debugging), use this exact format.

## Endpoint

```
POST https://ilinkai.weixin.qq.com/ilink/bot/sendmessage
```

## Headers (⚠️ ALL required — missing any one causes errcode -14)

```
Authorization: Bearer <bot_token>
AuthorizationType: ilink_bot_token          ← MISSING in earlier attempts!
Content-Type: application/json
Content-Length: <byte_length_of_body>        ← MUST match body size
X-WECHAT-UIN: <random_base64>               ← Random per request
iLink-App-Id: bot
iLink-App-ClientVersion: 131584             ← (2<<16)|(2<<8)|0
```

Python example:
```python
uin_value = struct.unpack(">I", secrets.token_bytes(4))[0]
x_wechat_uin = base64.b64encode(str(uin_value).encode()).decode()

headers = {
    "Content-Type": "application/json",
    "AuthorizationType": "ilink_bot_token",
    "Content-Length": str(len(body.encode("utf-8"))),
    "X-WECHAT-UIN": x_wechat_uin,
    "iLink-App-Id": "bot",
    "iLink-App-ClientVersion": "131584",
    "Authorization": f"Bearer {token}",
}
```

## Payload (⚠️ must include base_info — missing it = session timeout)

```json
{
  "msg": {
    "from_user_id": "",
    "to_user_id": "o9cq80xLB_74e_zHR6fJCVW-gOow@im.wechat",
    "client_id": "hermes-weixin-<random_uuid_hex>",
    "message_type": 2,
    "message_state": 2,
    "context_token": "<from context-tokens.json, optional>",
    "item_list": [
      {
        "type": 1,
        "text_item": {
          "text": "消息内容"
        }
      }
    ]
  },
  "base_info": {
    "channel_version": "2.2.0"
  }
}
```

Python:
```python
payload = {
    "msg": { ... },
    "base_info": {"channel_version": "2.2.0"}
}
# MUST use compact JSON — no spaces!
body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
```

## Success Response

Empty object `{}` = message sent. This differs from typical iLink responses:
- `{}` → ✅ Success (message delivered)
- `{"errcode": -14}` → ❌ Session timeout (context_token expired or missing headers/base_info)
- `{"errcode": -1}` → ❌ Bad request

| Field | Value | Constant in weixin.py |
|-------|-------|----------------------|
| `from_user_id` | `""` (empty string) | — |
| `to_user_id` | Target WeChat user ID (e.g. `o9cq80x...@im.wechat`) | — |
| `client_id` | `f"hermes-weixin-{uuid.uuid4().hex}"` | — |
| `message_type` | `2` | `MSG_TYPE_BOT = 2` |
| `message_state` | `2` | `MSG_STATE_FINISH = 2` |
| `item_list[].type` | `1` | `ITEM_TEXT = 1` |
| `context_token` | Opaque string from iLink inbound messages | — |

## context_token

- **Source**: `{hermes_home}/weixin/accounts/{account_id}.context-tokens.json`
- **Key format**: `"{account_id}:{user_id}"`
- **Lifecycle**: Obtained on each inbound message from iLink. Cached on disk by `ContextTokenStore`.
- **Critical rule**: After gateway restart, old context_tokens are **stale**. A direct `sendmessage` call with them returns `{"errcode": -14, "errmsg": "session timeout"}`. The user must send a new inbound message first.

## Token Storage Locations

| Profile | Accounts Dir |
|---------|-------------|
| xiaoxiaoxiong (main) | `~/.hermes/profiles/xiaoxiaoxiong/home/.hermes/weixin/accounts/` |
| Others (e.g. laopo) | `~/.hermes/profiles/{profile}/weixin/accounts/` |

Bot token is stored as `{bot_id}.json`. Context tokens as `{bot_id}.context-tokens.json`.

## Common Errors

| errcode | Meaning | Fix |
|---------|---------|-----|
| `-14` | Session timeout | Wait for user to send a message first, then use the fresh context_token from the gateway's reply |
| `-1` / HTTP 4xx | Bad request / auth | Check token format (`bot_id:hex_token`) and Authorization header |
| HTTP 404 | Wrong endpoint | Must be `/ilink/bot/sendmessage` (not `send_message` with underscore) |
