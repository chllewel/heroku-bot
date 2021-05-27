"""
Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from flask import Flask, request, jsonify
from webexteamssdk import WebexTeamsAPI
import os

# get environment variables
WT_BOT_TOKEN = os.environ['WT_BOT_TOKEN']

# uncomment next line if you are implementing a notifier bot
WT_ROOM_ID = os.environ['WT_ROOM_ID']

# uncomment next line if you are implementing a controller bot
#WT_BOT_EMAIL = os.environ['WT_BOT_EMAIL']

# start Flask and WT connection
app = Flask(__name__)
api = WebexTeamsAPI(access_token=WT_BOT_TOKEN)


@app.route('/',methods=['GET'])
def index():
    return """
    Hello world!
    
    This is a webhook receiver
    """

# defining the decorater and route registration for incoming alerts
@app.route('/webhook/alert/latency', methods=['POST','GET'])
def alert_received():
    if request.method == 'POST':
        raw_json = request.get_json()
        print(raw_json)

        # customize the behaviour of the bot here
        message = raw_json

        # uncomment if you are implementing a notifier bot
        api.messages.create(roomId=WT_ROOM_ID, markdown="```python %s ```"%message)


        return jsonify({'success': True})
    else:
        message="Test"
        api.messages.create(roomId=WT_ROOM_ID, markdown=message)
        return """This is the get request for the webhook"""

if __name__=="__main__":
    app.run(debug=True)