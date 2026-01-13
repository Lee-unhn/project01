# Basic TensorFlow Model Inference Example

## 專案總覽

這是一個極簡的 Python 腳本，旨在展示如何載入一個預先訓練好的 TensorFlow/Keras `SavedModel` 模型，並使用它對來自攝影機的即時影像進行分類。

---

## 功能

*   **模型載入**: 載入一個 TensorFlow `SavedModel` 格式的模型。
*   **影像擷取**: 使用 OpenCV 從預設的攝影機獲取即時影像串流。
*   **影像預處理**: 對每一幀影像進行必要的預處理，包括調整大小 (224x224) 和標準化 (-1 到 1 的範圍)，以符合 Teachable Machine 導出的模型輸入要求。
*   **即時推論**: 對預處理後的影像進行預測。
*   **結果顯示**:
    *   在 OpenCV 視窗的畫面上即時顯示預測的標籤和對應的可信度分數。
    *   在命令列 (console) 中同步印出預測結果，方便偵錯。

---

## 專案目的

此腳本的主要目的是作為一個基礎範例，用於快速測試 `converted_keras` 模型是否能正常運作，並理解其基本的輸入輸出流程。它不包含複雜的 UI 或邏輯，只專注於核心的模型推論過程。

---

## 環境設置與執行

### 1. 前置條件
*   Python 3.8 或更高版本。
*   已連接的電腦攝影機。
*   `converted_keras` 模型資料夾需放置於 `C:\Users\user\AI\GitHub\project01\Ai-project-LEE\` 路徑下（此為程式碼中的硬編碼路徑）。

### 2. 安裝依賴
本專案所需的套件包含：
*   `tensorflow`
*   `opencv-python`
*   `numpy`

您可以透過 `pip` 逐一安裝：
```bash
pip install tensorflow opencv-python numpy
```

### 3. 執行腳本
在 `Example` 資料夾下，執行以下指令：
```bash
python camera_stream.py
```
程式會開啟一個顯示攝影機畫面的視窗，並在左上角顯示預測結果。在命令列視窗按下 `q` 鍵可關閉程式。
