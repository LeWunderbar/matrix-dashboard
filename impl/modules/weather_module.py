from pyowm.owm import OWM
from threading import Thread
from queue import LifoQueue
import time
import requests

class WeatherModule:
    def __init__(self, config):
        self.current_weather = None
        self.pollution_index = None
        self.queue = LifoQueue()

        if (config is not None and 'OWM' in config and 'token' in config['OWM']
            and config['OWM']['token'] != "" and 'lat' in config['OWM'] and 'lon' in config['OWM']):
            self.mgr = OWM(config['OWM']['token']).weather_manager()
            self.api_key = config['OWM']['token']
            self.lat = float(config['OWM']['lat'])
            self.lon = float(config['OWM']['lon'])
            self.thread = Thread(
                target=update_weather,
                args=(self, self.mgr, self.queue, self.lat, self.lon, self.api_key)
            )
            self.thread.start()
        else:
            print("[Weather Module] Empty OWM API Token")

    def getWeather(self):
        if not self.queue.empty():
            data = self.queue.get()
            self.current_weather = data.get('weather')
            self.pollution_index = data.get('pollution')
            self.queue.queue.clear()
        return self.current_weather

    def getPollution(self):
        return self.pollution_index

def update_weather(weather_module, mgr, weather_queue, lat, lon, api_key):
    lastTimeCall = 0
    while True:
        currTime = time.time()
        if (currTime - lastTimeCall >= 600):  # Update every 10 minutes
            try:
                # Get current weather
                observation = mgr.weather_at_coords(lat, lon)
                weather = observation.weather

                # Get pollution index
                pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
                response = requests.get(pollution_url)
                pollution_index = None
                if response.status_code == 200:
                    data = response.json()
                    pollution_index = data['list'][0]['main']['aqi']  # 1-5

                weather_queue.put({
                    'weather': weather,
                    'pollution': pollution_index
                })
                lastTimeCall = currTime
            except Exception as e:
                print("Weather update error:", e)
            time.sleep(1)  # Avoid busy waiting