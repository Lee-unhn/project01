import sys
import os
# 將專案根目錄添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import numpy as np
import tensorflow as tf
from threading import Thread
import time

from camera_utils.camera_stream import CameraStream
from game_logic.rps_game import RPSGame

class RPSApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 基本視窗設定 ---
        self.title("剪刀石頭布 AI 遊戲")
        self.geometry("1200x800")
        ctk.set_appearance_mode("dark")

        # --- 變數初始化 ---
        self.player_move = None
        self.last_prediction_time = time.time()
        self.prediction_cooldown = 2 # 辨識到結果後，冷卻2秒再開始新一輪
        self.is_game_on = True

        # --- 載入模型與標籤 ---
        self.model, self.labels = self.load_model_and_labels()
        # 標籤映射: 將 "0 剪刀" -> "scissors"
        self.internal_labels = {
            "剪刀": "scissors",
            "石頭": "rock",
            "布": "paper",
            "沒有": "nothing"
        }

        # --- 初始化核心元件 ---
        self.camera = CameraStream()
        self.game = RPSGame()

        # --- UI 元件建立 ---
        self.create_widgets()

        # --- 啟動更新迴圈 ---
        self.update_camera_feed()
        
        # --- 啟動預測執行緒 ---
        self.prediction_thread = Thread(target=self.prediction_worker, daemon=True)
        self.prediction_thread.start()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # --- 主框架 ---
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # --- 標題 ---
        self.status_label = ctk.CTkLabel(main_frame, text="請對鏡頭出拳", font=ctk.CTkFont(size=30, weight="bold"))
        self.status_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # --- 攝影機畫面 ---
        self.camera_label = ctk.CTkLabel(main_frame, text="")
        self.camera_label.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # --- 遊戲資訊區 ---
        game_info_frame = ctk.CTkFrame(main_frame)
        game_info_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        game_info_frame.grid_columnconfigure(0, weight=1)

        # 分數
        self.score_label = ctk.CTkLabel(game_info_frame, text="玩家: 0  |  AI: 0", font=ctk.CTkFont(size=24))
        self.score_label.grid(row=0, column=0, pady=20)

        # 玩家出拳
        self.player_move_label = ctk.CTkLabel(game_info_frame, text="你的出拳: ?", font=ctk.CTkFont(size=20))
        self.player_move_label.grid(row=1, column=0, pady=10)

        # AI 出拳
        self.ai_move_label = ctk.CTkLabel(game_info_frame, text="AI 的出拳: ?", font=ctk.CTkFont(size=20))
        self.ai_move_label.grid(row=2, column=0, pady=10)

        # 重置按鈕
        self.reset_button = ctk.CTkButton(game_info_frame, text="重置分數", command=self.reset_game, font=ctk.CTkFont(size=18))
        self.reset_button.grid(row=3, column=0, pady=40)


    def load_model_and_labels(self):
        # 使用我們之前確認可行的路徑
        model_dir = os.path.join(os.path.dirname(__file__), "..", "models", "converted_keras")
        labels_path = os.path.join(model_dir, "labels.txt")

        try:
            # 根據 Keras 3 的要求，使用 TFSMLayer 載入 SavedModel
            print("正在載入模型 (Keras 3 / TFSMLayer)...")
            model_layer = tf.keras.layers.TFSMLayer(model_dir, call_endpoint='serving_default')
            self.model = tf.keras.Sequential([model_layer])
            print("模型載入成功。")

            with open(labels_path, "r", encoding="utf-8") as f:
                # 讀取 "0 剪刀" -> ["剪刀", "石頭", ...]
                self.labels = [line.strip().split(' ', 1)[1] for line in f.readlines()]
            print(f"標籤載入成功: {self.labels}")
            return self.model, self.labels
        except Exception as e:
            print(f"載入模型或標籤失敗: {e}")
            # 如果模型載入失敗，提供一個備用的空模型和標籤，讓應用程式仍能運行
            self.model = None
            self.labels = ["剪刀", "石頭", "布", "沒有"] # 備用標籤
            print("模型載入失敗，應用程式將以無模型模式啟動。")
            return self.model, self.labels
            
    def update_camera_feed(self):
        ret, frame = self.camera.get_frame()
        if ret:
            # 將 OpenCV BGR 影像轉換為 PIL 格式
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img)
            
            # 轉換為 CTk 適用的影像格式
            ctk_img = ctk.CTkImage(light_image=pil_img, size=(self.camera.width, self.camera.height))
            self.camera_label.configure(image=ctk_img)
            self.camera_label.image = ctk_img

        # 每 15ms 更新一次
        self.after(15, self.update_camera_feed)

    def prediction_worker(self):
        while True:
            # 確保模型已載入，且遊戲未暫停
            if self.model is None or not self.is_game_on:
                time.sleep(0.5)
                continue

            # --- 影像預處理 ---
            ret, frame = self.camera.get_frame()
            if not ret:
                time.sleep(0.1) # 避免無效幀時 CPU 過高
                continue

            # 調整影像大小以符合模型輸入
            resized_frame = cv2.resize(frame, (224, 224))
            # 標準化
            normalized_frame = (resized_frame.astype(np.float32) / 127.5) - 1
            # 擴展維度以符合模型輸入格式 (1, 224, 224, 3)
            input_data = np.expand_dims(normalized_frame, axis=0)

            try:
                # --- 進行預測 ---
                # TFSMLayer 的輸出通常是一個字典，我們需要從中提取預測結果
                prediction_dict = self.model.predict(input_data, verbose=0)
                prediction_tensor = list(prediction_dict.values())[0] # 假設我們需要的張量是字典中的第一個值
                
                predicted_index = np.argmax(prediction_tensor)
                confidence = np.max(prediction_tensor)

                # --- Debug Prints ---
                print(f"DEBUG: Raw Prediction Tensor (first 5 elements): {prediction_tensor[0][:5]}") # Print only first 5 elements for brevity
                print(f"DEBUG: Predicted Index: {predicted_index}, Confidence: {confidence:.2f}")

                # --- 處理預測結果 ---
                label_text = self.labels[predicted_index]
                player_move = self.internal_labels.get(label_text)
                print(f"DEBUG: Label Text: {label_text}, Player Move: {player_move}")

                if confidence > 0.90: # 只處理高信度的預測
                    if player_move and player_move != "nothing":
                        # 在主執行緒中觸發遊戲回合以確保UI安全更新
                        self.after(0, self.trigger_game_round, player_move)
                    else:
                        print(f"DEBUG: Not triggering game round. Player move is '{player_move}' (or None).")
                else:
                    print(f"DEBUG: Confidence {confidence:.2f} is below threshold 0.90. No game round triggered.")
            except Exception as e:
                print(f"預測時發生錯誤: {e}")
                # 可以在 UI 上顯示錯誤訊息
                # self.after(0, lambda: self.status_label.configure(text=f"預測錯誤: {e}"))

            time.sleep(0.1) # 降低 CPU 使用率

    def trigger_game_round(self, player_move):
        # 檢查冷卻時間
        current_time = time.time()
        if current_time - self.last_prediction_time < self.prediction_cooldown:
            return

        self.is_game_on = False # 暫停遊戲以顯示結果
        self.last_prediction_time = current_time

        ai_move = self.game.get_ai_choice()
        winner, reason = self.game.get_winner(player_move, ai_move)

        # --- 更新 UI ---
        self.status_label.configure(text=f"結果: {reason}")
        self.player_move_label.configure(text=f"你的出拳: {player_move.capitalize()}")
        self.ai_move_label.configure(text=f"AI 的出拳: {ai_move.capitalize()}")
        
        scores = self.game.get_scores()
        self.score_label.configure(text=f"玩家: {scores['player']}  |  AI: {scores['ai']}")

        # 短暫延遲後重新開始
        self.after(2000, self.prepare_next_round)

    def prepare_next_round(self):
        self.status_label.configure(text="請對鏡頭出拳")
        self.player_move_label.configure(text="你的出拳: ?")
        self.ai_move_label.configure(text="AI 的出拳: ?")
        self.is_game_on = True

    def reset_game(self):
        self.game.reset_scores()
        scores = self.game.get_scores()
        self.score_label.configure(text=f"玩家: {scores['player']}  |  AI: {scores['ai']}")
        self.prepare_next_round()
        print("分數已重置。")

    def on_closing(self):
        print("正在關閉應用程式...")
        self.camera.release()
        self.destroy()

if __name__ == "__main__":
    app = RPSApp()
    app.mainloop()
