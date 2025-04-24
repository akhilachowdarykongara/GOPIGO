# 🤖 Smart GoPiGo3 Robot System

Welcome to the **Smart GoPiGo3 Robotics Suite**, an advanced Raspberry Pi-based robotic system powered by Python, computer vision, and sensor intelligence. This repository showcases a multi-threaded, AI-enhanced robot capable of:

- Real-time object detection with OpenCV and scikit-learn.
- Distance-based navigation with obstacle avoidance.
- Voice feedback and alerts using `espeak` and a buzzer.
- Seamless image and video capture with PiCamera.
- Autonomous decision-making with safety thresholds.

## 📸 Features

### 1. **Vision System**
- Uses PiCamera to capture images and video at runtime.
- Applies KMeans clustering to identify a target color (e.g., white).
- Estimates distance from detected objects using area-based heuristics.
- Annotates processed frames with bounding boxes and distance overlays.

### 2. **Obstacle Avoidance**
- Continuously reads from multiple distance sensors (center, left, right).
- Automatically reroutes on detecting close-range obstacles.
- Moves strategically forward, backward, or turns based on distance readings.

### 3. **Speech and Alerts**
- Verbally announces robot actions (`espeak`) like "Moving forward", "Turning left".
- Buzzer alerts are triggered during directional changes or obstacle events.
- Button press acts as an emergency stop mechanism.

### 4. **Threaded Architecture**
- Separate threads for:
  - Image processing (vision).
  - Navigation and movement logic.
- Thread-safe image queue using `queue.Queue` and `threading.Lock`.

## 🚀 How It Works

1. **Initialization**:
   - GoPiGo3, sensors (I2C/AD), camera, and peripherals are initialized.
   - A directory for storing video (`robot_images`) is created if not present.

2. **Processing Loop**:
   - Camera starts capturing frames.
   - Frames are enqueued to a vision processing thread.
   - KMeans clustering detects target colors and estimates distance.
   - Based on color and proximity, movement logic executes appropriate responses.

3. **Safety Checks**:
   - If the robot approaches an object too closely, it reroutes and announces its movement.
   - Button can be used to stop robot operation immediately.

## 🧠 Tech Stack

| Technology        | Purpose                                 |
|------------------|-----------------------------------------|
| Python 3          | Main programming language               |
| PiCamera          | Image and video capture                 |
| OpenCV + PIL      | Image processing and annotation         |
| KMeans (sklearn)  | Color clustering and detection          |
| EasyGoPiGo3       | GoPiGo3 motor and sensor interface      |
| Espeak            | Voice feedback engine                   |
| ffmpeg (optional) | For video format conversion             |
| threading/queue   | Multi-threaded data processing          |

## 📂 Project Structure

```bash
.
├── Camera.py               # Basic PiCamera test script
├── video.py                # Full-featured image processing and navigation script
├── obstacle_voice_bot.py   # Voice-controlled robot with button + sensor logic
└── README.md               # You're here!
