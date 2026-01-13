# 剪刀石頭布 AI 遊戲

這是一個使用 Python 開發的桌面應用程式，您可以透過攝影機即時出拳，與 AI 進行一場剪刀石頭布的對決。

專案結合了電腦視覺模型、遊戲邏輯和現代化的圖形使用者介面(GUI)，提供流暢的互動體驗。

## ✨ 功能亮點

- **即時手勢辨識**: 透過攝影機捕捉您的手勢（剪刀、石頭、布）。
- **AI 對手**: 一個簡單的 AI 會隨機出拳與您對戰。
- **Modern UI**: 使用 CustomTkinter 打造美觀且現代化的使用者介面。
- **即時反饋**: 介面會即時顯示攝影機畫面、您的出拳、AI 的出拳以及每一局的勝負結果。

## 📂 專案架構概覽

```
rock_paper_scissors_app/
├── models/
│   └── keras_model.h5      # Keras/TensorFlow 模型檔案
├── ui/
│   └── app.py            # CTk UI 主程式碼與應用程式進入點
├── game_logic/
│   └── rps_game.py       # 剪刀石頭布遊戲核心邏輯 (勝負判斷、分數計算)
├── camera_utils/
│   └── camera_stream.py  # 處理攝影機串流、影像擷取與預處理
├── requirements.txt      # 專案依賴庫
└── README.md             # 專案說明
```

## 🚀 環境設置與安裝

**1. 克隆專案**
```bash
git clone <your-repo-url>
cd rock_paper_scissors_app
```

**2. 建立並啟用虛擬環境 (建議)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. 安裝依賴套件**

本專案需要以下主要套件，您可以透過 `requirements.txt` 一次性安裝：
```bash
pip install -r requirements.txt
```
主要的依賴包含：
- `customtkinter`
- `opencv-python`
- `tensorflow` (或 `tflite-runtime`，取決於您的模型)
- `Pillow` (PIL)

**4. 下載模型**

請將您訓練好的手勢辨識模型 (例如 `keras_model.h5` 或 `converted_keras.zip` 解壓縮後的檔案) 放置在 `models/` 資料夾中。

## ▶️ 如何執行

確保您的攝影機已連接並正常運作。然後執行 UI 應用程式：

```bash
python ui/app.py
```

程式啟動後，畫面上會顯示攝影機的即時影像。

## 🎮 遊戲玩法

1. 將您的手（握拳代表石頭、五指張開代表布、兩指伸出代表剪刀）放在攝影機前。
2. 應用程式會辨識您的手勢並顯示在畫面上。
3. AI 會同時做出它的選擇。
4. 每一局的結果（贏、輸、平手）會顯示在畫面上方。

---
祝您遊戲愉快！
