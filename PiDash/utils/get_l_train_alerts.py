import requests

def get_l_train_alerts():
    url = "https://api.mta.info/service-alerts/v2/alerts/route/L"
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        alerts = []
        for a in data.get("alerts", []):
            header = a.get("header_text", {}).get("translation", [{}])[0].get("text", "")
            desc = a.get("description_text", {}).get("translation", [{}])[0].get("text", "")
            if header or desc:
                alerts.append(f"**{header}** — {desc}")
        return alerts
    except Exception as e:
        print("Error fetching alerts:", e)
        return []
