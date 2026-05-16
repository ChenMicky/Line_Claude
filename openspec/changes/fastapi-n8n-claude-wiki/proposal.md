## Why

需要一個中間層服務，讓 n8n 工作流程能透過 webhook 傳送資料，並利用專案內 Claude_wiki 的 Obsidian 筆記內容作為上下文，呼叫 Claude API 進行智能處理與回應。

## What Changes

- 新增 FastAPI 應用程式，提供 n8n webhook 接收端點
- 整合 Claude API 呼叫功能，支援將 Obsidian wiki 內容作為知識庫上下文
- 實作 Obsidian 筆記讀取與處理邏輯，載入 Claude_wiki 資料夾內的 markdown 檔案
- 新增環境變數配置，管理 API 金鑰與服務參數
- **新增 Docker 容器化配置**，將 FastAPI 應用程式封裝在 Docker 容器內運行

## Capabilities

### New Capabilities
- `n8n-webhook-api`: 提供 FastAPI webhook 端點接收 n8n 傳送的資料
- `claude-api-integration`: 整合 Claude API 呼叫，並將 Obsidian wiki 內容作為上下文傳入
- `obsidian-wiki-loader`: 讀取、解析與載入 Claude_wiki 資料夾內的 Obsidian markdown 筆記
- `docker-containerization`: 將 FastAPI 應用程式容器化，使用 Docker 部署與運行

### Modified Capabilities

（無，此為新專案）

## Impact

- 新增 FastAPI 相關依賴 (fastapi, uvicorn, httpx)
- 新增 Anthropic SDK 依賴 (anthropic)
- 新增環境變數配置檔 (.env)
- 新增 Docker 相關檔案 (Dockerfile, docker-compose.yml, .dockerignore)
- 影響範圍：新增 `app/` 目錄結構，包含 API 路由、Claude 整合、wiki 載入器等模組
- 影響範圍：Docker 容器將 Claude_wiki 資料夾掛載為 volume，讓容器內的應用程式能存取 Obsidian 筆記
