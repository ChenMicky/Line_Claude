## ADDED Requirements

### Requirement: 接收 n8n webhook 請求
系統 SHALL 提供 POST /webhook/n8n 端點，接收來自 n8n 的 HTTP 請求。

#### Scenario: 成功接收 n8n 資料
- **WHEN** n8n 發送 POST 請求到 /webhook/n8n，包含有效的 JSON payload
- **THEN** 系統 SHALL 回傳 HTTP 200 狀態碼，並回傳包含處理結果的 JSON 回應

#### Scenario: 接收無效資料格式
- **WHEN** n8n 發送非 JSON 格式的請求到 /webhook/n8n
- **THEN** 系統 SHALL 回傳 HTTP 422 狀態碼，並回傳錯誤訊息

#### Scenario: Swagger UI 測試 webhook 端點
- **WHEN** 開發者透過 Swagger UI (/docs) 發送測試請求到 /webhook/n8n
- **THEN** 系統 SHALL 正確處理請求並在 Swagger UI 中顯示回應結果

### Requirement: 請求資料驗證
系統 SHALL 使用 Pydantic 模型驗證 n8n 傳入的請求資料結構。

#### Scenario: 驗證必要欄位
- **WHEN** n8n 發送缺少必要欄位的請求
- **THEN** 系統 SHALL 回傳 HTTP 422 狀態碼，並列出缺少的欄位

#### Scenario: 驗證選填欄位
- **WHEN** n8n 發送包含選填欄位的請求
- **THEN** 系統 SHALL 正確解析並使用這些欄位值

### Requirement: 健康檢查端點
系統 SHALL 提供 GET /health 端點，供 n8n 或監控系統檢查服務狀態。

#### Scenario: 健康檢查回應
- **WHEN** 發送 GET 請求到 /health
- **THEN** 系統 SHALL 回傳 HTTP 200 狀態碼，並回傳 {"status": "healthy"}
