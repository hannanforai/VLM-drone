import json
import cv2  # OpenCV

img = cv2.imread("frame.jpg")  # load the saved picture
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # brightness only: 0 = black, 255 = white
_, mask = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)  # pixels darker than 90 become white
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # outline of each blob

detections = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)  # smallest upright box around the blob
    if w * h < 2000:  # ignore tiny specks
        continue
    detections.append({"x": x, "y": y, "w": w, "h": h, "cx": x + w // 2, "cy": y + h // 2})
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)  # green box, 3 px thick

print(json.dumps(detections))  # the detections as JSON text
cv2.imwrite("detected.jpg", img)  # picture with boxes drawn on it