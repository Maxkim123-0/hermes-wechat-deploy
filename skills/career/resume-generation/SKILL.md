---
name: resume-generation
description: 简历生成、优化、模板搜索。从零生成或基于现有简历优化，支持HTML/PDF输出。
version: 1.0.0
triggers:
  - 写简历/改简历/优化简历
  - resume/CV/求职简历
  - 帮我看看简历/简历模板
  - 按xxx模板给yyy做一份/参考模板生成
---

# 简历生成与优化

## 用户画像（熊正阳）

- 上海商学院零售业管理大三（专升本），两年义务兵退伍
- 目标方向：连锁零售营运管培生 / 新零售私域运营 / 社区零售运营
- 证书：CET-4、计算机二级、普通话二甲、C1驾照
- 王牌经历：边防一线服役（连三等功×2）、瑞幸咖啡、拾光驿站创业策划、微信AI助手部署、闲鱼个人创业

## 排版铁律

1. 精简得体 — 每条经历2条bullet封顶，HR 30秒扫完能记住
2. 数据驱动 — 每条有数字，"甜品连带率29%（+11%）"比"提升约20%"强
3. 去AI味 — 不用首先其次最后，不要过度包装
4. 服役独立成段 — 王牌不能混在其他板块
5. 删不可验证的 — "专业排名前1%"删掉
6. 技能绑场景 — "用ChatGPT生成促销文案，AB测试转化率+19%"
7. 不相关的删 — 足球/数码评测跟零售无关就砍
8. 求职意向具体化 — 不能只写销售，要写具体岗位方向

## 工作流

### 1. 获取现有简历
有文件根据格式选工具：
- **PDF**: pymupdf（清华镜像安装 `pip3 install pymupdf -i https://pypi.tuna.tsinghua.edu.cn/simple`）
- **DOCX**: python-docx
- **.doc（旧格式）**: olefile — 读取 WordDocument stream，UTF-16LE 解码提取中文
  ```python
  import olefile, re
  ole = olefile.OleFileIO(filepath)
  data = ole.openstream("WordDocument").read()
  text = data.decode('utf-16-le', errors='ignore')
  text = re.sub(r'[^\u4e00-\u9fff\u3000-\u303f\uff00-\uffefa-zA-Z0-9\s.,;:!?()\-\n\r/+=@#%]', '', text)
  ```
- ⚠️ 微信传过来的 DOCX 可能编码异常（magic bytes `0231 4248`），python-docx 和 zipfile 都打不开。让用户传原始文件或截图。
- 纯文字都没有就基于已知信息从零生成。

### 2. 诊断
扫描：重复内容、缺数据、求职意向模糊、排版乱、无关信息、虚假数据。如用户提供了AI/HR的批改报告，提取有效建议融合进优化版——但不过度照搬（AI报告通常过于冗长，每条经历写5条bullet不像人写的）。

### 3. 优化
每条经历提炼2条核心bullet，补数据（连带率/转化率/NPS），合并同类项+去重，服役提到独立板块。适度模糊化AI报告中过于精确的数字（"6.2小时""89.4%"），保持可信度。

### 4. 模板
搜模板走 github-resource-discovery 技能。顶级模板：Awesome-CV(27k)、awesome-resume-for-chinese(7.6k)、resumejob/awesome-resume(7.2k)、NewFuture/CV(97)。

内置模板：
- `templates/resume.html` — 标准求职版（求职意向在前，传统结构）
- `templates/resume-academic-cn.html` — 曹静格式中文版（照片前置、经历优先、求职意向末尾）
- `templates/resume-academic-en.html` — 曹静格式英文版（同上，Georgia/Times New Roman字体）

### 5. 生成PDF
HTML+CSS 通过 Playwright page.pdf() 渲染A4，边距14/18mm。命令：
```bash
NODE_PATH=/usr/local/lib/node_modules node -e "
const { chromium } = require('playwright');
...
await page.pdf({ path: 'output.pdf', format: 'A4', margin: { top:'14mm',bottom:'14mm',left:'18mm',right:'18mm' }, printBackground: true });
"
```

## 简历结构变体

### 变体A：标准求职版（默认）
1. 头部（姓名/电话/邮箱/城市）
2. 求职意向（方向+薪资+到岗）
3. 教育背景（倒序，专升本标注）
4. 实习经历（2-4段，每段2条bullet）
5. 项目经历（2-3段）
6. 比赛经历（简写）
7. 服役经历（独立板块）
8. 技能证书+荣誉奖励（双栏）
9. 技能特长（一句带场景）

