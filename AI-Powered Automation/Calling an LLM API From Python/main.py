import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

chat = client.chats.create(model="gemini-2.5-flash")

first_response = chat.send_message("I'm planning a trip to Japan. Any general tips?")
print(first_response.text)

second_response = chat.send_message("What about the best time of year to go?")
print(second_response.text)

for message in chat.get_history():
    print(message.role, ":", message.parts[0].text[:60])