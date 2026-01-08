import cv2

# 0 代表預設的攝影機
cap = cv2.VideoCapture(0)

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

    # 顯示結果幀
    cv2.imshow('Camera Stream', frame)

    # 按 'q' 鍵退出迴圈
    if cv2.waitKey(1) == ord('q'):
        break

# 完成後釋放捕獲
cap.release()
cv2.destroyAllWindows()
