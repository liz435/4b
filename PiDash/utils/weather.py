import requests
import threading
import time

def get_weather(lat, lon):
    """
    获取 NOAA 天气数据
    https://api.weather.gov/points/{lat},{lon}/forecast
    """
    try:
        # Step 1: 获取对应的 forecast URL
        meta_url = f"https://api.weather.gov/points/{lat},{lon}"
        meta_resp = requests.get(meta_url, timeout=5)
        meta_resp.raise_for_status()
        forecast_url = meta_resp.json()["properties"]["forecast"]

        # Step 2: 获取天气预报
        forecast_resp = requests.get(forecast_url, timeout=5)
        forecast_resp.raise_for_status()
        forecast_data = forecast_resp.json()

        # 获取最近的预报信息
        period = forecast_data["properties"]["periods"][2]
        return {
            "name": period["name"],
            "temperature": period["temperature"],
            "unit": period["temperatureUnit"],
            "detailedForecast": period["detailedForecast"],
            "windSpeed": period["windSpeed"],
            "shortForecast": period["shortForecast"],
            "icon": period["icon"]
        }
    except Exception as e:
        print("Weather API error:", e)
        return None

def fahrenheit_to_celsius(fahrenheit):
    """
    Convert Fahrenheit to Celsius.
    Formula: (F - 32) * 5/9
    """
    return (fahrenheit - 32) * 5 / 9

# 缓存天气数据和更新时间
weather_cache = {
    "data": None,
    "last_updated": 0
}

# 更新间隔（秒）
UPDATE_INTERVAL = 600  # 10分钟

def update_weather(lat, lon):
    """
    定时更新天气数据
    """
    global weather_cache
    while True:
        weather_cache["data"] = get_weather(lat, lon)
        weather_cache["last_updated"] = time.time()
        print("Weather updated:", weather_cache["data"])
        time.sleep(UPDATE_INTERVAL)

def get_dynamic_weather():
    """
    获取动态天气数据（从缓存中获取）
    """
    global weather_cache
    return weather_cache["data"]

# 示例：启动动态天气更新线程
if __name__ == "__main__":
    latitude = 40.7128  # 示例经纬度（纽约）
    longitude = -74.0060

    # 启动更新线程
    weather_thread = threading.Thread(target=update_weather, args=(latitude, longitude), daemon=True)
    weather_thread.start()

    # 示例：每5秒获取一次动态天气数据
    while True:
        current_weather = get_dynamic_weather()
        print("Current Weather:", current_weather)
        time.sleep(5)
