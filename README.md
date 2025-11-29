#  Autonomous Vehicle Prototype (Raspberry Pi 4)

## Overview

This project details the design, implementation, and testing of a prototype autonomous vehicle capable of **Lane Keeping** and **Obstacle Detection**. Built around a **Raspberry Pi 4**, the system uses computer vision (OpenCV) to interpret road markings and ultrasonic sensors to detect physical barriers, creating a robust *"Sense-Think-Act"* control loop.

This repository contains the source code and documentation required to replicate this project, which was developed at **COEP Technological University, Pune** for the *Sensors for Industrial Robotics* course.

##  Features

### Driving & Safety Logic

1. First ordered list item: **Real-time Lane Detection**
   * Uses a Pi Camera and OpenCV to detect lane lines via edge detection and centroid calculation.
2. Another item: **Obstacle Avoidance (Sonar)**
   * Uses an **HC-SR04 Ultrasonic sensor** to measure time-of-flight distance.
3. Actual numbers don't matter, just that it's a number: **Hierarchical Safety Logic**
   * A decision system that prioritizes collision avoidance over lane following:
     1. Ordered sub-list: **< 15 cm:** **Emergency Stop** (`STOP()`).
     2. Ordered sub-list: **15 cm – 30 cm:** _Slow Down_ (`SLOW_DOWN()`) to 15% duty cycle, while continuing lane following.
     3. Ordered sub-list: **> 30 cm:** _Normal Navigation_ (`NORMAL_SPEED()`) at 35% duty cycle, with full lane following.

### Hardware & Chassis

* Modular Chassis: Custom **3D-printed ABS chassis** featuring a parallel Ackerman steering geometry.
* Steering Mechanism: SG90 Micro Servo programmed to operate within a range of $\pm30^{\circ}$ (60$^{\circ}$ to 120$^{\circ}$) for precise directional control.

##  Hardware Requirements

| Component | Specification | Qty |
| :--- | :--- | :--- |
| **Processing Unit** | **Raspberry Pi 4 Model B** (2GB or higher) | 1 |
| **Vision Sensor** | Raspberry Pi Camera Module (Rev 1.3, 5MP) | 1 |
| **Distance Sensor** | HC-SR04 Ultrasonic Sensor | 1 |
| **Motor Driver** | L298N Dual Channel Driver | 1 |
| **Drive Motors** | 12V DC BO Motors (Straight Shaft) | 2 |
| **Steering Motor** | SG90 Micro Servo (360$^{\circ}$ or 180$^{\circ}$) | 1 |
| **Power (Logic)** | 10,000mAh Power Bank (5V 3A) | 1 |
| **Power (Drive)** | 3S2P Li-ion 18650 Pack (12V) | 1 |
| **Misc** | Breadboard, Jumper Wires, **Voltage Divider Resistors** (1kΩ & 2kΩ) | As needed |

##  Circuit & Wiring

**WARNING: Voltage Divider Required**
*The HC-SR04 Echo pin outputs **5V**, but the Raspberry Pi GPIO is only **3.3V tolerant**. You **MUST** use a voltage divider (1kΩ and 2kΩ resistors) on the Echo line to safely drop the voltage to 3.3V, preventing damage to the Raspberry Pi. 

### Pin Configuration (BCM Mode)

| Component | Pin Label | Raspberry Pi GPIO (BCM) | Function |
| :--- | :--- | :--- | :--- |
| **Motor Driver** | ENA | **GPIO 22** | Left Motor Speed (PWM) |
| **Motor Driver** | IN1 | **GPIO 24** | Left Motor Direction |
| **Motor Driver** | IN2 | **GPIO 23** | Left Motor Direction |
| **Motor Driver** | ENB | **GPIO 25** | Right Motor Speed (PWM) |
| **Motor Driver** | IN3 | **GPIO 17** | Right Motor Direction |
| **Motor Driver** | IN4 | **GPIO 27** | Right Motor Direction |
| **Servo Motor** | PWM | **GPIO 19** | Steering Angle Control |
| **Ultrasonic** | Trigger | **GPIO 18** | Send Sound Pulse |
| **Ultrasonic** | Echo | **GPIO 21** | Receive Echo (via Divider) |

##  Software Architecture

The software operates on a continuous **Sense** $\rightarrow$ **Think** $\rightarrow$ **Act** loop.

### 1. Lane Detection (Vision)

The vision system uses standard OpenCV techniques on a 640x480 video frame:

| Step | Description |
| :--- | :--- |
| **Preprocessing** | Convert to Grayscale, apply Gaussian Blur (5x5 kernel), and Inverse Binary Thresholding (Threshold: 100). |
| **ROI** | Focuses processing on the **bottom 10%** of the image frame. |
| **Calculation** | Finds contours, selects the largest one, and calculates the **Centroid** ($C_x$) using Image Moments. |
| **Error Signal** | Deviation = $C_x$ - 320 (Center of frame). |

### 2. Obstacle Detection (Sonar)

| Step | Formula |
| :--- | :--- |
| **Pulse** | Sends a 10µs Trigger pulse. |
| **Duration** | Calculates the duration of the Echo pulse (Time\_Elapsed). |
| **Distance** | $\text{Distance} = (\text{Time\_Elapsed} \times 34300) / 2$ |

## ⚙️ Installation & Usage

### Prerequisites

1. First ordered list item: **Enable Camera**
   * Run `sudo raspi-config` > Interface Options > Camera > Enable.
2. Another item: **Enable I2C/GPIO**
   * Ensure GPIO interfaces are enabled via `sudo raspi-config`.

### Dependencies

Install the required Python libraries and tools:

```bash
sudo apt-get update
sudo apt-get install python3-opencv python3-pip
pip3 install RPi.GPIO
pip3 install picamera2
pip3 install numpy
```

### Running the Autonomous Code

1. **Clone this repository:**

   ```bash
   git clone [https://github.com/dharmikyash7118/Self-Driving-RC-Car.git](https://github.com/dharmikyash7118/Self-Driving-RC-Car.git "Self-Driving RC Car Repository")
   cd Self-Driving-RC-Car
   ```

2. **Run the main script:**

   ```bash
   python3 main.py
   ```

##  Chassis Design

The chassis was custom designed and **3D printed using ABS** for heat resistance and durability.

*  **Steering Mechanism:** The vehicle utilizes a **parallel Ackerman steering geometry**. 

 The SG90 servo acts as the direct actuator, connected to C-shaped clamp assemblies. These clamps house the wheel hubs (bolts) and bearings, ensuring smooth rotation. The servo is programmed to operate within a range of $\pm30^{\circ}$ relative to the center position (moving between $60^{\circ}$ and $120^{\circ}$) to provide precise directional control.
*  **Camera Mount:** A custom **3D-printed stand** positions the camera **22.5 cm** above the chassis base. It is fixed at a precise tilt angle of $19.98^{\circ}$ to optimize the field of view for lane detection.
*  **Sensor Mounts:** Dedicated front-facing mount for the HC-SR04 Ultrasonic sensor.

##  Future Work

Areas identified for continuous improvement:

1. First ordered list item: **PID Control**
   * Implementing a closed-loop PID controller for smoother, more stable steering correction (instead of simple Proportional control).
2. Another item: **IMU Fusion**
   * Adding an **MPU-6050** for orientation feedback to prevent drift.
3. Actual numbers don't matter, just that it's a number: **Deep Learning**
   * Replacing threshold-based CV with a **CNN (like YOLO)** for object classification (e.g., Stop signs, pedestrians).
4. And another item: **ROS Integration**
   * Migrating the software stack to **Robot Operating System (ROS)** for better modularity.





