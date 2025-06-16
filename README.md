# 🧬 Matrix Dashboard (Unofficial Fork)

This is an **unofficial fork** of the Matrix Dashboard project originally featured in the YouTube video by **allenslab**:  
🔗 [Watch the video here](https://youtu.be/A5A6ET64Oz8?si=lJgQuG-YSMkDBDVc)  
📁 [Original repository (unavailable)](https://github.com/allenslab)  
📁 This fork is based on [ty-porter/matrix-dashboard](https://github.com/ty-porter/matrix-dashboard)  

> **All credit goes to allenslab** for creating this awesome dashboard project.  
> I merely maintain and modify the code for my own enjoyment and personal use.

---

## 📋 Description

This project is a customizable smart dashboard designed to display time, weather, calendar events, and more — perfect for a Raspberry Pi-powered desk display or wall-mounted screen.

---

## ✨ Notable Changes in This Fork

- **🔄 Rewrote OpenWeatherMap Integration**  
  Modified the weather API logic to work with the 100% free version of OpenWeatherMap instead of using the paid One Call API 3.0.
- **🌦️ Redesigned Weather App**  
  Updated the weather display components to work with the new API structure.
- **⚙️ Updated `config-template.ini`**  
  Now includes more detailed configuration options for easier customization.
- **🔁 Added New Config Options**
  - `allow_app_rotation`: Enable or disable automatic rotation between apps.
  - `temp_unit`: Choose between Celsius or Fahrenheit.
  - `apps`: Allows the user to enable/disable apps via the config file.

---

## 🛠️ Hardware Setup

### **Connecting the Display and Components**

1. **Connect the LED Matrix Display to the Raspberry Pi**
   - **Display wiring guide:**  
     [https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/wiring.md](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/wiring.md)
   - Use the provided guide to properly connect the HUB75 connector and power supply.

2. **Connect Tilt Switch and Rotary Encoder**
   - **Default GPIO Pins (can be changed in code):**
     - **GPIO 13:** Rotary encoder Switch (SW)
     - **GPIO 5:** Rotary encoder Clock (CLK)
     - **GPIO 6:** Rotary encoder Data (DT)
     - **GPIO 16:** Tilt Switch
   - **Note:**  
     These pin assignments can be modified in the code if you wish to use different GPIO pins.

---

## 🚀 Getting Started

Check the original video or forked repo documentation for instructions on setting up the dashboard with your preferred device.

---

## 📜 License

This fork maintains the same license as the original unless otherwise stated. Use at your own discretion.

---

## 🙏 Credits

- **Original concept and code:** [allenslab](https://www.youtube.com/@allenslab)
- **Base fork:** [ty-porter](https://github.com/ty-porter/matrix-dashboard)
- **Maintained and modified by:** LeWunderbar
