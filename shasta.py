import tweepy, json
import requests
from pyowm import OWM
from keys import *
from emoji import *

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

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

api.update_status(status=tweet)
