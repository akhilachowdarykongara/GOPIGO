#Here is the code which operates a GoPiGo3 robot, enabling movement, obstacle detection, and voice feedback via a speaker. The robot moves forward while a distance sensor monitors for obstacles; if one is too close, it stops and randomly turns left, right, or moves backward. A buzzer emits sound alerts, and a speaker (espeak) announces actions like movement and stopping. Pressing a button halts the robot, with built-in error handling for stability. The loop continues running until manually stopped or interrupted by a button press.

import time
import random
import easygopigo3 as easy
import threading
import os  # This will use system commands for speech
gpg = easy.EasyGoPiGo3()
buzzer = gpg.init_buzzer("AD2")
button = gpg.init_button_sensor("AD1")
servo = gpg.init_servo("SERVO2")
try:
    my_distance_sensor = gpg.init_distance_sensor("I2C")
    print("Distance sensor initialized successfully.")
except Exception as e:
    my_distance_sensor = None
    print(f" Error initializing distance sensor: {e}")
def speak(message):
    os.system(f'espeak "{message}" --stdout | aplay')
def beep():
    buzzer.sound(1000)  
    time.sleep(0.2)  
    buzzer.sound_off()
def move_forward():
    speak("Moving forward")
    print(" Moving forward.")
    gpg.forward()
def stop():
    speak("Stopping")
    print(" Stopping the robot.")
    gpg.stop()
def turn_left():
    speak("Turning left")
    print("Turning left.")
    servo.rotate_servo(90)  
    gpg.left()
    beep()  
    time.sleep(1)  
    gpg.stop()
    servo.rotate_servo(0)  
def turn_right():
    speak("Turning right")
    print(" Turning right.")
    servo.rotate_servo(-90)
    gpg.right()
    beep()  
    time.sleep(1)  
    gpg.stop()
    servo.rotate_servo(0)  
def move_backward():
    speak("Moving backward")
    print(" Moving backward.")
    gpg.backward()
    beep()  
    time.sleep(1)
    gpg.stop()
def is_button_pressed():
    if button.read() == 1:
        time.sleep(0.2)
        if button.read() == 1:
            return True
    return False
# Main loop
try:
    while True:
        if is_button_pressed():
            print(" Button pressed! Stopping robot.")
            stop()
            break  
        move_forward()
        if my_distance_sensor:
            try:
                distance = my_distance_sensor.read_mm()
                if distance is None or distance <= 0:
                    print(" Invalid distance reading! Retrying...")
                    continue
               
                print(f" Distance Sensor Reading: {distance} mm")
               
                if distance < 100:  # Obstacle detected at less than 100mm
                    print(f" Obstacle detected at {distance} mm!")
                    stop()
                    time.sleep(1)
                    action = random.choice(["left", "right", "backward"])
                    if action == "left":
                        turn_left()
                    elif action == "right":
                        turn_right()
                    else:
                        move_backward()
                    time.sleep(2)
            except Exception as e:
                print(f"Distance sensor error: {e}")
        time.sleep(0.05)  # Faster response time
except KeyboardInterrupt:
    print(" Program terminated.")
    stop()

