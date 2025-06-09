from pyowm.owm import OWM
from threading import Thread
from queue import LifoQueue
import time

class WeatherModule:
    def __init__(self, config):
        self.current_weather = None  # Store current weather instead of one_call
        self.queue = LifoQueue()

        if (config is not None and 'OWM' in config and 'token' in config['OWM'] 
            and config['OWM']['token'] != "" and 'lat' in config['OWM'] and 'lon' in config['OWM']):
            self.mgr = OWM(config['OWM']['token']).weather_manager()
            self.thread = Thread(
                target=update_weather,
                args=(self.mgr, self.queue, float(config['OWM']['lat']), float(config['OWM']['lon']))
            )
            self.thread.start()
        else:
            print("[Weather Module] Empty OWM API Token")

    def getWeather(self):
        if not self.queue.empty():
            self.current_weather = self.queue.get()
            self.queue.queue.clear()
        return self.current_weather

def update_weather(mgr, weather_queue, lat, lon):
    lastTimeCall = 0
    while True:
        currTime = time.time()
        if (currTime - lastTimeCall >= 600):  # Update every 10 minutes
            try:
                # Use weather_at_coords instead of one_call
                observation = mgr.weather_at_coords(lat, lon)
                weather_queue.put(observation.weather)
                lastTimeCall = currTime
            except Exception as e:
                print("Weather update error:", e)
            time.sleep(1)  # Avoid busy waiting