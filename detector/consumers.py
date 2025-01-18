from channels.generic.websocket import AsyncWebsocketConsumer
import json
import google.generativeai as genai
import dotenv
import os
dotenv.load_dotenv()

snippet = "hello world"

def ask_gemini(snippet):
    genai.configure(api_key=os.getenv('api_key'))
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    prompt = f'''
Analyze the following snippet from a call with an unknown caller ID. Use your expertise regarding scam calls, phishing methods, and conversational behavior to evaluate the snippet. 

Snippet:
"{snippet}"

Instructions:
1. Analyze the snippet for any signs of suspicious behavior, such as requests for sensitive information, creation of urgency, or manipulation tactics.
2. Consider what the caller might be attempting to achieve based on the content of the snippet.
3. Provide a statement formatted as: "This activity is [suspicious/safe] because [reason]."
4. Offer a recommendation based on your evaluation. Ensure the recommendation is concise, actionable, and appropriate to the situation, addressing how the user should respond.

Your response must be structured like this:
{{
  "evaluation": "This activity is [suspicious/safe] because [reason]",
  "recommendations": "Your recommendation in a smooth and natural sentence, providing clear next steps for the user."
}}
'''
    
    response = model.generate_content(prompt)
    return response.text

print(ask_gemini(snippet))

class CallMonitorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connecting...")
        await self.accept()
        print("WebSocket connected!")

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected with code: {close_code}")

    async def receive(self, text_data):
        print(f"Received message: {text_data}")
        try:
            data = json.loads(text_data)
            command = data.get('command')
            print(f"Received command: {command}")

            if command == 'start':
                pass
            elif command == 'stop':
                pass
            elif command == 'mute':
                pass

        except Exception as e:
            print(f"Error: {str(e)}") 