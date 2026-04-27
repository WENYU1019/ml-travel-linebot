# trip_bot 使用手冊

`trip_bot` 是一個以 LINE Bot 為入口的聚餐與出遊輔助系統。使用者在 LINE 群組中討論時間、地點、人數、預算或候選方案時，Bot 會分析對話內容，判斷是否需要介入，並回覆適合的建議。

本專案是單一專案結構，主體為根目錄的 `app.py`，其他第一層資料夾都是支援 `app.py` 的功能模組。

## 專案目的

- 協助群組判斷聚餐或出遊討論進度。
- 擷取對話中的時間、地點、人數、預算、限制條件與候選選項。
- 判斷 AI 是否應該介入，避免過度打斷自然討論。
- 優先使用 Groq LLM 做情境判斷。
- 當 LLM 或 API key 不可用時，改用規則式 fallback。
- 產生 LINE Bot 可直接回覆的建議文字。

## 使用者流程

```text
LINE 群組對話
    |
    v
LINE Messaging API webhook
    |
    v
app.py 接收 /callback
    |
    v
analysis.engine.analyze_dialogue(text)
    |
    +--> extraction/ 擷取關鍵資訊
    +--> analysis/ 判斷情境與是否介入
    +--> data/ 提供資料模型與情境知識庫
    |
    v
回傳 AnalysisResult
    |
    v
app.py 依結果回覆 LINE
```

## 專案內容

- `app.py`：LINE Bot 啟動與 webhook 主程式。
- `analysis/`：對話分析、LLM 判斷、fallback 規則分類。
- `extraction/`：從群組對話擷取時間、地點、人數、預算與限制條件。
- `data/`：資料模型、情境知識庫與 CSV 測試資料。
- `interfaces/`：CLI 測試入口與 LINE Bot 整合範例。
- `tests_TODO/`：待整理的手動測試案例。
- `fronted/`：網頁展示或前端相關檔案。
- `docx/`：研究、會議、專案文件、研討會資料與劇本文件。
- `venv/`：專案唯一 Python 虛擬環境。
- `.env.example`：環境變數範例。
- `.env`：本機金鑰設定檔，不可上傳。
- `requirements.txt`：Python 套件需求。

## 主要 API

### LINE Messaging API

用途：

- 接收 LINE 群組或使用者訊息。
- 驗證 webhook 簽章。
- 使用 reply token 回覆訊息。

需要的環境變數：

```env
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret
```

官方文件：

- https://developers.line.biz/en/docs/messaging-api/getting-started/
- https://developers.line.biz/en/docs/basics/channel-access-token/

### Groq API

用途：

- 使用 LLM 進行情境判斷。
- 產生結構化分析結果。
- 提供 `suggested_reply` 給 LINE Bot 回覆。

需要的環境變數：

```env
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

官方文件：

- https://console.groq.com/keys
- https://console.groq.com/docs/api-reference

## 快速啟動

```powershell
venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

啟動後可使用：

- `GET /`：健康檢查。
- `POST /callback`：LINE webhook。

本機測試 LINE webhook 時，需要使用 ngrok、Cloudflare Tunnel 或其他 HTTPS tunnel，將公開網址填入 LINE Developers Console，例如：

```text
https://your-domain.example/callback
```

## 文件導覽

- `README.md`：使用手冊，說明專案內容、目的、API 與快速啟動。
- `組員操作手冊.md`：組員開發環境、上傳方式、上傳規範與協作規則。
- `程式說明手冊.md`：程式流程、資料夾結構、核心函式調用方式與維護方式。
