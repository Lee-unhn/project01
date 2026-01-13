AI Vision Applications Collection
這是一個基於 MediaPipe 與 OpenCV 開發的 AI 視覺應用整合專案。本專案旨在探索電腦視覺（Computer Vision）在不同場景下的應用，從基礎的手勢辨識到進階的系統自動化操作。

📂 專案功能說明
目前專案內包含以下四大核心系統：

1. ✌️ 簡單剪刀石頭布系統 (Rock-Paper-Scissors Game)
功能： 透過鏡頭即時辨識玩家的手勢（剪刀、石頭或布），並與電腦進行對戰。

技術： 手掌偵測、指尖位置計算、邏輯判定。

2. ✋ 手部辨識系統 (Hand Tracking System)
功能： 高精準度追蹤手部 21 個關鍵點（Landmarks），並即時繪製骨架連線。

技術： 使用 MediaPipe Tasks API 定義手部骨架模型。

3. 👤 臉部辨識系統 (Face Detection & Recognition)
功能： 偵測畫面中的人臉位置，並標記面部特徵點或進行身份識別。

技術： 臉部關鍵點偵測、邊界框（Bounding Box）繪製。

4. 💻 手勢操縱視窗系統 (Gesture Window Controller)
功能： 透過特定手勢（如捏合、揮動）來控制電腦視窗，例如調整音量、模擬滑鼠點擊或切換視窗。

技術： 座標映射（Mapping）、動態手勢軌跡追蹤、PyAutoGUI 系統整合。

🛠️ 技術棧 (Tech Stack)
程式語言： Python 3.10+

核心框架： * MediaPipe: 提供強大的 AI 模型處理手部與臉部偵測。

OpenCV: 用於影像處理與即時畫面渲染。

系統控制： PyAutoGUI / Screen-Brightness-Control (用於視窗操縱)。

🚀 快速上手
1. 複製專案
Bash

git clone https://github.com/你的帳號/你的專案名稱.git
cd AI-media
2. 環境設定
建議使用 Conda 或虛擬環境：

Bash

conda create -n mediapipe_env python=3.10
conda activate mediapipe_env
pip install -r requirements.txt
3. 執行程式
Bash

# 執行手部骨架辨識
python work1.py
📈 未來計畫
[ ] 加入更多自定義手勢模型（Gesture Customization）。

[ ] 整合多模態互動（同時辨識臉部表情與手勢）。

[ ] 優化即時處理效能，降低 CPU 使用率。

📜 授權 (License)
本專案基於 MIT 授權條款。

1. 將您的手（握拳代表石頭、五指張開代表布、兩指伸出代表剪刀）放在攝影機前。
2. 應用程式會辨識您的手勢並顯示在畫面上。
3. AI 會同時做出它的選擇。
4. 每一局的結果（贏、輸、平手）會顯示在畫面上方。

---
祝您遊戲愉快！
