import customtkinter as ctk
from PIL import Image
import cv2
import tensorflow as tf
import numpy as np
import threading
import os
from collections import deque
import time

# --- Constants ---
STABLE_PREDICTION_THRESHOLD = 5 # 需要連續5次預測相同才算穩定
CONFIDENCE_THRESHOLD = 0.80     # 可信度低於此值則忽略

# --- App Class ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("AI 即時手勢辨識")
        self.geometry("800x450")
        ctk.set_appearance_mode("dark")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- State Variables ---
        self.current_frame = None
        self.model = None
        self.labels = []
        self.prediction_history = deque(maxlen=STABLE_PREDICTION_THRESHOLD)
        self.last_stable_prediction = None

        # --- Layout Configuration ---
        self.grid_columnconfigure(0, weight=6)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        # --- Left Frame (for Camera) ---
        self.left_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#000000")
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.camera_label = ctk.CTkLabel(self.left_frame, text="")
        self.camera_label.pack(expand=True, fill="both")

        # --- Right Frame (for Info and Controls) ---
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        self.right_frame.grid_rowconfigure(0, weight=2) # Give more space to result
        self.right_frame.grid_rowconfigure(1, weight=1) # Space for progress bar
        self.right_frame.grid_rowconfigure(2, weight=2) # Space for status indicator
        self.right_frame.grid_columnconfigure(0, weight=1)

        # --- Result Label (Top Right) ---
        self.result_label = ctk.CTkLabel(self.right_frame, text="初始化中...", font=ctk.CTkFont(size=30, weight="bold"), wraplength=250)
        self.result_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")

        # --- Confidence Bar ---
        self.confidence_bar = ctk.CTkProgressBar(self.right_frame, orientation="horizontal", progress_color="#008A00")
        self.confidence_bar.set(0)
        self.confidence_bar.grid(row=1, column=0, padx=50, pady=10, sticky="ew")

        # --- Status Indicator (Bottom Right, Circular) ---
        self.status_indicator = ctk.CTkFrame(self.right_frame, width=150, height=150, corner_radius=75, fg_color="#404040", border_width=3, border_color="gray")
        self.status_indicator.grid(row=2, column=0, padx=20, pady=10)
        self.status_label = ctk.CTkLabel(self.status_indicator, text="待機", font=ctk.CTkFont(size=28, weight="bold"))
        self.status_label.place(relx=0.5, rely=0.5, anchor="center")

        # --- Start Processes ---
        # Load model in main thread to prevent threading errors with UI updates.
        # This will cause a short freeze on startup, which is acceptable.
        self.load_model_and_labels()
        self.cap = cv2.VideoCapture(0)
        self.update_camera()

    def load_model_and_labels(self):
        model_dir = r"C:\Users\user\AI\GitHub\project01\Ai-project-LEE\converted_keras"
        labels_path = os.path.join(model_dir, "labels.txt")

        # Update UI before blocking to load model
        self.result_label.configure(text="載入模型中...")
        self.update_idletasks() # Force UI to redraw

        try:
            model_layer = tf.keras.layers.TFSMLayer(model_dir, call_endpoint='serving_default')
            self.model = tf.keras.Sequential([model_layer])
            with open(labels_path, "r", encoding="utf-8") as f:
                self.labels = [line.strip().split(' ', 1)[1] for line in f.readlines()]
            print("模型和標籤載入成功。")
            self.result_label.configure(text="待機中")

            # Start prediction thread only after model is loaded successfully
            threading.Thread(target=self.prediction_worker, daemon=True).start()
        except Exception as e:
            print(f"載入模型或標籤失敗: {e}")
            self.result_label.configure(text="模型載入失敗！")

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            ctk_image = ctk.CTkImage(light_image=Image.fromarray(frame_rgb), size=frame_rgb.shape[0:2][::-1])
            self.camera_label.configure(image=ctk_image)
        self.after(10, self.update_camera)

    def prediction_worker(self):
        while True:
            if self.current_frame is None:
                time.sleep(0.1)
                continue

            frame_copy = self.current_frame.copy()
            resized_frame = cv2.resize(frame_copy, (224, 224))
            normalized_frame = (resized_frame.astype(np.float32) / 127.5) - 1
            input_data = np.expand_dims(normalized_frame, axis=0)
            
            try:
                prediction_dict = self.model.predict(input_data, verbose=0)
                prediction_tensor = list(prediction_dict.values())[0]
                confidence = np.max(prediction_tensor)
                
                if confidence < CONFIDENCE_THRESHOLD:
                    self.update_prediction_state(None, 0)
                else:
                    predicted_index = np.argmax(prediction_tensor)
                    predicted_label = self.labels[predicted_index]
                    self.update_prediction_state(predicted_label, confidence)
            except Exception as e:
                print(f"預測時發生錯誤: {e}")
            
            time.sleep(0.1) # Control prediction frequency

    def update_prediction_state(self, label, confidence):
        if label is None or label.lower() == "nothing":
            self.prediction_history.clear()
            if self.last_stable_prediction is not None:
                self.last_stable_prediction = None
                self.after(0, self.update_ui_for_idle)
            return

        self.prediction_history.append(label)

        if len(self.prediction_history) == self.prediction_history.maxlen and len(set(self.prediction_history)) == 1:
            stable_prediction = self.prediction_history[0]
            if stable_prediction != self.last_stable_prediction:
                self.last_stable_prediction = stable_prediction
                self.after(0, self.update_ui_for_stable_prediction, stable_prediction, confidence)
        else:
            if self.last_stable_prediction is not None:
                 self.last_stable_prediction = None
                 self.after(0, self.update_ui_for_detecting)

    def update_ui_for_idle(self):
        self.result_label.configure(text="待機中")
        self.confidence_bar.set(0)
        self.status_indicator.configure(fg_color="#404040", border_color="gray")
        self.status_label.configure(text="待機")

    def update_ui_for_detecting(self):
        self.result_label.configure(text="偵測中...")
        self.confidence_bar.set(0)
        self.status_indicator.configure(fg_color="#B08000", border_color="yellow")
        self.status_label.configure(text="分析")

    def update_ui_for_stable_prediction(self, label, confidence):
        self.result_label.configure(text=label)
        self.confidence_bar.set(confidence)
        self.status_indicator.configure(fg_color="#008A00", border_color="lightgreen")
        self.status_label.configure(text="鎖定")

    def on_closing(self):
        print("Releasing camera and closing app...")
        self.cap.release()
        self.destroy()

# --- Main Execution ---
if __name__ == "__main__":
    app = App()
    app.mainloop()
