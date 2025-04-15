# 🤖 GoPiGo3 Autonomous Robot with Obstacle Avoidance & Voice Feedback

This project brings to life a **self-aware, responsive GoPiGo3 robot** powered by Python, equipped with intelligent obstacle detection, audible feedback, and autonomous navigation. The robot uses a distance sensor to monitor its path, reacts to obstacles by rerouting itself, and announces its decisions via a speaker using `espeak`. A button interface is included to halt the robot at any time, ensuring safety and control.

---

## 🚀 Key Features

- 🔄 **Autonomous Navigation**  
  Moves forward and intelligently responds to nearby obstacles with randomized maneuvers.

- 📏 **Real-Time Obstacle Detection**  
  Utilizes an I2C distance sensor to detect objects within a configurable threshold (default: 100mm).

- 🔈 **Voice Feedback**  
  Uses `espeak` to vocalize actions like "Moving forward", "Turning left", and more via system audio.

- 📣 **Auditory Alerts**  
  Buzzer emits beeps during directional changes and warnings.

- ⏹️ **Manual Stop Button**  
  A physical button allows safe interruption and halting of robot activity.

- 🛠️ **Robust Error Handling**  
  Distance sensor reads and hardware calls are wrapped in exception handling for stability.

---

## 🧩 Hardware Components

- [GoPiGo3 Robot Base](https://www.dexterindustries.com/gopigo3/)
- Distance Sensor (I2C)
- Buzzer Module (Connected to AD2)
- Button Sensor (Connected to AD1)
- Servo Motor (Connected to SERVO2)
- Speaker (for `espeak` output)

---

## 🛠️ Installation & Setup

### 🔧 Dependencies

Install required packages before running the script:

```bash
sudo apt-get update
sudo apt-get install espeak alsa-utils
