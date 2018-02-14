#!/usr/bin/env python3
# Authenticate with TLOPO and then launch the client

import os
import requests
import subprocess
import urllib
from time import sleep


# ------------------------------------------------------------------------------------------
# Dict of possible responses from the API
# ------------------------------------------------------------------------------------------
responses = {0: 'An unknown error has occurred.', 1: 'The submitted Username/Password was incorrect.', 2: 'A server error has occurred.',
             3: 'This account has two-step authentication enabled.', 4: 'This account is banned or disabled.', 5: 'The server is closed.',
             6: 'This IP is banned.', 7: 'This account has successfully logged in.', 8: 'This account\'s email has not been verified.',
             9: 'This account does not have an active playtime. Deprecated--will not occur.', 10: 'This account is trying to log in too quickly.',
             11: 'This account is logging in from an unknown location.'}

# ------------------------------------------------------------------------------------------
# Authenticates with the API, asks for a gameserver/token, and then launches the client
# ------------------------------------------------------------------------------------------
username, password, user_val = "", "", ""
with open("./files/selected_account.txt", "r") as selected_user:
    for line in selected_user:
        user_val = line
with open("./files/users.csv") as users:
    for line in users:
        user_num, name, user_name, pass_word = line.split(",")
        if user_num.strip() == user_val.strip():
            username, password = user_name, pass_word

params = urllib.parse.urlencode({'username': username.strip(),
                                 'password': password.strip()})
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

r = requests.post('https://api.piratesonline.co/login/', data=params, headers=headers)
r = r.json()
#print(r)

api_response = r['status']
if not api_response == 7:
    print('Failure to connect. Error code {}.'.format(api_response))
    print(responses[api_response])
    exit()
else:
    print(responses[api_response])
sleep(3)  # Give the system a moment to brace itself for the launching of the infamous TLOPO client

os.environ['TLOPO_GAMESERVER'] = r['gameserver']
os.environ['TLOPO_PLAYCOOKIE'] = r['token']

subprocess.call('./launch_client.sh')
