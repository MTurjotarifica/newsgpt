import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slackeventsapi import SlackEventAdapter
from flask import Flask, request, make_response
from dotenv import load_dotenv

from functions import *

import pandas as pd



load_dotenv()

# Initialize the Flask app and the Slack app
app = Flask(__name__)
slack_app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

client = slack_app.client

urls, titles, descriptions =newsapi_query()

translated_title, translated_description = newsgpt(urls, titles, descriptions)

# translated_title= translated_title[ :len(translated_description)]

# Add a route for the /hello command
@app.route("/hello2", methods=["POST"])
def handle_hello_request():
    data = request.form
    channel_id = data.get('channel_id')
    # Execute the /hello command function
    client.chat_postMessage(response_type= "in_channel", channel=channel_id, text=" 2nd it works!33!" )
    return "Hello world1" , 200

@app.route("/newsgpt", methods=["POST"])
def newsapi():
    data = request.form
    channel_id = data.get('channel_id')
    
    try:
        for i in range (len(translated_description)):
            response = client.chat_postMessage(
                        channel=channel_id,
                        text=f"• <{urls[i]}|{translated_title[i]}>\n{translated_description[i]}\n",
                        unfurl_links=False,
                    )
    except SlackApiError as e:
        print("Error sending message to Slack: {}".format(e))
                
    #returning empty string with 200 response
    return 'newsapi works', 200
        
# Start the Slack app using the Flask app as a middleware
handler = SlackRequestHandler(slack_app)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    app.run(debug=True)
