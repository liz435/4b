from google.transit import gtfs_realtime_pb2
import requests, datetime
import openai

def get_mta_status(stop_id="L15S"):
    """
    Jefferson St = L15
    L15S: southbound (to Canarsie)
    L15N: northbound (to 8 Av)
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

# Function to interact with OpenAI API
def query_openai(prompt, model="gpt-3.5-turbo", max_tokens=100):
    """
    Query the OpenAI API with a given prompt.

    Args:
        prompt (str): The input prompt to send to the OpenAI API.
        model (str): The model to use for the query (default: gpt-3.5-turbo).
        max_tokens (int): The maximum number of tokens to return (default: 100).

    Returns:
        str: The response text from the OpenAI API.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error querying OpenAI API: {e}")
        return None
