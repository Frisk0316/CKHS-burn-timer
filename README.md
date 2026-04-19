# 建中有多少天沒有被炎上計時器

即時追蹤建國中學距離上次炎上已過了多久（精確到秒）。

**[→ 線上版本](https://frisk0316.github.io/CKHS-burn-timer/)**

---

## 功能

- 天 / 時 / 分 / 秒 即時計時
- 歷史炎上事件紀錄，附新聞與貼文來源連結
- **每日自動更新**：GitHub Actions 每天從 Google News RSS 搜尋相關報導，偵測到新炎上事件時自動重置計時器
- 炎上偵測來源快速搜尋連結（Threads、Google 新聞、PTT）

---

## 自動更新機制

```
每天 10:00（台灣時間）
  └─ GitHub Actions 執行 scripts/fetch_news.py
       ├─ 搜尋 Google News RSS（建中炎上、建中批評、privilege…等 10 組查詢）
       ├─ 過濾含關鍵字的文章，寫入 incidents.json → recent_news
       └─ 偵測到「炎上／道歉／撤展」等高信心度關鍵字
            └─ 自動更新 last_incident 日期，網頁計時器重置
```

若要手動新增事件，直接編輯 `incidents.json`，無需動 HTML。

---

## 本地執行

```bash
# 安裝依賴
pip install -r requirements.txt

# 手動執行一次新聞抓取
python scripts/fetch_news.py

# 本地預覽（需用 HTTP server，不能直接開 HTML 檔）
python -m http.server 8080
# 開啟 http://localhost:8080
```

---

## 部署到 GitHub Pages

```bash
git clone https://github.com/你的帳號/你的-repo.git
cd 你的-repo
# 複製本專案所有檔案進去

git add .
git commit -m "init"
git push -u origin main
```

接著到 **Settings → Pages → Branch: main / root → Save**，約 1 分鐘後上線。

GitHub Actions 會自動每天執行，無需額外設定（使用內建的 `GITHUB_TOKEN`）。

---

## 事件紀錄

| 日期 | 事件 |
|------|------|
| 2025-12-31 | 建中生 privilege 論述在 Threads 爆發，引爆特權量表風潮 |
| 2025-12-07 | 學生藝術展以 911 雙子星為素材，AIT 介入，校方撤展道歉 |
| 2024-12-28 | 麥當勞抵制風波期間，學生揪團去吃並 PO 網炎上 |
| 2024-12-26 | 校友會菜單出現不雅字眼，引爆性平爭議，索賠 13 萬 |

---

## 專案結構

```
├── index.html               # 前端頁面（從 incidents.json 動態載入資料）
├── incidents.json           # 資料來源：事件紀錄 + 自動抓取的新聞
├── scripts/
│   └── fetch_news.py        # 新聞抓取腳本
├── .github/
│   └── workflows/
│       └── update-news.yml  # 每日排程
└── requirements.txt
```

---

## 技術說明

- 純靜態前端（HTML + CSS + JS），資料由 `fetch('incidents.json')` 動態載入
- 字體：Google Fonts（Bebas Neue、Share Tech Mono、Noto Sans TC）
- 計時基準：台灣時間 UTC+8，每 500ms 更新
- 後端：GitHub Actions（免費額度內）+ Google News RSS（免費、無需 API key）

---

*本站僅作幽默統計用途　資料來源：Google News RSS、Threads、各大網路媒體*
