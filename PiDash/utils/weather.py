import requests
import time

def get_weather(lat, lon):
    """
    https://api.weather.gov/points/{lat},{lon}/forecast
    """
    try:
        # Step 1: 获取对应的 forecast URL
        meta_url = f"https://api.weather.gov/points/{lat},{lon}"

        meta_resp = requests.get(meta_url, timeout=5)

        meta_resp.raise_for_status()
        forecast_url = meta_resp.json()["properties"]["forecast"]
        dayforecast_url = forecast_url.replace("forecast", "forecast/hourly")
   
        # Step 2: 获取天气预报
        forecast_resp = requests.get(forecast_url, timeout=5)
        dayforecast_resp = requests.get(dayforecast_url, timeout=5)
        forecast_resp.raise_for_status()
        dayforecast_resp.raise_for_status()
        forecast_data = forecast_resp.json()
        dayforecast_data = dayforecast_resp.json()
        
        print(dayforecast_data)

        # 获取最近的预报信息
        period = forecast_data["properties"]["periods"][0]

        # 获取最高气温和最低气温
        temperatures = [p["temperature"] for p in dayforecast_data["properties"]["periods"]]
        highest_temp = max(temperatures)
        lowest_temp = min(temperatures)

        # 返回天气数据
        return {
            "name": period["name"],
            "temperature": period["temperature"],
            "unit": period["temperatureUnit"],
            "detailedForecast": period["detailedForecast"],
            "windSpeed": period["windSpeed"],
            "shortForecast": period["shortForecast"],
            "icon": period["icon"],
            "highest_temperature": highest_temp,
            "lowest_temperature": lowest_temp
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
