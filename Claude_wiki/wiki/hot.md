
---
Description
新 session開始時,先讀這個文件就能知道上次進度,無需重新解釋背景即可接續工作。當結束對話時,把本次進展內容更新寫入此文件,並保持500字內。

# [[Hot Status]]

**建立日期：** 2026-05-03  
**更新頻率：** 每個 session 結束時自動更新

## 🔥 最近狀態壓縮

- **專案狀態：** 維基百科系統架構已建立，LLM Wiki 架構與規範準備就緒
- **核心目標：** 維護 compounding knowledge base，每次對話產出的重要進展都累積在 wiki 中
- **文件規範：** YAML frontmatter + wikilink `[[Entity]]` 格式，跨參考第一等公民
- **目錄結構：**
  - `Raw/`：不可變原始文件（唯讀）
  - `wiki/`：LLM 維護的知識庫（overview、index、log、entities、concepts、sources、archive）
  - `CLAUDE.md`：可協同演進的規範文件

## 📋 已知實體與概念

- **LLM Wiki Schema** - 維基維護規範與工作流程
- **Hot Cache** - Python 快取機制（50 pages, 10min TTL）
- **Compounding Knowledge** - 知識累積原則

## 🎯 下一步建議

- 確定首次資料 ingest 的來源
- 建立初始 overview.md 綜觀頁面
- 設定定期 lint 流程

## 📝 Session 歷史

- **2026-05-03** - 建立 hot.md 狀態追蹤機制，確認 Wiki 架構規範
