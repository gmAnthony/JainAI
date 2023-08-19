from flask import Flask, request, jsonify, copy_current_request_context
from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter
from jain import init_pinecone, get_or_create_pinecone_data, query_pinecone
import dotenv
import threading

dotenv.load_dotenv()

app = Flask(__name__)

SLACK_BOT_TOKEN = dotenv.get_key(".env", "SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = dotenv.get_key(".env", "SLACK_SIGNING_SECRET")
SLACK_BOT_USER_ID = dotenv.get_key(".env", "SLACK_BOT_USER_ID")

slack_client = WebClient(SLACK_BOT_TOKEN)
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)


@slack_events_adapter.on("message")
def handle_message(event_data):
    @copy_current_request_context
    def process_with_context():
        process_event(event_data)

    threading.Thread(target=process_with_context).start()
    return jsonify({"status": "ok"})


def process_event(event_data):
    message = event_data["event"]
    if message.get("subtype") and message["subtype"] == "bot_message":
        print("Ignoring bot message")
        return ""

    if message.get("user") == SLACK_BOT_USER_ID:
        print("Ignoring message from myself")
        return ""

    if message.get("channel_type") == "im":
        user_query = message.get("text").strip()
        answer = query_pinecone(user_query)
        channel = message["channel"]
        slack_client.chat_postMessage(channel=channel, text=answer)


@app.route("/", methods=["GET"])
def hello():
    print("Hello!")
    return "Hello! I'm alive!"


if __name__ == "__main__":
    init_pinecone()
    get_or_create_pinecone_data()
    print("Starting server...")
    app.run(port=3000, debug=True)
