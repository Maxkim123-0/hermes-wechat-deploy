---
name: github-resource-discovery
description: 用 GitHub API 搜索现成开源方案。做任何工具类任务前先搜，不自造轮子。文档了 API、git clone、raw 镜像等可用路径。
category: software-development
triggers:
  - 找脚本 / 搜GitHub / 开源方案 / 现成的 / 有没有工具 / 搜一下
---

# GitHub 资源搜索

## 核心原则
**做任何工具类任务前，先搜 GitHub，不自造轮子。**

## 可用路径

### 1. GitHub API（稳定，不走浏览器）
```bash
curl -s "https://api.github.com/search/repositories?q=KEYWORD&sort=stars&per_page=10" | python3 -c "
import json,sys; d=json.load(sys.stdin)
for r in d.get('items',[]): print(f'★{r[\"stargazers_count\"]}|{r[\"full_name\"]}|{(r[\"description\"] or \"N/A\")[:100]}')
"
```

### 2. Git Clone（直接拉代码）
```bash
git clone --depth 1 https://github.com/USER/REPO.git /tmp/REPO
```
- 用 `--depth 1` 加快速度
- 超时设 30s，超时换方案

### 3. Raw 文件（直接读内容）
```bash
curl -s "https://raw.githubusercontent.com/USER/REPO/main/FILE"
```
- 已验证可通（HTTP 200）

### 4. 镜像站（备选）
- Gitee: https://search.gitee.com/?q=KEYWORD&type=repository
- GitHub 镜像不稳定，优先用 API

## 搜索技巧

| 场景 | 关键词 |
|------|--------|
| 网课刷课 | icourse163 / zhihuishu + 刷课 |
| 自动化脚本 | playwright / puppeteer + 自动化 |
| 下载工具 | downloader / 下载器 |
| 油猴脚本 | tampermonkey + 平台名 |

## 不宜做的事
- 不要手动实现已有高星项目能做的事
- 不要硬写登录/滑块绕过（用现成方案或让用户手动完成）
- 不要假设方案A必行，搜备选方案并行判断