### 变体B：学术/高校教师版（曹静格式，照片+经历前置）
触发词：「按曹静格式」「照片放前面」「经历放前面」「求职意向放最后」
1. 个人信息（照片+姓名/年龄/电话/邮箱/城市，照片占位用 onerror 兜底显示"[照片]"）
2. 工作经历（AI/技术经历前置，基础岗放最后；每段2条bullet封顶）
3. 项目经历（2-3段）
4. 服役经历（独立板块）
5. 教育背景（倒序）
6. 技能证书+荣誉奖励（双栏，技术栈用 tag 样式）
7. 求职意向（末尾footer，灰色小字）

## 「给别人也做一份」模式

当用户要求"按XXX的模板给YYY也做一份"时：
1. 复制 HTML 模板结构，改头部信息
2. **内容全部重写** — 不照抄原版的数据、经历、项目，换不同的企业/品牌/场景
3. 保持相同板块顺序和排版样式
4. 同专业背景就换实习企业、比赛类型；不同背景就整体换方向
5. 生成完提醒用户核对替换的占位信息（手机号、邮箱等）

## 双语生成（中英文各一份）

触发词：「中英文各一份」「双语」「中文+英文」
1. 先生成中文版 HTML，确认内容无误
2. 复制结构翻译为英文版，保持相同板块顺序和样式
3. 英文版注意：服役经历译为 Military Service，三等功→Class III Merit，专升本→Top-up Degree
4. 两个 HTML 分别渲染 PDF，中文版用宋体/黑体，英文版用 Georgia/Times New Roman/Arial
5. 中文PDF因字体嵌入会明显比英文版大（800KB+ vs 60KB+），正常现象

## 生成PDF
HTML+CSS 通过 Playwright page.pdf() 渲染A4。模板文件：`templates/resume.html`。

已验证命令：
```bash
NODE_PATH=/usr/local/lib/node_modules node -e "
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const html = fs.readFileSync('input.html', 'utf-8');
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.pdf({
    path: 'output.pdf',
    format: 'A4',
    margin: { top: '14mm', bottom: '14mm', left: '18mm', right: '18mm' },
    printBackground: true
  });
  await browser.close();
})();
```

## 在微信上发送
前端对话中用 `MEDIA:/absolute/path/to/file.pdf` 发送文件。生成后 git push 到 `Maxkim123-0/hermes-wechat-deploy/resumes/` 备份。

## 增量修改模式

用户发回新版PDF让你"再改"时：
1. pymupdf 读PDF确认当前版本内容
2. 用 patch 工具直接改 HTML 模板（别重新写整个文件），每次只改变动部分
3. 改完重新 `page.pdf()` 渲染
4. 每次渲染后 git commit + push，累积修改可追溯

常见增量修改触发词：
- "把实习经历改为XXX" → 替换整个实习板块
- "教育背景改成..." → 替换教育板块
- "比赛经历改成..." → 替换比赛板块
- "荣誉奖励改成..." → 替换荣誉板块
- "技能证书改成..." → 替换证书板块
- "薪资改成XXX" → patch 中文「期望薪资」+ 英文「Salary Expectation」，改完重新渲染PDF

每次只改用户指定的板块，不动其他内容。

## 常见坑
- 每条超3条bullet → HR不看
- 没数字 → 像编的
- 求职意向只写销售 → 太泛
- 5条超长AI式bullet → 精简到2条
- 生涯规划写进简历 → 不属于简历
- 给别人做简历别照抄原版数据 → 内容全部重写，只保留模板骨架
- Playwright pdf() 边距单位是字符串 '14mm' 不是数字
- 增量修改用 patch 而不是重写整个 HTML → 避免引入新错
- 用户说的品牌名可能不标准（"中薛高"→ 钟薛高），按正确写法但要提醒用户确认
- 照片占位：`<img src="photo.jpg" onerror="this.parentNode.innerHTML='[照片]'"/>` — 用户还没给照片时也能正常渲染PDF，之后替换 photo.jpg 即可
- 🔴 **照片嵌入PDF必须用 base64 data URI**，不能直接用 `src="photo.jpg"` — Playwright 渲染上下文没有当前目录的文件访问权限，`file://` 路径也无效。正确做法：`import base64; b64 = base64.b64encode(open('photo.jpg','rb').read()).decode(); html.replace('src="photo.jpg"', f'src="data:image/jpeg;base64,{b64}"')`
- 旧 .doc 文件用 olefile 读 WordDocument stream，别死磕 python-docx（只支持 .docx）
- 「薪资改成XXX」→ 增量修改触发词，patch 两处（中文版期望薪资 + 英文版 Salary Expectation），然后重新渲染 PDF
