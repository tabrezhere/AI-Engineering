import cv2

print("Opening camera...")

camera = cv2.VideoCapture(0)

ret, frame = camera.read()

if ret:
    cv2.imwrite("photo.jpg", frame)
    print("Photo captured successfully!")
    print("Saved as photo.jpg")
else:
    print("Could not access the camera.")

camera.release()