import cv2
from PIL import Image, ImageTk

class CameraStream:
    def __init__(self, camera_index=0):
        """
        初始化攝影機串流。
        :param camera_index: 攝影機的索引，0 通常是預設的筆電鏡頭。
        """
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise IOError("無法開啟攝影機")
        
        # 獲取攝影機的寬度和高度
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"攝影機初始化成功，解析度: {self.width}x{self.height}")

    def get_frame(self):
        """
        從攝影機讀取單一畫面。
        :return: 成功時返回 (True, frame)，失敗時返回 (False, None)。
                 frame 是 OpenCV 的 BGR 格式影像。
        """
        ret, frame = self.cap.read()
        if ret:
            # 垂直翻轉影像，使其看起來像鏡子
            return ret, cv2.flip(frame, 1)
        return ret, None

    def release(self):
        """
        釋放攝影機資源。
        """
        self.cap.release()
        print("攝影機資源已釋放。")

# --- 以下為單獨測試此模組的程式碼 ---
if __name__ == '__main__':
    try:
        camera = CameraStream()
        print("按 'q' 鍵關閉預覽視窗。")
        while True:
            ret, frame = camera.get_frame()
            if not ret:
                print("無法獲取影像，結束預覽。")
                break
            
            cv2.imshow('Camera Preview', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        if 'camera' in locals():
            camera.release()
        cv2.destroyAllWindows()
        print("預覽結束。")
