import cv2
import tensorflow as tf
import numpy as np

# 0 代表預設的攝影機
cap = cv2.VideoCapture(0)

# 模型和標籤路徑
MODEL_PATH = r"C:\Users\user\AI\GitHub\project01\Ai-project-LEE\converted_keras"
LABELS_PATH = r"C:\Users\user\AI\GitHub\project01\Ai-project-LEE\converted_keras\labels.txt"

# 載入模型和標籤
try:
    # 根據 Keras 3 的要求，使用 TFSMLayer 載入 SavedModel
    print("偵測到 Keras 3 環境，嘗試使用 TFSMLayer 載入...")
    model_layer = tf.keras.layers.TFSMLayer(MODEL_PATH, call_endpoint='serving_default')
    # 為了讓 .predict() 方法能像之前一樣使用，我們將 layer 包裝在一個 Sequential 模型中
    model = tf.keras.Sequential([model_layer])
    print(f"模型載入成功 (Keras 3 / TFSMLayer): {MODEL_PATH}")

    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        labels = [line.strip().split(' ', 1)[1] for line in f.readlines()]
    print(f"標籤載入成功: {LABELS_PATH}, 內容: {labels}")
except Exception as e:
    print(f"載入模型或標籤失敗: {e}")
    print("請確認 `converted_keras` 資料夾內包含 `saved_model.pb` 和 `variables` 資料夾。")
    exit()


if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # 逐幀捕獲
    ret, frame = cap.read()

    # 如果正确读取帧，ret为True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # --- 影像預處理 ---
    # 調整影像大小以符合模型輸入 (Teachable Machine Keras 模型通常是 224x224)
    resized_frame = cv2.resize(frame, (224, 224))
    # 標準化像素值 (Teachable Machine Keras 模型通常是歸一化到 -1 到 1 之間)
    normalized_frame = (resized_frame.astype(np.float32) / 127.5) - 1
    # 擴展維度以符合模型輸入格式 (1, 224, 224, 3)
    input_data = np.expand_dims(normalized_frame, axis=0)

    # --- 進行預測 ---
    # Keras 3 的 TFSMLayer 輸出是一個字典，我們需要從中提取預測結果
    prediction_dict = model.predict(input_data, verbose=0)
    # 假設我們需要的張量是字典中的第一個值
    prediction_tensor = list(prediction_dict.values())[0]
    
    predicted_index = np.argmax(prediction_tensor)
    confidence = np.max(prediction_tensor)

    # --- 顯示預測結果 (在畫面上) ---
    predicted_label = labels[predicted_index]
    display_text = f"預測: {predicted_label} ({confidence:.2f})"
    cv2.putText(frame, display_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    # --- 偵錯：印出預測結果到控制台 ---
    print(display_text)

    # 顯示結果幀
    cv2.imshow('Camera Stream', frame)

    # 按 'q' 鍵退出迴圈
    if cv2.waitKey(1) == ord('q'):
        break

# 完成後釋放捕獲
cap.release()
cv2.destroyAllWindows()
