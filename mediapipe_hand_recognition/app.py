import cv2
import mediapipe as mp
import time
import pyautogui
import os # Import os module
import pygetwindow as gw
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Define the connections between hand landmarks for drawing the skeleton
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (9, 10), (10, 11), (11, 12),
    (13, 14), (14, 15), (15, 16),
    (0, 17), (17, 18), (18, 19), (19, 20),
    (5, 9), (9, 13), (13, 17)
]

# Path to the gesture recognizer model file
# Construct the absolute path to the model file
script_dir = os.path.dirname(__file__)
model_path = os.path.join(script_dir, 'models', 'gesture_recognizer.task')

# --- Feature Variables ---
GESTURE_HOLD_DURATION = 0.3 # Common hold duration for navigation gestures
APP_CLOSE_HOLD_DURATION = 2.0 # Hold duration for closing the app
GESTURE_COOLDOWN = 2.0 # seconds

# Timers and states for each gesture
pointing_up_start_time = None
fist_start_time = None
victory_start_time = None
open_palm_start_time = None

gesture_cooldown_end_time = 0

# MediaPipe Gesture Recognizer setup
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a gesture recognizer instance with the image mode:
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1 # Limit to one hand for clearer control
)
recognizer = GestureRecognizer.create_from_options(options)

# Webcam setup
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Read frame from camera
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Perform gesture recognition
    gesture_recognition_result = recognizer.recognize(mp_image)

    # --- Gesture Control Logic ---
    is_on_cooldown = time.time() < gesture_cooldown_end_time
    current_gesture = "None"
    if gesture_recognition_result.gestures:
        current_gesture = gesture_recognition_result.gestures[0][0].category_name
        # For debugging gesture names:
        print(f"Detected gesture: {current_gesture}") # Keep this for user debugging

    # Reset all timers if not on cooldown
    if not is_on_cooldown:
        # --- Pointing_Up ---
        if current_gesture == 'Pointing_Up':
            if pointing_up_start_time is None: pointing_up_start_time = time.time()
            if (time.time() - pointing_up_start_time) > GESTURE_HOLD_DURATION:
                print("Pointing_Up held. Switching to previous window...")
                pyautogui.hotkey('alt', 'shift', 'tab')
                pointing_up_start_time = None
                gesture_cooldown_end_time = time.time() + GESTURE_COOLDOWN
        else:
            pointing_up_start_time = None
        
        # --- Closed_Fist ---
        if current_gesture == 'Closed_Fist':
            if fist_start_time is None: fist_start_time = time.time()
            if (time.time() - fist_start_time) > GESTURE_HOLD_DURATION:
                print("Closed_Fist held. Switching to next window...")
                pyautogui.hotkey('alt', 'tab')
                fist_start_time = None
                gesture_cooldown_end_time = time.time() + GESTURE_COOLDOWN
        else:
            fist_start_time = None

        # --- Victory ---
        if current_gesture == 'Victory':
            if victory_start_time is None: victory_start_time = time.time()
            if (time.time() - victory_start_time) > GESTURE_HOLD_DURATION:
                print("Victory held. Bringing app window to front...")
                try:
                    window = gw.getWindowsWithTitle('MediaPipe Gesture Recognition')[0]
                    if window:
                        window.activate()
                except IndexError:
                    print("Could not find the app window 'MediaPipe Gesture Recognition'.")
                victory_start_time = None
                gesture_cooldown_end_time = time.time() + GESTURE_COOLDOWN
        else:
            victory_start_time = None

        # --- Open_Palm ---
        if current_gesture == 'Open_Palm':
            if open_palm_start_time is None: open_palm_start_time = time.time()
            if (time.time() - open_palm_start_time) > APP_CLOSE_HOLD_DURATION:
                print("Open_Palm held. Closing app...")
                break # Exit the main loop to close the app
        else:
            open_palm_start_time = None

    # --- UI/UX Drawing ---
    
    # Define colors and positions
    ui_bg_color = (20, 20, 20)
    ui_text_color = (255, 255, 255)
    hint_color = (200, 200, 200)
    cooldown_color = (50, 50, 255)
    timer_color = (255, 255, 0)
    
    # Create semi-transparent overlays
    overlay = frame.copy()
    
    # Bottom Status Bar
    cv2.rectangle(overlay, (0, h - 60), (w, h), ui_bg_color, -1)
    
    # Right Hint Panel
    cv2.rectangle(overlay, (w - 220, 0), (w, h), ui_bg_color, -1)
    
    # Blend overlays with the frame
    alpha = 0.6
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    # --- Draw Text on UI Panels ---

    # 1. Status Text (Bottom Bar)
    status_text = f"Gesture: {current_gesture}"
    cv2.putText(frame, status_text, (10, h - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, ui_text_color, 2)
    
    # Display Cooldown or active timer
    if is_on_cooldown:
        cooldown_time_left = gesture_cooldown_end_time - time.time()
        timer_text = f"COOLDOWN: {cooldown_time_left:.1f}s"
        cv2.putText(frame, timer_text, (w - 180, h - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cooldown_color, 2)
    else:
        # Display active gesture timer
        timer_text = ""
        if pointing_up_start_time: timer_text = f"Holding Point Up... ({time.time() - pointing_up_start_time:.1f}s)"
        elif fist_start_time: timer_text = f"Holding Fist... ({time.time() - fist_start_time:.1f}s)"
        elif victory_start_time: timer_text = f"Holding Victory... ({time.time() - victory_start_time:.1f}s)"
        elif open_palm_start_time: timer_text = f"Holding Open Palm... ({time.time() - open_palm_start_time:.1f}s)"
        
        if timer_text:
            cv2.putText(frame, timer_text, (250, h - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, timer_color, 2)

    # 2. Hint Text (Right Panel)
    cv2.putText(frame, "Commands", (w - 190, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, ui_text_color, 2)
    cv2.line(frame, (w - 210, 60), (w - 10, 60), hint_color, 1)
    
    hints = [
        ("Fist (0.3s)", "-> Next Win"),
        ("Point Up (0.3s)", "-> Prev Win"),
        ("Victory (0.3s)", "-> Focus App"),
        ("Open Palm (2s)", "-> Close App")
    ]
    
    for i, (gesture, action) in enumerate(hints):
        y_pos = 100 + i * 60
        cv2.putText(frame, gesture, (w - 210, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, hint_color, 1)
        cv2.putText(frame, action, (w - 210, y_pos + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, hint_color, 1)

    cv2.imshow('MediaPipe Gesture Recognition', frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Cleanup
pyautogui.keyUp('alt') # Ensure alt key is released on exit
cap.release()
cv2.destroyAllWindows()
recognizer.close()