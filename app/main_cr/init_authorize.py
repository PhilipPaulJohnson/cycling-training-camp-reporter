import requests
import datetime
import json
from init_auth_strava_vars import *
from pathlib import Path

CUR_DIR = Path(__file__).parent.absolute()

response = requests.post(url = 'https://www.strava.com/oauth/token', data = {'client_id': client_id, 'client_secret': client_secret, 'code': auth_code, 'grant_type': 'authorization_code'})
strava_tokens = response.json()
with open(CUR_DIR / 'strava_tokens.json', 'w') as outfile:
    json.dump(strava_tokens, outfile)
with open(CUR_DIR / 'strava_tokens.json') as check:
  data = json.load(check)
#print(data)
refresh_token = data.get('refresh_token')
access_token = data.get('access_token')
expires_at = data.get('expires_at')
date_time = datetime.datetime.fromtimestamp(expires_at) 

print('\n' + '(saved to strava_tokens.json)' + '\n' + 'athlete username: ' + str(data.get('athlete')['username']) + '\n' + 'refresh token: ' + str(refresh_token) + '\n' + 'access token: ' + str(access_token) + '\n' + 'access token expires at: ' + str(date_time) + '\n')
