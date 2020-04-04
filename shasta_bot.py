import tweepy, json, time, requests
from config import create_api
from pyowm import OWM
from keys import WEATHERBIT_IO_KEY, LATITUDE, LONGITUDE
from emoji import *

def check_mentions(api, since_id):
    print("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        # Follow back
        if not tweet.user.following:
            tweet.user.follow()
        var = get_weather()
        api.update_with_media('mtshasta.jpg',f"{tweet.user.name} Hi!. {var}", in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
    return new_since_id

def get_weather():
    url = f"https://api.weatherbit.io/v2.0/current?key={WEATHERBIT_IO_KEY}&lat={LATITUDE}&lon={LONGITUDE}&units=I"
    data = requests.get(url).json()
    data = data['data'][0]

    temp = data['temp']
    app_temp = data['app_temp']
    description = data['weather']['description']

    # Bogus emoji
    if "snow" in description.lower():
        emoji = Snow
    elif "clear" in description.lower():
        emoji = Clear
    elif "rain" in description.lower():
        emoji = Rain
    elif "clouds" in description.lower():
        emoji = Clouds
    elif "thunderstorm" in description.lower():
        emoji = Thunderstorm
    elif "mist" in description.lower():
        emoji = Mist
    elif "haze" in description.lower():
        emoji = Haze
    else:
        emoji = notsure

    tweet = f"It's {temp}{degree_sign}F, feeling like {app_temp}{degree_sign}F. {description} {emoji}"
    return tweet

def post_weather(api):
    tweet = get_weather()
    try:
        api.update_status(status=tweet)
    except tweepy.TweepError as error:
        if error.api_code == 187:
            api.update_status(f"The weather has not changed {notsure}.")
            print("The weather has not changed")
        else:
           raise error
    print("Weather Updated")


def main():
    api = create_api()
    since_id = 1
    exec = ["0800", "1200", "1600", "1900", "2200"]
    while True:
        if time.strftime("%H%M") in exec:
            post_weather(api)
        since_id = check_mentions(api, since_id)
        # Check mentions every minute
        time.sleep(60)

if __name__ == "__main__":
    main()
