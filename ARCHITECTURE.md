# AI圖書館 專案結構圖

```
library_system/
│
├── app.py                # Flask 主程式，所有路由與資料庫操作
├── requirements.txt      # Python 套件需求
├── .env                  # 環境變數（資料庫連線）
│
├── templates/            # 前端 HTML 樣板（Jinja2 + Bootstrap 5）
│   ├── base.html         # 主版型（含 navbar）
│   ├── books.html        # 書籍管理頁
│   ├── readers.html      # 讀者管理頁
│   ├── borrow.html       # 借書頁
│   ├── return.html       # 還書頁
│   ├── records.html      # 借閱紀錄頁
│   └── edit_book.html    # 書籍編輯頁
│
├── static/               # 靜態資源（CSS、圖片等）
│   └── style.css         # 自訂樣式（如有）
```

## 架構說明
- **app.py**：Flask 應用主體，負責路由、資料庫 CRUD、頁面渲染。
- **templates/**：所有前端頁面，採用 Jinja2 模板語法，並以 base.html 為共用主版。
- **static/**：靜態檔案資料夾，預設僅 style.css，可擴充放置圖片、JS 等。
- **.env**：儲存資料庫連線資訊，避免敏感資料寫死在程式碼。
- **requirements.txt**：專案所需 Python 套件清單。

---
如需擴充功能，建議依照 Flask Blueprint 或 MVC 分層設計進行模組化。
