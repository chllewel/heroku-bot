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
import json

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
        with open("gsrCard.json","r") as f:
            card = f.read()
            f.close()
        card = json.loads(card)

        raw_json = request.get_json()

        print(raw_json)

        if raw_json['eventType'] == 'ALERT_NOTIFICATION_CLEAR':
            card['body'][0]['items'][0]['text'] = "Latency Alert Cleared!"
            card['body'][1]['items'][0]['text'] = "ThousandEyes Alert has cleared for {ruleExpression} for {testName}".format(ruleExpression=raw_json['alert']['ruleExpression'], testName=raw_json['alert']['testName'])
            card['body'][2]['items'][0]['items'][0]['items'][0]['items'][2]['text'] = "Alert Triggered by {agentName} on {testTargetDescription}".format(agentName=raw_json['alert']['agents'][0]['agentName'],testTargetDescription=raw_json['alert']['testTargetDescription'][0])
            card['body'][2]['items'][0]['items'][0]['items'][0]['items'][4]['inlines']['text'] = raw_json['alert']['permalink']

            api.messages.create(roomId=WT_ROOM_ID, attachments=card)

            return jsonify({'success': True})
        elif raw_json['eventType'] == 'ALERT_NOTIFICATION_TRIGGER':
            card['body'][1]['items'][0]['text'] = "ThousandEyes has detected {ruleExpression} for {testName}".format(ruleExpression=raw_json['alert']['ruleExpression'],testName=raw_json['alert']['testName'])
            card['body'][2]['items'][0]['items'][0]['items'][0]['items'][2]['text'] = "Alert Triggered by {agentName} on {testTargetDescription}".format(agentName=raw_json['alert']['agents'][0]['agentName'], testTargetDescription=raw_json['alert']['testTargetDescription'][0])
            card['body'][2]['items'][0]['items'][0]['items'][0]['items'][4]['inlines']['text'] = raw_json['alert']['permalink']

            api.messages.create(roomId=WT_ROOM_ID, attachments=card)


            return jsonify({'success': True})


if __name__=="__main__":
    app.run(debug=True)