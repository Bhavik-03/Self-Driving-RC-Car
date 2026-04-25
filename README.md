# Autonomous RC Car (Raspberry Pi)

## Overview
Real-time autonomous RC car capable of lane detection and steering control using OpenCV on Raspberry Pi. The system processes live camera input to detect lane boundaries and adjusts steering dynamically for stable navigation.

## Video link of car working : 
https://youtube.com/shorts/Uuat53RBruc?si=H6TtnL0lAqo2MNvh
- Achieves ~20+ FPS real-time performance on Raspberry Pi


## My Contribution
- Implemented a real-time lane detection pipeline using Canny Edge Detection and Hough Transform  
- Optimized image processing pipeline to achieve ~20+ FPS on Raspberry Pi  
- Developed smooth servo control for steering using proportional adjustment to reduce abrupt motion  
- Reduced processing latency by ~40% through ROI masking and frame resizing  
- Improved overall system responsiveness and control stability  

## Tech Stack
- Python  
- OpenCV  
- Raspberry Pi  
- Embedded Systems  

## Features
- Real-time lane detection using classical computer vision  
- Autonomous steering control based on lane deviation  
- Optimized pipeline for low-power embedded hardware  
- Smooth steering for stable navigation  

## Results
- Achieved stable lane tracking at ~20+ FPS on live video feed  
- Reduced latency by ~40%, enabling faster response to lane changes  

## Note
This repository is a fork of an existing project. My contributions focus on improving performance, optimizing the vision pipeline, and enhancing steering control logic.
