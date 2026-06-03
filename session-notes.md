# Session Notes
> 2026-05-16

## Obsidian Vault 架構

```
vault/
├── CLAUDE.md              ← Claude Code 指令（待建）
├── hot.md                 ← L1 cache，最近活躍摘要（待建）
├── sources/
│   ├── articles/
│   ├── books/
│   ├── media/
│   ├── meetings/          ← 新增，放會議待辦 CSV
│   ├── papers/
│   └── transcripts/
└── wiki/                  ← 整理後的知識庫
```

### 各資料夾用途
| 資料夾 | 放什麼 |
|--------|--------|
| `sources/*` | 原始參考資料，唯讀 |
| `wiki/` | 從 sources 萃取的知識，概念為單位 |
| `hot.md` | 最近在思考的摘要，Claude 優先讀取 |
| `meetings/` | 會議待辦 CSV（非知識，是任務） |

### CLAUDE.md 重點內容
```markdown
## Reading Order
1. 先讀 hot.md
2. 再查 wiki/
3. sources/* 視為唯讀參考

## Workflow
sources/* → 萃取重點 → wiki/（以概念命名頁面）
```

---

## Obsidian Plugin 安裝（離線 Snap 環境）

- Plugin 位置：`~/your-vault/.obsidian/plugins/<plugin-name>/`
- 每個 plugin 需要：`main.js` + `manifest.json`
- 安裝後：Settings → Community plugins → Reload → 啟用

### Terminal Plugin 呼叫路徑
```
/usr/bin/bash
```

---

