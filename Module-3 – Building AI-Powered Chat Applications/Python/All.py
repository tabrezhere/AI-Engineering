import os
import cv2
# 1. System Control
print("1. Opening Notepad...")
os.system("notepad")

# 2. File Operation
print("2. Creating file...")

with open("demo.txt", "w") as file:
    file.write("Hello ISL")

print("demo.txt created!")

# 3. Hardware Access


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
# 4. Code Execution
print("3. Performing calculation...")

numbers = [10, 20, 30, 40, 50]
total = sum(numbers)

print("Total =", total)

# 4. Result
print("All operations completed!")