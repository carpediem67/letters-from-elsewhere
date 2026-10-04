# 美西手帐示例

[在线翻阅](https://carpediem67.github.io/letters-from-elsewhere/) · [制作过程](PROCESS.md) · [来源](SOURCES.md) · [验证范围](VALIDATION.md)

15 张公开摄影、6 枚照片衍生贴纸、15 页手帐。根目录 `docs/pages/` 保留全部 1200 × 1600 PNG；`source/` 保留实际排版程序、照片阅读副本、纸纹与字体；贴纸程序引用 `docs/process/` 中的同一 PNG。原始高分辨率摄影通过 `sources.json` 的详情页查看，不在仓库另建原片图库。

## 修改与重建

需要 Python 3.11+、Node.js 与 Playwright 的 Chromium。以下在仓库根目录运行；浏览器依赖仅用于重新导出示例，不是翻阅器运行依赖。

```bash
python3 examples/western/source/compose.py
npm install --no-save playwright
npx playwright install chromium
node examples/western/render_pages.cjs
python3 scripts/build_scrapbook.py docs/pages \
  --output output/journal.html \
  --title '美西 · 把风贴进本子里' \
  --credits examples/western/credits.json
```

改文字与构图：编辑 `source/compose.py`，再渲染；改摄影和贴纸：检查来源、许可与完整轮廓，再替换相应输入。首次重渲染的 Chromium 与字体版本不同可能带来细小像素差异；重新审阅全页，不把代码运行成功当作视觉通过。

提示词记录中的 `originals/<key>.jpg` 是制作时的逻辑输入名，不是本仓库的文件；可按来源页获取原片后使用，不要用低分辨率过程缩略图声称精确编辑。
