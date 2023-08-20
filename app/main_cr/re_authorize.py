import requests
import time
import datetime
import json
from init_auth_strava_vars import *
from pathlib import Path

CUR_DIR = Path(__file__).parent.absolute()

with open(CUR_DIR / 'strava_tokens.json') as json_file:
    strava_tokens = json.load(json_file)
if strava_tokens['expires_at'] < time.time():
    response = requests.post(url = 'https://www.strava.com/oauth/token', data = {'client_id': client_id,'client_secret': client_secret,'grant_type': 'refresh_token','refresh_token': strava_tokens['refresh_token']})
    new_strava_tokens = response.json()
    with open(CUR_DIR / 'strava_tokens.json', 'w') as outfile:
        json.dump(new_strava_tokens, outfile)
    strava_tokens = new_strava_tokens
with open(CUR_DIR / 'strava_tokens.json') as check:
    data = json.load(check)
expires_at = data.get('expires_at')
date_time = datetime.datetime.fromtimestamp(expires_at)   
#print(data)

print('\n' + '(saved to strava_tokens.json)' + '\n' + 'refresh token: ' + str(data.get('refresh_token')) + '\n' + 'access token: ' + str(data.get('access_token')) + '\n' + 'access token expires at: ' + str(date_time) + '\n')