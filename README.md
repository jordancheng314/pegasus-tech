# 飛馬先進科技官方網站

PEGASUS ADVANCE TECHNOLOGY LTD. 官方靜態網站，可直接部署至 GitHub Pages。

## 本機預覽

用瀏覽器直接開啟 `index.html`，或在此資料夾執行：

```bash
# Python
python -m http.server 8080

# Node
npx serve .
```

然後開啟 `http://localhost:8080`。

## 部署到 GitHub Pages

### 方式 A：整個 `website` 資料夾獨立成 Repo（建議）

1. 在 GitHub 建立新 Repository（例如 `pegasus-tech-website`）
2. 將本資料夾內容推上 GitHub：

```bash
cd website
git init
git add .
git commit -m "Add Pegasus official website"
git branch -M main
git remote add origin https://github.com/<你的帳號>/<repo名稱>.git
git push -u origin main
```

3. 到 GitHub → **Settings** → **Pages**
4. **Source** 選擇 `Deploy from a branch`
5. Branch 選 `main`，資料夾選 `/ (root)` → Save
6. 數分鐘後即可用：
   `https://<你的帳號>.github.io/<repo名稱>/`

### 方式 B：放在現有 Repo 的 `/docs`

1. 將本資料夾重新命名或複製為 Repo 根目錄下的 `docs`
2. GitHub Pages Source 選擇 `main` + `/docs`

## 頁面結構

| 檔案 | 說明 |
|------|------|
| `index.html` | 首頁（含輪播） |
| `about.html` | 關於我們 |
| `services.html` | 營業項目 |
| `contact.html` | 聯絡我們 |
| `css/style.css` | 樣式 |
| `js/main.js` | 下拉選單與輪播 |

## 公司資訊來源

- [飛馬先進科技部落格](https://pegasus-tech.blogspot.com/)
- 經濟部商工登記公開資料（統編 54757538）
