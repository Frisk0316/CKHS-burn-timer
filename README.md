# 🔥 建中有多少天沒有被炎上計時器

> 即時追蹤建國中學距離上次炎上已過了多久（精確到秒）

## 網站預覽

計時器會顯示：
- **天 / 時 / 分 / 秒** 四格計時
- 最近一次炎上的日期與事件說明
- 歷史炎上事件紀錄
- **炎上偵測來源**：Threads 搜尋連結（建中炎上、建中生 privilege、建中批評）、Google 新聞、PTT CKSH 版

---

## 🚀 部署到 GitHub Pages（五分鐘完成）

### 方法一：直接上傳（最簡單）

1. 前往 [github.com](https://github.com) 並登入
2. 點右上角 **「+」→「New repository」**
3. 填入 Repository name，例如 `cksh-timer`
4. 選 **Public**，其他預設即可，點 **「Create repository」**
5. 在新頁面點 **「uploading an existing file」**
6. 把 `index.html` 拖曳上去，然後按 **「Commit changes」**
7. 前往 **Settings → Pages**（左側選單）
8. Branch 選 `main`，資料夾選 `/ (root)`，按 **Save**
9. 等約 1 分鐘，網址就會出現在頁面上：

```
https://你的帳號.github.io/cksh-timer/
```

### 方法二：用 Git 指令

```bash
git init
git add index.html
git commit -m "init: 建中炎上計時器"
git remote add origin https://github.com/你的帳號/cksh-timer.git
git push -u origin main
# 然後到 Settings → Pages 開啟即可
```

---

## 🗓️ 更新炎上日期

當建中又發生新的炎上事件，打開 `index.html`，找到這一行：

```js
const LAST_INCIDENT = new Date('2025-12-07T00:00:00+08:00').getTime();
```

把日期改成新的炎上日期（格式：`YYYY-MM-DDT00:00:00+08:00`），然後 commit 即可。

同時在 HTML 裡的 `<!-- Incident log -->` 區段新增一條紀錄。

---

## 📋 目前事件紀錄

| 日期 | 事件 |
|------|------|
| 2025-12-07 | 學生以911雙子星為藝術素材，AIT介入，校方撤展道歉 |
| 2024-12-28 | 麥當勞抵制風波期間，學生揪團去吃並PO網炎上 |
| 2024-12-26 | 校友會菜單出現不雅字眼，引爆性平爭議 |
| 持續中 | 「建中生 privilege」論述：Threads 週期性出現批評建中生精英意識貼文 |

---

## 技術說明

- 純靜態 HTML + CSS + JS，無任何後端
- 字體使用 Google Fonts（Bebas Neue + Share Tech Mono + Noto Sans TC）
- 計時基準為台灣時間 UTC+8
- 每 500ms 更新一次，秒數跳動時有閃爍動畫

---

*資料來源：Threads 社群搜尋、CTWANT、Newtalk、自由時報等各大網路媒體、PTT CKSH 版｜本站僅作幽默統計用途*
