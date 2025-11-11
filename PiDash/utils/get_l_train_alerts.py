from google.transit import gtfs_realtime_pb2
import requests
from datetime import datetime, timedelta
import pytz

def get_l_train_alerts(latest_only=False, route_filter="L"):
    url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts"
    feed = gtfs_realtime_pb2.FeedMessage()
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        feed.ParseFromString(r.content)

        alerts = []
        for entity in feed.entity:
            if entity.alert:
                header = entity.alert.header_text.translation[0].text if entity.alert.header_text.translation else ""
                desc = entity.alert.description_text.translation[0].text if entity.alert.description_text.translation else ""
                informed_routes = [info.route_id for info in entity.alert.informed_entity if info.route_id]
                if route_filter in informed_routes and (header or desc):
                    timestamp = entity.alert.active_period[0].start if entity.alert.active_period else 0
                    formatted_alert = f"""
 {header}
 <br>
 @{datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'N/A'}

"""
                    alerts.append({
                        "header": header,
                        "description": desc,
                        "timestamp": timestamp,
                        "formatted": formatted_alert
                    })

        # Filter alerts to only include those for today and tomorrow (New York time)
        nyc_now = datetime.now(pytz.timezone("America/New_York"))
        nyc_today = nyc_now.date()
        nyc_tomorrow = nyc_today + timedelta(days=1)

        filtered_alerts = [
            alert for alert in alerts
            if nyc_today <= datetime.fromtimestamp(alert["timestamp"], pytz.timezone("America/New_York")).date() <= nyc_tomorrow
        ]

        # Sort filtered alerts by timestamp (descending) and return the latest one if latest_only is True
        filtered_alerts.sort(key=lambda x: x["timestamp"], reverse=True)
        if latest_only:
            return [filtered_alerts[0]["formatted"], filtered_alerts[1]["formatted"]] if filtered_alerts else []
        return [alert["formatted"] for alert in filtered_alerts]
    except Exception as e:
        print("Error fetching alerts:", e)
        return []
