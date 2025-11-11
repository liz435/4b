from google.transit import gtfs_realtime_pb2
import requests, datetime

def get_mta_status(stop_id="L20S"):
    """
    Jefferson St = L20
    L20S: southbound (to Canarsie)
    L20N: northbound (to 8 Av)
    """
    url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l"
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url, timeout=5)
    feed.ParseFromString(response.content)

    arrivals = []
    for entity in feed.entity:
        if entity.HasField("trip_update"):
            for update in entity.trip_update.stop_time_update:
                if update.stop_id == stop_id and update.arrival.time:
                    arrival = datetime.datetime.fromtimestamp(update.arrival.time)
                    minutes = int((arrival - datetime.datetime.now()).total_seconds() // 60)
                    if minutes >= 0:
                        arrivals.append(minutes)
    return sorted(arrivals)[:5]
