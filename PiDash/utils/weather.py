import requests

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
        period = forecast_data["properties"]["periods"][0]
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
