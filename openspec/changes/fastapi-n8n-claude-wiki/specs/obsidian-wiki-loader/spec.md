## ADDED Requirements

### Requirement: 載入 Obsidian wiki 筆記
系統 SHALL 在啟動時掃描 Claude_wiki 資料夾，讀取所有 .md 檔案並儲存其內容。

#### Scenario: 成功載入 wiki 檔案
- **WHEN** 系統啟動且 Claude_wiki 資料夾存在並包含 .md 檔案
- **THEN** 系統 SHALL 讀取所有 .md 檔案內容，並將其儲存在記憶體中供後續使用

#### Scenario: Claude_wiki 資料夾不存在
- **WHEN** 系統啟動但指定的 Claude_wiki 資料夾路徑不存在
- **THEN** 系統 SHALL 記錄警告日誌，並使用空的 wiki 內容繼續執行

#### Scenario: 資料夾內無 .md 檔案
- **WHEN** Claude_wiki 資料夾存在但沒有 .md 檔案
- **THEN** 系統 SHALL 記錄資訊日誌，並使用空的 wiki 內容繼續執行

### Requirement: 支援 wiki 資料夾路徑配置
系統 SHALL 透過環境變數 WIKI_PATH 設定 Claude_wiki 資料夾的路徑。

#### Scenario: 使用預設路徑
- **WHEN** 環境變數 WIKI_PATH 未設定
- **THEN** 系統 SHALL 使用預設路徑 "./Claude_wiki"

#### Scenario: 使用自訂路徑
- **WHEN** 環境變數 WIKI_PATH 設定為自訂路徑
- **THEN** 系統 SHALL 使用該路徑作為 wiki 資料夾位置

### Requirement: 遞迴掃描子目錄
系統 SHALL 遞迴掃描 Claude_wiki 資料夾及其所有子目錄中的 .md 檔案。

#### Scenario: 掃描巢狀子目錄
- **WHEN** Claude_wiki 資料夾包含多層子目錄且有 .md 檔案
- **THEN** 系統 SHALL 找到並讀取所有子目錄中的 .md 檔案
