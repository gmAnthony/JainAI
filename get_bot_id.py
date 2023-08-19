from slack_sdk import WebClient
import dotenv

dotenv.load_dotenv()

SLACK_BOT_TOKEN = dotenv.get_key(".env", "SLACK_BOT_TOKEN")

slack_client = WebClient(token=SLACK_BOT_TOKEN)

response = slack_client.api_call("auth.test")

bot_id = response["user_id"]
print("Bot ID:", bot_id)
