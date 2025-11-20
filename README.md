# Self-Driving-RC-Car
A Python-based project for building an autonomous mobile robot on a Raspberry Pi. The robot uses computer vision (OpenCV) for real-time lane detection (line following) and an ultrasonic sensor for obstacle detection and avoidance.

Integrated Control System: Combines sensing (camera, ultrasonic) and actuation (DC motors, servo) within a single Python script.

Computer Vision Navigation: Uses OpenCV for image processing (thresholding, contour analysis) and centroid calculation to find the center of the lane line.

Proportional (P-like) Control: Implements a simple P-controller for steering correction based on deviation from the lane center.

Obstacle Detection Hierarchy: Prioritized logic for safety:

Emergency Stop for very close obstacles.

Cautionary Slow-Down for intermediate obstacles.

Smooth Motion Control: Uses a software smoothing filter on the servo output to prevent jerky steering movements.



