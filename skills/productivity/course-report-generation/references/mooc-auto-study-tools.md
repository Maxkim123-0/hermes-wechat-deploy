# MOOC 刷课工具调研

> 调研日期: 2026-05-14 | 平台: 智慧树 + 中国大学MOOC

## 需求背景

用户需要自动化完成智慧树(zhihuishu.com)和中国大学MOOC(icourse163.org)课程进度条100%，包括视频播放和答题。

## 工具矩阵

### 智慧树 (zhihuishu.com)

| 工具 | Stars | 类型 | 部署方式 |
|------|-------|------|---------|
| [VermiIIi0n/fuckZHS](https://github.com/VermiIIi0n/fuckZHS) | ⭐2014 | Python CLI | 服务器，纯HTTP请求 |
| [CXRunfree/Autovisor](https://github.com/CXRunfree/Autovisor) | ⭐771 | Python + Playwright | 服务器，模拟浏览器 |
| [ocsjs/ocsjs](https://github.com/ocsjs/ocsjs) | ⭐3008 | 油猴脚本 | 用户浏览器 |

**推荐**: fuckZHS — 纯Python+requests，轻量，支持账号密码/二维码登录，AI答题，无需浏览器。

### 中国大学MOOC (icourse163.org)

| 工具 | Stars | 类型 | 部署方式 |
|------|-------|------|---------|
| [ocsjs/ocsjs](https://github.com/ocsjs/ocsjs) | ⭐3008 | 油猴脚本 | 用户浏览器 |
| [Moonyear817/MoocTools](https://github.com/Moonyear817/MoocTools) | ⭐1 | Chrome扩展 | 用户浏览器 |
| [Pu-NINE-9/MOOC-chrome-plugin](https://github.com/Pu-NINE-9/MOOC-chrome-plugin) | ⭐1 | Chrome扩展 | 用户浏览器 |

**推荐**: ocsjs — 安装Tampermonkey/ScriptCat后在icourse163.org页面自动生效，支持视频、答题。

## 登录注意事项

### 中国大学MOOC校园登录流程
1. 点击"登录|注册" → 选择"校园用户登录"(不是爱课程登录)
2. 选择学校(上海商学院) → 选择身份(学生)
3. 学号 + 认证码(身份证后6位) + 手机号
4. 可能需要短信验证码
5. 爱课程登录入口账号密码对校园用户不适用

### 智慧树登录
fuckZHS支持两种方式:
- 账号密码登录
- 二维码扫码登录(qrlogin: true)

## 搜索策略

GitHub前端在国内服务器被墙/超时，但 **GitHub REST API 可直接访问**:
```bash
curl -s "https://api.github.com/search/repositories?q=icourse163+mooc&sort=stars&per_page=10"
```

Gitee(码云)搜索结果少，直接用 GitHub API。

## 部署注意事项

- fuckZHS: `pip install -r requirements.txt`，配置 `config.json`(用户名/密码或二维码登录)
- Autovisor: 需要Playwright + Chromium，内存占用较高
- ocsjs: 用户在浏览器安装Tampermonkey → 访问 https://docs.ocsjs.com 安装脚本
- 服务器运行Python刷课脚本需要稳定的网络和足够的运行时间(通常数小时)
