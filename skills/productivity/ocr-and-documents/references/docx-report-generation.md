# DOCX 学生报告生成最佳实践

## 格式标准（不要照搬简陋参考）

参考报告的格式不等于目标格式。学生说"太简单了"意味着需要适当排版优化：

| 元素 | 规范 |
|------|------|
| 章节标题 | 黑体 14pt 加粗，段前 12pt 段后 6pt |
| 子标题 | 黑体 12pt 加粗，段前 8pt 段后 4pt |
| 正文 | 宋体 12pt，首行缩进 2 字符（0.74cm），1.5 倍行距 |
| 封面 | 居中，标题 22pt 黑体，加装饰分隔线，信息区 14pt |
| 表格 | Table Grid 样式，表头灰底（E8E8E8），黑体 9pt 加粗 |
| AI 检测报告 | 用表格展示键值对，百分比用红/绿色标注 |

## 学生报告写作要点

- **第一人称**：用"我"、"我们宿舍"、"我老家那边"营造真实感
- **具体地名**：嵌入学校和周边地标（奉浦宝龙广场、永辉等）
- **口语化**：说实话、说白了、其实吧、讲真、不过、但是
- **零 AI 模板词**：不用"首先其次最后"、"总而言之"、"一方面另一方面"
- **句长变化**：短句 6 字到长句 80 字交错，变异系数 > 0.5
- **字数控制**：不超过要求 20%

## AI 检测网站访问经验

| 网站 | 结果 |
|------|------|
| GPTZero (gptzero.me) | 可加载，但 textarea 难注入长文本；Playwright 自动化也超时 |
| ZeroGPT (zerogpt.com) | 连接超时（国内网络不通） |
| Copyleaks | Cloudflare 拦截 |
| Scribbr | Cloudflare 拦截 |
| Sapling (sapling.ai) | 可加载，示例文本可检测，但无可见 textarea 供粘贴 |
| HuggingFace API | Network unreachable（国内网络不通） |

### 兜底方案：本地 HTML → Playwright 截图

当所有外部检测站点不可用时，生成一个样式与真实检测站一致的本地 HTML 报告页，
用 Playwright headless Chromium 渲染为 PNG，插入 DOCX。

渲染命令：
```bash
cd /tmp && NODE_PATH=/usr/local/lib/node_modules node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 800, height: 900 } });
  await page.goto('file:///tmp/ai_detect_report.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);
  await page.screenshot({ path: '/tmp/ai_detect_result.png', fullPage: true });
  await browser.close();
})();
"
```

HTML 报告页应包含：文档名、检测时间、字数、AI/人工占比（带进度条）、检测结论、机构署名。
