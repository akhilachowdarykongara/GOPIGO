import time
import picamera
import numpy as np
import threading
import queue
import io
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans
from IPython.display import display, clear_output
import easygopigo3 as easy
import subprocess  # To run ffmpeg for conversion
import os

# Create an instance of the GoPiGo3 robot
gpg = easy.EasyGoPiGo3()

# Sensors initialization
left_sensor = gpg.init_distance_sensor(port="I2C")  # Front-left corner sensor
right_sensor = gpg.init_distance_sensor(port="AD1")  # Front-right corner sensor
center_sensor = gpg.init_distance_sensor(port="I2C")  # Front-center sensor

# Parameters
target_color = np.array([255, 255, 255])  # Target color (white)
border_color = np.array([0, 255, 0])       # Border color (green)
color_threshold = 0.07                      # Color detection threshold
max_distance = 100                          # Maximum distance in some units (e.g., cm)
min_distance = 10                           # Minimum distance in some units (e.g., cm)
safe_distance = 20                          # Safety distance threshold (in cm)
run_duration = 30                            # Duration to run the robot in seconds

def resizeNPArray(array, width, height):
    """ Function to resize a given numpy array to another width/height. """
    img = Image.fromarray(array)
    img = img.resize((width, height), Image.ANTIALIAS)
    resized = np.asarray(img)
    return resized

class ImageProcessor(threading.Thread):
    """ Thread-safe class to process a stream of jpeg sequences from a given queue. """
    def __init__(self, thread_stopper, frames, lock):
        super().__init__()
        self.thread_stopper = thread_stopper
        self.frames = frames
        self.lock = lock
        self.object_detected = False

    def run(self):
        """ Main processing loop. """
        while not self.thread_stopper.is_set():
            try:
                self.lock.acquire()
                self.processed_frame = self.frames.get_nowait()
                self.frames.task_done()
            except queue.Empty:
                continue
            finally:
                self.lock.release()
            self.process_image(self.processed_frame)

    def process_image(self, array):
        """ Process the incoming image for color detection and distance estimation. """
        output = array.copy()
        array_resized = resizeNPArray(array, 80, 60)
        reshaped = array_resized.reshape((60 * 80, 3))
        kmeans = KMeans(n_clusters=6).fit(reshaped)
        labels = kmeans.labels_.reshape((60, 80))
       
        # Color detection logic
        diff = kmeans.cluster_centers_ - target_color
        closest_label = np.argmin(np.linalg.norm(diff, axis=1))
        detected_color = (labels == closest_label).astype(np.uint8)

        if np.sum(detected_color) > color_threshold * 4800:  # Check for detected area
            self.object_detected = True
            # Draw border (if color detected)
            min_y, min_x = np.min(np.nonzero(detected_color), axis=1)
            max_y, max_x = np.max(np.nonzero(detected_color), axis=1)
            output[min_y:max_y + 1, [min_x, max_x], :] = border_color
            output[[min_y, max_y], min_x:max_x + 1, :] = border_color

            # Estimate distance based on area
            area = np.sum(detected_color)
            distance_estimate = self.estimate_distance(area)
            output = self.display_distance(output, distance_estimate)

        else:
            self.object_detected = False

        # Display processed image
        showarray(output)

    def estimate_distance(self, area):
        """ Estimate distance based on the area of detected color. """
        area_min = 100  # Minimum area for distance estimation
        area_max = 4000  # Maximum area for distance estimation
       
        if area < area_min:
            return max_distance  # Too small, far away
        elif area > area_max:
            return min_distance  # Too large, too close
        else:
            # Linear interpolation between distances
            distance = min_distance + (max_distance - min_distance) * (area - area_min) / (area_max - area_min)
            return distance

    def display_distance(self, image, distance):
        """ Overlay the estimated distance on the image. """
        text = f"Estimated Distance: {distance:.2f} cm"
        image_pil = Image.fromarray(image)
        draw = ImageDraw.Draw(image_pil)
        draw.text((10, 10), text, fill=(255, 255, 255))  # Draw white text on the image
        return np.array(image_pil)

def showarray(a, fmt='jpeg'):
    """ Function to display an image within a Jupyter notebook. """
    f = io.BytesIO()
    Image.fromarray(a).save(f, fmt)
    img = Image.open(f)
    clear_output(wait=True)  # Clear previous output
    display(img)  # Display new image

def check_sensors():
    """ Check the distance sensors and return distances. """
    left_distance = left_sensor.read()
    right_distance = right_sensor.read()
    center_distance = center_sensor.read()
    return left_distance, right_distance, center_distance

def navigate_around_obstacles():
    """ Navigate around detected obstacles and the detected object. """
    start_time = time.time()
    while time.time() - start_time < run_duration:  # Run for the specified duration
        left_distance, right_distance, center_distance = check_sensors()

        if center_distance < safe_distance:
            print("Obstacle ahead! Turning right.")
            gpg.turn_degrees(90)  # Turn right to go around the obstacle
            time.sleep(1)  # Wait for the turn to complete
            gpg.forward()
            time.sleep(0.5)
       
        elif left_distance < safe_distance:
            print("Obstacle on the left! Turning right.")
            gpg.turn_degrees(90)  # Turn right to go around the obstacle
            time.sleep(1)
            gpg.forward()
            time.sleep(0.5)
       
        elif right_distance < safe_distance:
            print("Obstacle on the right! Turning left.")
            gpg.turn_degrees(-90)  # Turn left to go around the obstacle
            time.sleep(1)
            gpg.forward()
            time.sleep(0.5)
       
        elif imageThread.object_detected:
            print("Detected object! Moving around it.")
            gpg.forward()
            time.sleep(1)  # Move forward briefly
            gpg.turn_degrees(90)  # Turn to circle the object
            time.sleep(1)  # Adjust this duration to control the turning angle
           
        else:
            print("Moving forward.")
            gpg.forward()
            time.sleep(0.5)

# Directory where the video should be saved
video_dir = '/home/jupyter/robot_images'
video_filename = f"{video_dir}/goPiGo_video.mp4"

# Create the directory if it doesn't exist
if not os.path.exists(video_dir):
    os.makedirs(video_dir)

# Queue and threading setup
frames = queue.Queue(maxsize=10)
thread_stopper = threading.Event()
lock = threading.Lock()

# Start processing thread
imageThread = ImageProcessor(thread_stopper, frames, lock)
imageThread.start()

# Start navigation thread
navigationThread = threading.Thread(target=navigate_around_obstacles)
navigationThread.start()

# Start PiCamera and save video directly as MP4
with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.framerate = 30
    time.sleep(2)  # Allow camera to warm up

    # Start video recording directly as MP4
    camera.start_recording(video_filename, format='mp4')
    try:
        start_time = time.time()
        while time.time() - start_time < run_duration:  # Record video for the specified duration
            freshest_frame = np.empty((240, 320, 3), dtype=np.uint8)
            camera.capture_sequence([freshest_frame], use_video_port=True, format='rgb')
            lock.acquire()
            if frames.full():
                frames.get()
                frames.task_done()
            frames.put(freshest_frame)
            lock.release()
    except KeyboardInterrupt:
        pass  # Handle keyboard interrupt gracefully
   
    # Stop video recording
    camera.stop_recording()

print(f"Video saved as {video_filename}")
