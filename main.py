import cv2
import numpy as np
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time

# === PIN CONFIGURATION ===
SERVO_PIN = 19
# Motor A (Left)
ENA_PIN = 22
IN1_PIN = 24
IN2_PIN = 23
# Motor B (Right)
ENB_PIN = 25
IN3_PIN = 17
IN4_PIN = 27
# Ultrasonic Sensor
GPIO_TRIGGER = 18
GPIO_ECHO = 21

# === GPIO SETUP ===
GPIO.setmode(GPIO.BCM)
GPIO.setup([ENA_PIN, IN1_PIN, IN2_PIN, ENB_PIN, IN3_PIN, IN4_PIN, SERVO_PIN, GPIO_TRIGGER, GPIO_ECHO], GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN) # Re-setup Echo pin as IN

# === PWM SETUP ===
servo = GPIO.PWM(SERVO_PIN, 50)  # Servo: 50 Hz
servo.start(7.5) # Neutral

motor_left = GPIO.PWM(ENA_PIN, 1000)  # Left motor
motor_right = GPIO.PWM(ENB_PIN, 1000) # Right motor
motor_left.start(0)
motor_right.start(0)

# === CAMERA SETUP ===
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

def get_distance():
    """Measures distance using the ultrasonic sensor"""
    # Set Trigger pin to LOW
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.000002) # Small delay for sensor to settle
    
    # Set Trigger pin to HIGH for 10 microseconds
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    pulse_start = time.time()
    pulse_end = time.time()

    # Save pulse start time
    while GPIO.input(GPIO_ECHO) == 0:
        pulse_start = time.time()
    
    # Save pulse end time
    while GPIO.input(GPIO_ECHO) == 1:
        pulse_end = time.time()

    # Calculate time difference and distance
    time_elapsed = pulse_end - pulse_start
    distance = (time_elapsed * 34300) / 2 # Speed of sound in cm/s
    
    return distance

def motor_forward(speedL, speedR):
    GPIO.output(IN1_PIN, GPIO.HIGH)
    GPIO.output(IN2_PIN, GPIO.LOW)
    GPIO.output(IN3_PIN, GPIO.HIGH)
    GPIO.output(IN4_PIN, GPIO.LOW)
    motor_left.ChangeDutyCycle(speedL)
    motor_right.ChangeDutyCycle(speedR)

def motor_stop():
    motor_left.ChangeDutyCycle(0)
    motor_right.ChangeDutyCycle(0)

def set_servo_angle(angle):
    """Limit servo motion to avoid overshoot"""
    angle = max(50, min(130, angle))
    duty = (angle / 18) + 2.5
    servo.ChangeDutyCycle(duty)

def find_lane_center(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)
    height, width = thresh.shape
    roi = thresh[int(height * 0.9):, :] # ROI: bottom 40%
    contours, _ = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    lane_center = None

    if len(contours) > 0:
        largest = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            lane_center = cx
            cv2.line(image, (cx, int(height * 0.6)), (cx, height - 1), (0, 255, 0), 3)
    return lane_center, thresh

def calculate_deviation(frame_width, lane_center):
    return lane_center - (frame_width / 2)

def smooth_servo_control(target_angle, prev_angle, smoothing_factor=0.3):
    return prev_angle + smoothing_factor * (target_angle - prev_angle)
try:
    prev_angle = 90
    while True:
        # Capture camera frame at the beginning of the loop
        frame = picam2.capture_array()
        height, width, _ = frame.shape
        lane_center, mask = find_lane_center(frame)

        distance = get_distance()

        # --- Obstacle Detection Logic ---
        if distance < 15:
            motor_stop()
            servo.stop()
            print("Stopping: Obstacle detected within 15 cm!")

        elif distance < 30:
            # Slow down the car but keep following the line
            print(f"Slowing down: Obstacle at {distance:.2f} cm")
            motor_forward(15,15) # Reduced speed
            # The rest of the lane-following logic will still execute below

        else:
            # No close obstacle, proceed with normal lane-following
            if lane_center is not None:
                deviation = calculate_deviation(width, lane_center)

                # --- Steering Control ---
                k = 0.06  # Steering sensitivity
                target_angle = 90 - (deviation * k)
                smooth_angle = smooth_servo_control(target_angle, prev_angle)
                set_servo_angle(smooth_angle)
                prev_angle = smooth_angle

                # --- Speed Control based on curve ---
                if abs(deviation) > 80:
                    motor_forward(35,35) # Slower speed for sharp turns
                else:
                    motor_forward(35,35) # Normal speed for straight/mild curves
            else:
                # If no lane is detected, stop motors
                motor_stop()
        
        # Display the processed frame
        cv2.imshow("Lane Mask", mask)
        if cv2.waitKey(1) == ord('q'):
            break

except KeyboardInterrupt:
    print("Exiting safely...")

finally:
    motor_stop()
    servo.stop()
    motor_left.stop()
    motor_right.stop()
    GPIO.cleanup()
    cv2.destroyAllWindows()
