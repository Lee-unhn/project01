import cv2
import mediapipe as mp
import time
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 定義手部 21 個點之間的連線關係 (官方標準)
HAND_CONNECTIONS = [
    # 掌心/大拇指
    (0, 1), (1, 2), (2, 3), (3, 4),
    # 食指
    (0, 5), (5, 6), (6, 7), (7, 8),
    # 中指
    (9, 10), (10, 11), (11, 12),
    # 無名指
    (13, 14), (14, 15), (15, 16),
    # 小指
    (0, 17), (17, 18), (18, 19), (19, 20),
    # 掌心連線 (指根相連)
    (5, 9), (9, 13), (13, 17)
]

def main():
    # 模型路徑設定
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'gesture_recognizer.task')
    
    if not os.path.exists(model_path):
        print(f"錯誤：找不到模型檔 {model_path}")
        return

    # 設定辨識器
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2
    )

    cap = cv2.VideoCapture(0)
    
    with vision.GestureRecognizer.create_from_options(options) as recognizer:
        print("骨架連線版啟動... 按下 'q' 退出")
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success: break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            timestamp_ms = int(time.time() * 1000)
            result = recognizer.recognize_for_video(mp_image, timestamp_ms)

            # --- 手動繪製骨架邏輯 ---
            if result.hand_landmarks:
                for i, landmarks in enumerate(result.hand_landmarks):
                    # 1. 先計算所有點的像素座標
                    points = []
                    for lm in landmarks:
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        points.append((cx, cy))

                    # 2. 畫出連線 (骨架)
                    for connection in HAND_CONNECTIONS:
                        start_idx = connection[0]
                        end_idx = connection[1]
                        cv2.line(frame, points[start_idx], points[end_idx], (255, 255, 255), 2) # 白色線條

                    # 3. 畫出關鍵點 (關節)
                    for pt in points:
                        cv2.circle(frame, pt, 5, (0, 255, 0), -1) # 綠色圓點

                    # 4. 顯示手勢文字
                    if result.gestures and len(result.gestures[i]) > 0:
                        gesture_name = result.gestures[i][0].category_name
                        cv2.putText(frame, gesture_name, (points[0][0], points[0][1] - 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            cv2.imshow('Manual Hand Skeleton', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()