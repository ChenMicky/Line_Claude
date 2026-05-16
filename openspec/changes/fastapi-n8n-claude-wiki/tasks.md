## 1. 專案基礎設置

- [x] 1.1 建立專案目錄結構 (app/, app/routers/, app/services/, app/core/)
- [x] 1.2 建立 requirements.txt 檔案，包含 fastapi, uvicorn, anthropic, python-dotenv, httpx 依賴
- [x] 1.3 建立 .env.example 檔案，包含 ANTHROPIC_API_KEY, WIKI_PATH, PORT 等環境變數範本
- [x] 1.4 建立 app/__init__.py 與主應用程式入口點 app/main.py

## 2. Obsidian Wiki 載入器實作

- [x] 2.1 實作 app/services/wiki_loader.py：掃描 Claude_wiki 資料夾並讀取所有 .md 檔案
- [x] 2.2 實作遞迴掃描子目錄功能，確保所有巢狀子目錄的 .md 檔案都被讀取
- [x] 2.3 實作環境變數 WIKI_PATH 配置，支援預設路徑與自訂路徑
- [x] 2.4 加入錯誤處理：資料夾不存在或無 .md 檔案時的日誌記錄

## 3. Claude API 整合實作

- [x] 3.1 實作 app/services/claude_client.py：初始化 Anthropic SDK 並設定 API 金鑰
- [x] 3.2 實作將 wiki 內容整合到 system prompt 的邏輯
- [x] 3.3 實作呼叫 Claude API 並處理回應的函式
- [x] 3.4 加入錯誤處理：API 金鑰未設定、API 呼叫失敗、token 限制等異常情況

## 4. FastAPI Webhook 端點實作

- [x] 4.1 實作 app/routers/webhook.py：建立 POST /webhook/n8n 端點
- [x] 4.2 定義 Pydantic 請求模型，包含必要欄位（如 message）與選填欄位
- [x] 4.3 實作請求驗證與錯誤回應（HTTP 422 處理）
- [x] 4.4 實作 GET /health 健康檢查端點
- [x] 4.5 設定 Swagger UI 與 ReDoc 自動文件生成（FastAPI 內建功能）

## 5. Docker 容器化配置

- [x] 5.1 建立 Dockerfile：使用 python:3.12-slim 基礎映像，安裝依賴，設定啟動命令
- [x] 5.2 建立 .dockerignore 檔案，排除不必要的檔案（如 __pycache__, .git 等）
- [x] 5.3 建立 docker-compose.yml：設定服務、端口映射（8000:8000）、volume 掛載（Claude_wiki）、環境變數
- [x] 5.4 測試 Docker 構建與啟動，確認容器能正確讀取 wiki 內容與環境變數

## 6. 測試與驗證

- [x] 6.1 透過 Swagger UI (/docs) 測試 webhook 端點，驗證請求處理與回應
- [x] 6.2 使用 curl 或 httpx 發送測試請求到 /webhook/n8n，驗證完整流程
- [x] 6.3 測試錯誤情境：無效請求格式、API 金鑰未設定、wiki 資料夾不存在
- [x] 6.4 驗證 Docker 容器內的 Swagger UI 可正常存取與測試
