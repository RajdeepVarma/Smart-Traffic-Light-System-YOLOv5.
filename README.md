# Smart Traffic Light System Using YOLO

This repository contains the implementation of a Smart Traffic Light System that dynamically adjusts signal timings based on real-time lane-wise vehicle density. Traditional traffic lights rly on fixed-time intervals, leading to inefficient road utilization and congestion. This project overcomes that limitation by integrating computer vision and embedded hardware to create an automated, adaptive traffic management solution

Using the **YOLOv5** deep learning model, the system processes live video feeds to detect and count vehicles in real-time. A rolling average mechanism via Python's `deque` ensures stable density estimation. Based on these counts, an adaptive scheduling algorithm determines the optimal green light allocation, prioritizing heavily congested lanes. The decision output is transmitted via serial communication to an **Arduino microcontroller**, which physically actuates the LED traffic signals

### Key Features
* **Real-Time Vehicle Detection:** Utilizes PyTorch and the YOLOv5s model for high-speed object detection, achieving an accuracy of approximately 96.3%
* **Adaptive Signal Control:** Dynamically allocates green signal duration based on real-time traffic density comparisons between lanes
* **Hardware Integration:** Bridges software-based AI perception with physical actuation using an Arduino microcontroller and serial communication
* **Data Smoothing:** Implements a sliding window approach to maintain a rolling average of vehicle counts, preventin abrupt signal changes due to temporary detection fluctuations
