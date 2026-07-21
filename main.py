import cv2
import torch
import serial
import time
from collections import deque

# 1. Initialize Arduino Serial Communication
# NOTE: Update 'COM3' (Windows) or '/dev/ttyUSB0' (Linux/Mac) to your actual Arduino port
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)  # Allow time for the serial connection to initialize
    print("Arduino connected successfully.")
except Exception as e:
    print(f"Error connecting to Arduino: {e}. Running in simulation mode.")
    arduino = None

# 2. Load the YOLOv5s Model (Pretrained)
print("Loading YOLOv5s model...")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 3. Initialize Video Input
# Replace 'traffic_video.mp4' with 0 for live webcam feed, or your actual video file path
cap = cv2.VideoCapture('traffic_video.mp4') 

# 4. Initialize Data Structures for Rolling Average
# Deque stores the counts from the last 30 frames to smooth out detection fluctuations
lane1_history = deque(maxlen=30) 
lane2_history = deque(maxlen=30)

# Timer variables for adaptive scheduling logic
last_switch_time = time.time()
switch_interval = 10  # Evaluate traffic density every 10 seconds

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video stream.")
        break

    # Define lanes (Assuming a split screen for prototype: Left = Lane 1, Right = Lane 2)
    height, width, _ = frame.shape
    mid_point = width // 2

    # 5. Perform YOLOv5 Inference
    results = model(frame)
    df = results.pandas().xyxy[0]  # Extract bounding box predictions

    # Filter detections specifically for vehicles (COCO classes: car=2, motorcycle=3, bus=5, truck=7)
    vehicles = df[df['class'].isin([2, 3, 5, 7])]

    lane1_count = 0
    lane2_count = 0

    # 6. Categorize Vehicles by Lane
    for index, row in vehicles.iterrows():
        x_center = (row['xmin'] + row['xmax']) / 2
        if x_center < mid_point:
            lane1_count += 1
            # Draw bounding box for visual debugging
            cv2.rectangle(frame, (int(row['xmin']), int(row['ymin'])), (int(row['xmax']), int(row['ymax'])), (255, 0, 0), 2)
        else:
            lane2_count += 1
            cv2.rectangle(frame, (int(row['xmin']), int(row['ymin'])), (int(row['xmax']), int(row['ymax'])), (0, 0, 255), 2)

    # 7. Update Moving Averages
    lane1_history.append(lane1_count)
    lane2_history.append(lane2_count)
    
    avg_lane1 = sum(lane1_history) / len(lane1_history)
    avg_lane2 = sum(lane2_history) / len(lane2_history)

    # 8. Adaptive Control Algorithm (Decision Logic)
    current_time = time.time()
    if current_time - last_switch_time > switch_interval:
        if avg_lane1 > avg_lane2:
            decision = 'L1\n'
            print(f"Traffic higher in Lane 1 ({avg_lane1:.1f} vs {avg_lane2:.1f}). Switching Green to Lane 1.")
        else:
            decision = 'L2\n'
            print(f"Traffic higher in Lane 2 ({avg_lane2:.1f} vs {avg_lane1:.1f}). Switching Green to Lane 2.")
            
        # Transmit decision to hardware
        if arduino:
            arduino.write(decision.encode())
        
        last_switch_time = current_time  # Reset the 10-second timer

    # 9. GUI Visualization Overlay
    cv2.line(frame, (mid_point, 0), (mid_point, height), (0, 255, 0), 2)
    cv2.putText(frame, f"L1 Avg: {avg_lane1:.1f}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"L2 Avg: {avg_lane2:.1f}", (mid_point + 10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display processed frame
    cv2.imshow('Smart Traffic Light System Using YOLO', frame)

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 10. Clean Up Resources
cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
