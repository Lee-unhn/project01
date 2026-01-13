# AI Concept App - Real-time Gesture Recognition

## 專案總覽

這是一個使用 CustomTkinter 開發的桌面應用程式，它利用 TensorFlow/Keras 模型，透過電腦攝影機實現即時手勢辨識。應用程式著重於提供一個現代化且反應靈敏的使用者介面，以視覺化方式呈現 AI 模型的預測結果。

---

## 主要功能

*   **現代化使用者介面 (Modern UI)**: 使用 CustomTkinter 框架打造美觀的深色主題介面。
*   **即時影像串流**: 在 UI 中無縫顯示來自攝影機的即時畫面。
*   **即時手勢預測**: 利用 TensorFlow 模型對影像幀進行即時推論，辨識手勢。
*   **穩定的預測邏輯**: 只有當模型連續多次輸出相同預測結果時，才將其視為「穩定預測」，有效過濾掉因手勢變化或模型不確定性造成的結果閃爍。
*   **視覺化回饋**:
    *   **可信度條**: 以進度條的形式直觀顯示當前預測的可信度分數。
    *   **狀態指示器**: 一個圓形的指示燈，會根據應用程式的狀態（待機、偵測中、鎖定）改變顏色和文字，提供清晰的狀態回饋。

---

## 專案架構

本專案為單一腳本應用程式，其核心邏輯皆包含在 `app.py` 中：

*   **UI 層**: 使用 `customtkinter` 建立視窗、框架、標籤和進度條。
*   **影像處理層**: 使用 `OpenCV` 捕捉和處理攝影機影像。
*   **模型推論層**: 使用 `TensorFlow` 載入預先訓練的 Keras `SavedModel`，並在獨立的執行緒中進行預測，以避免 UI 阻塞。
*   **狀態管理**: 透過 `deque` 結構來追蹤預測歷史，實現穩定預測的判斷邏輯。

---

## 環境設置與執行

### 1. 前置條件
*   Python 3.8 或更高版本。
*   已連接的電腦攝影機。
*   `converted_keras` 模型資料夾需放置於 `C:\Users\user\AI\GitHub\project01\Ai-project-LEE\` 路徑下（此為程式碼中的硬編碼路徑）。

### 2. 安裝依賴
本專案所需的套件包含：
*   `customtkinter`
*   `tensorflow`
*   `opencv-python`
*   `Pillow`
*   `numpy`

您可以透過 `pip` 逐一安裝：
```bash
pip install customtkinter tensorflow opencv-python Pillow numpy
```

### 3. 執行應用程式
在 `AI_Concept_App` 資料夾下，執行以下指令：
```bash
python app.py
```
程式啟動後，會需要一些時間載入 TensorFlow 模型，之後便會顯示主視窗。
