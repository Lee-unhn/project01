# MediaPipe 手勢辨識 - 手動繪製骨架範例

## 專案總覽

本專案包含一個 Python 腳本 (`work1.py`) 和一個 MediaPipe 手勢辨識模型 (`gesture_recognizer.task`)。其主要目的是展示如何使用 MediaPipe `tasks` API 進行即時手勢辨識，並完全透過 OpenCV 手動繪製出手部的骨架和關節點。

---

## 主要功能與技術特點

*   **現代化 MediaPipe API**: 使用 `mediapipe.tasks.vision.GestureRecognizer`，這是目前官方推薦的 API，並以 `VIDEO` 串流模式運行。
*   **手動骨架繪製**:
    *   本專案的**核心亮點**是不依賴 `mediapipe.solutions.drawing_utils` 這個可能在不同版本間存在差異的繪圖工具。
    *   它展示了如何自行定義 `HAND_CONNECTIONS` (手部關節連線)。
    *   透過迭代模型輸出的手部地標 (landmarks)，計算其在畫面上的實際像素座標。
    *   使用 OpenCV 的 `cv2.line` 函式繪製骨架連線，並用 `cv2.circle` 函式標示關節點。
*   **即時結果呈現**: 在畫面上即時顯示辨識出的手勢名稱，例如 "Victory", "Open_Palm" 等。

---

## 專案目的

對於希望完全客製化手部骨架視覺效果，或者在 `drawing_utils` 不可用或不適用的環境中進行開發的開發者來說，這個腳本提供了一個清晰、可行的解決方案。它讓開發者能完全掌控骨架的顏色、粗細、樣式等視覺元素。

---

## 環境設置與執行

### 1. 前置條件
*   Python 3.8 或更高版本。
*   已連接的電腦攝影機。

### 2. 確認檔案
*   確保 `work1.py` 和 `gesture_recognizer.task` 兩個檔案位於同一個資料夾中。

### 3. 安裝依賴
本專案所需的主要套件為：
*   `mediapipe`
*   `opencv-python`

您可以透過 `pip` 進行安裝：
```bash
pip install mediapipe opencv-python
```

### 4. 執行腳本
在 `AI-media` 資料夾下，執行以下指令：
```bash
python work1.py
```
程式會開啟一個顯示攝影機畫面的視窗，並在您的手部出現時繪製出手部骨架。在命令列視窗按下 `q` 鍵可關閉程式。
