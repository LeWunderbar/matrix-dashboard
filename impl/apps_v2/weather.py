from PIL import Image, ImageFont, ImageDraw
import os
import time
from InputStatus import InputStatusEnum
from datetime import datetime
from dateutil import tz
from ast import literal_eval

class WeatherScreen:
    def __init__(self, config, modules, default_actions):
        self.modules = modules
        self.default_actions = default_actions
        self.font = ImageFont.truetype("fonts/tiny.otf", 5)

        self.canvas_width = config.getint('System', 'canvas_width', fallback=64)
        self.canvas_height = config.getint('System', 'canvas_height', fallback=32)
        self.icons = generateIconMap()

        self.text_color = literal_eval(config.get('Weather Screen', 'text_color', fallback="(255,255,255)"))
        self.low_color = literal_eval(config.get('Weather Screen', 'low_color', fallback="(255,255,255)"))
        self.high_color = literal_eval(config.get('Weather Screen', 'high_color', fallback="(255,255,255)"))

        self.temp_type = config.get('OWM', 'type', fallback="fahrenheit")

    def generate(self, isHorizontal, inputStatus):
        if inputStatus is InputStatusEnum.SINGLE_PRESS:
            self.default_actions['toggle_display']()
        elif inputStatus is InputStatusEnum.ENCODER_INCREASE:
            self.default_actions['switch_next_app']()
        elif inputStatus is InputStatusEnum.ENCODER_DECREASE:
            self.default_actions['switch_prev_app']()

        frame = Image.new("RGB", (self.canvas_width, self.canvas_height), (0,0,0))
        weather_module = self.modules['weather']
        weather = weather_module.getWeather()

        if weather is not None:
            # Current weather only (no forecast or sunrise/sunset)
            curr_temp = round(weather.temperature(self.temp_type)['temp'])
            humidity = weather.humidity
            weather_icon_name = weather.weather_icon_name
            wind_speed = round(weather.wind()['speed'] * 3.6)  # Convert m/s to km/h
            pollution_index = weather_module.getPollution()

            draw = ImageDraw.Draw(frame)

            # Display Temp, Wind, Pollution, Humidity
            draw.text((3, 3), f"TEMP {curr_temp}°C", self.text_color, font=self.font)
            draw.text((3, 10), f"WIND {wind_speed}", self.text_color, font=self.font)
            if pollution_index is not None:
                draw.text((3, 17), f"AQI  {pollution_index}", self.text_color, font=self.font)
            draw.text((3, 24), f"HUMIDITY {humidity}%", self.text_color, font=self.font)

            # Weather icon
            if weather_icon_name in self.icons:
                frame.paste(self.icons[weather_icon_name], (40, 1))

        return frame

def generateIconMap():
    icon_map = dict()
    for _, _, files in os.walk("apps_v2/res/weather"):
        for file in files:
            if file.endswith('.png'):
                icon_map[file[:-4]] = Image.open('apps_v2/res/weather/' + file).convert("RGB")
    return icon_map

def convertToTwoDigits(num):
    if num < 10:
        return '0' + str(num)
    return str(num)