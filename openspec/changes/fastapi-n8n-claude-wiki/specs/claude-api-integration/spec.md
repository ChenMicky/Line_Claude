## ADDED Requirements

### Requirement: 呼叫 Claude API 處理請求
系統 SHALL 接收使用者輸入後，將 Claude_wiki 內容作為上下文，呼叫 Claude API 生成回應。

#### Scenario: 成功呼叫 Claude API
- **WHEN** 系統收到 n8n webhook 請求，且 Claude API 設定正確
- **THEN** 系統 SHALL 將 wiki 內容與使用者輸入合併為 prompt，呼叫 Claude API，並回傳生成的回應

#### Scenario: Claude API 金鑰未設定
- **WHEN** 系統嘗試呼叫 Claude API 但 ANTHROPIC_API_KEY 環境變數未設定
- **THEN** 系統 SHALL 回傳 HTTP 500 狀態碼，並回傳錯誤訊息指示 API 金鑰未設定

#### Scenario: Claude API 呼叫失敗
- **WHEN** Claude API 回傳錯誤（如 rate limit、invalid request）
- **THEN** 系統 SHALL 捕獲異常並回傳適當的 HTTP 錯誤碼與錯誤訊息

### Requirement: 將 Obsidian wiki 內容作為上下文
系統 SHALL 將載入的 Obsidian wiki 筆記內容作為系統提示詞（system prompt）傳遞給 Claude API。

#### Scenario: Wiki 內容整合到 prompt
- **WHEN** 系統準備呼叫 Claude API
- **THEN** 系統 SHALL 將所有 wiki 筆記內容前置到使用者訊息之前，作為上下文參考

#### Scenario: Wiki 內容過大處理
- **WHEN** wiki 內容總字數超過 Claude API 的 token 限制
- **THEN** 系統 SHALL 記錄警告日誌，並嘗試截斷或摘要 wiki 內容以符合限制

### Requirement: Swagger UI 測試 Claude API 整合
系統 SHALL 提供透過 Swagger UI 測試 webhook 端點的功能，驗證 Claude API 整合是否正常。

#### Scenario: 透過 Swagger 測試完整流程
- **WHEN** 開發者在 Swagger UI 中發送包含測試訊息的請求
- **THEN** 系統 SHALL 執行完整流程（載入 wiki、呼叫 Claude API、回傳結果），並在 Swagger UI 中顯示完整回應
