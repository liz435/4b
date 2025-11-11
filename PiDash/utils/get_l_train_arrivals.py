from google.transit import gtfs_realtime_pb2
import requests, datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_l_train_arrivals(stop_ids=["L1S"]):
    """
    Fetch arrival times for multiple stop IDs from the GTFS Realtime feed.

    Args:
        stop_ids (list): List of stop IDs to fetch arrivals for.

    Returns:
        dict: A dictionary where keys are stop IDs and values are lists of arrival details.
    """
    
    url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l"

    feed = gtfs_realtime_pb2.FeedMessage()
    try:
        logging.debug("Fetching GTFS Realtime feed...")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        logging.debug(f"Raw GTFS feed response: {response.content[:500]}...")  # Log first 500 bytes of the response
        feed.ParseFromString(response.content)

        arrivals = {stop_id: [] for stop_id in stop_ids}
        logging.debug(f"Processing stop IDs: {stop_ids}")
        for entity in feed.entity:
            if entity.HasField("trip_update"):
                trip_id = entity.trip_update.trip.trip_id
                route_id = entity.trip_update.trip.route_id
                for update in entity.trip_update.stop_time_update:
                    logging.debug(f"Checking stop ID: {update.stop_id}")
                    if update.stop_id in stop_ids and update.arrival.time:
                        arrival_time = datetime.datetime.fromtimestamp(update.arrival.time)
                        minutes = int((arrival_time - datetime.datetime.now()).total_seconds() // 60)
                        if minutes >= 0:
                            arrivals[update.stop_id].append({
                                "minutes": minutes,
                                "trip_id": trip_id,
                                "route_id": route_id,
                                "arrival_time": arrival_time.strftime("%Y-%m-%d %H:%M:%S"),
                            })
        return arrivals
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return {stop_id: [] for stop_id in stop_ids}
