## Context

本專案需要建立一個 FastAPI 應用程式，作為 n8n 工作流程與 Claude API 之間的中間層服務。應用程式需要：
- 接收來自 n8n 的 webhook HTTP 請求
- 讀取專案內 Claude_wiki 資料夾的 Obsidian markdown 筆記作為知識庫
- 將 wiki 內容作為上下文，呼叫 Claude API 進行智能處理
- 使用 Docker 容器化部署，方便在不同環境運行
- 提供 Swagger UI 讓開發者可以測試 API 端點

目前專案中沒有現有的 API 服務，這是一個全新建立的服務。

## Goals / Non-Goals

**Goals:**
- 建立 FastAPI 應用程式，提供 webhook 端點接收 n8n 資料
- 實作 Obsidian wiki 載入器，讀取 Claude_wiki 資料夾內的 markdown 檔案
- 整合 Anthropic Claude API，將 wiki 內容作為上下文傳入
- 使用 Docker 容器化 FastAPI 應用程式
- 透過 volume 掛載方式，讓容器內應用程式能存取 Claude_wiki 內容
- **提供 Swagger UI (/docs) 與 ReDoc (/redoc) 自動生成的 API 文件與測試介面**

**Non-Goals:**
- 不實作使用者介面 (UI)
- 不實作身份驗證機制 (可於後續版本加入)
- 不建立資料庫儲存 (直接使用檔案系統讀取 wiki)
- 不實作 wiki 內容的自動同步或監聽 (使用 Docker volume 掛載即可)

## Decisions

### 1. 使用 FastAPI 作為 web 框架
**選擇**: FastAPI
**理由**: FastAPI 提供原生 async 支援、自動生成 OpenAPI 文件（Swagger UI 與 ReDoc）、驗證機制 (Pydantic)，適合建立輕量級 API 服務。
**替代方案**: Flask (較輕量但缺少 async 支援與自動文件生成)、Django (過於重量級)

### 2. 使用 Anthropic Python SDK 呼叫 Claude API
**選擇**: anthropic Python SDK
**理由**: 官方 SDK 提供完整的 API 支援，包含 streaming、tool use 等功能，且維護良好。
**替代方案**: 直接使用 httpx 呼叫 REST API (需要自行處理更多細節)

### 3. Docker 容器化策略
**選擇**: 使用 python:3.12-slim 作為基礎映像，透過 volume 掛載 Claude_wiki 資料夾
**理由**:
- slim 映像體積小，適合生產環境
- Volume 掛載讓 wiki 內容可以在不重建映像的情況下更新
- 使用 docker-compose 簡化部署流程

**替代方案**: 將 wiki 內容複製到映像內 (不利於內容更新)

### 4. Obsidian wiki 載入方式
**選擇**: 啟動時掃描 Claude_wiki 資料夾，載入所有 .md 檔案內容到記憶體
**理由**: 簡單直接，適合中小規模的 wiki (數百到數千個筆記)
**替代方案**: 使用向量資料庫 (如 ChromaDB) 建立語意搜尋 (過於複雜，非當前需求)

### 5. 環境變數管理
**選擇**: 使用 python-dotenv 讀取 .env 檔案
**理由**: 簡單且廣泛使用，適合管理 API 金鑰與服務配置

### 6. Swagger UI 與 API 測試
**選擇**: 使用 FastAPI 內建的 Swagger UI (/docs) 與 ReDoc (/redoc)
**理由**:
- FastAPI 自動根據 Pydantic 模型與路徑操作生成 OpenAPI 規範
- Swagger UI 提供互動式 API 測試介面，開發者可以直接在瀏覽器測試 webhook 端點
- 不需要額外配置或依賴
- 支援請求/回應模型的視覺化與驗證

**替代方案**: 使用 Postman 或 Insomnia 等外部工具 (需要手動配置，不如內建方便)

## Risks / Trade-offs

- **[Wiki 載入效能]** → 若 Claude_wiki 內容過大 (數千個檔案)，啟動時載入可能較慢。緩解方式：實作懶載入或快取機制。
- **[Claude API 費用]** → 每次請求都會將 wiki 內容作為上下文，可能消耗大量 tokens。緩解方式：限制上下文大小，或實作相關性篩選。
- **[Webhook 安全性]** → 目前沒有驗證機制，任何知道端點的人都可以呼叫。緩解方式：後續可加入 API key 驗證。
- **[Docker volume 權限]** → macOS/Windows 上掛載 volume 可能有權限問題。緩解方式：確保容器內使用者權限正確配置。
- **[Swagger 暴露]** → Swagger UI 在生產環境可能暴露 API 細節。緩解方式：生產環境可考慮透過環境變數控制是否啟用 Swagger 文件。
