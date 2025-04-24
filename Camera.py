import picamera
import time

print("Testing basic camera functionality...")
try:
    # Initialize the camera directly
    camera = picamera.PiCamera()
    print("Camera initialized successfully using picamera library")
   
    # Set resolution
    camera.resolution = (1024, 768)
   
    # Wait for camera to initialize
    time.sleep(2)
   
    # Take a picture
    local_file = "test_direct.jpg"
    print(f"Taking photo and saving to {local_file}")
    camera.capture(local_file)
    print("Photo captured successfully!")
   
    # Clean up
    camera.close()
   
except Exception as e:
    print(f"Camera error: {e}")
