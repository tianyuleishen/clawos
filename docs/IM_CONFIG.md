# 🦞 ClawOS IM平台配置

## 支持的平台

| 平台 | 必需配置 | 可选配置 |
|------|---------|---------|
| 飞书 | app_id, app_secret | webhook_url |
| 企业微信 | app_id, app_secret | agent_id |
| 钉钉 | app_key, app_secret | agent_id |
| QQ | http_url | access_token |

## 配置文件格式

配置文件保存在 `~/.clawos/im/{platform}.json`

### 飞书配置

```json
{
    "platform": "feishu",
    "app_id": "your_app_id",
    "app_secret": "your_app_secret"
}
```

### 企业微信配置

```json
{
    "platform": "wecom",
    "app_id": "your_corp_id",
    "app_secret": "your_app_secret",
    "agent_id": "your_agent_id"
}
```

### 钉钉配置

```json
{
    "platform": "dingtalk",
    "app_key": "your_app_key",
    "app_secret": "your_app_secret"
}
```

### QQ配置

```json
{
    "platform": "qq",
    "http_url": "http://localhost:5700",
    "access_token": "your_access_token"
}
```

## 获取凭证

### 飞书

1. 登录 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业应用
3. 在"凭证与权限"页面获取app_id和app_secret
4. 开通"发消息"权限

### 企业微信

1. 登录 [企业微信管理后台](https://work.weixin.qq.com/)
2. 创建应用
3. 获取corp_id (在"我的企业"页面)
4. 获取agent_id和app_secret (在应用详情页面)

### 钉钉

1. 登录 [钉钉开放平台](https://open.dingtalk.com/)
2. 创建应用
3. 获取appKey和appSecret

### QQ (go-cqhttp)

1. 下载 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
2. 配置account和HTTP服务器
3. 启动后配置ClawOS连接

## 常见问题

### Q: 飞书连接失败
A: 检查app_id和app_secret是否正确，确认应用已发布

### Q: 企业微信消息发送失败
A: 检查agent_id是否配置，确认应用有发消息权限

### Q: QQ连接失败
A: 确认go-cqhttp已启动，http_url是否正确

