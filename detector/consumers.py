from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import google.generativeai as genai
import dotenv
import os
import re
from .models import CallLog
dotenv.load_dotenv()

snippet = "hello world"

def ask_gemini(snippet, context):
    genai.configure(api_key=os.getenv('api_key'))
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    prompt = f'''
Analyze the following snippet from a call with an unknown caller ID. Use your expertise regarding scam calls, phishing methods, and conversational behavior to evaluate the snippet. I also want you to provide a confidence level for your evaluation based on the sentence and past context.

Snippet:
"{snippet}"
Context:
"{context}"

Instructions:
1. Analyze the snippet for any signs of suspicious behavior, such as requests for sensitive information, creation of urgency, or manipulation tactics.
2. Consider what the caller might be attempting to achieve based on the content of the snippet.
3. Each message will either start with "User is speaking -" or "Caller is speaking - ". Take into account who is speaking and update your impression based on the new context.
4. Provide a statement formatted as: "This activity is [suspicious/safe] because [reason]."
5. Offer a recommendation based on your evaluation. Ensure the recommendation is concise, actionable, and appropriate to the situation, addressing how the user should respond.
6. Offer a confidence level for your evaluation, 0-100%
Your response must be structured like this:
{{
  "evaluation": "This activity is [suspicious/safe] because [reason]",
  "recommendations": "Your recommendation in a smooth and natural sentence, providing clear next steps for the user."
  "confidence_level": "Your confidence level for your evaluation, 0-100%"
}}
'''
    
    response = model.generate_content(prompt)
    return response.text

context=[""]
lastConfidence=[""]
class CallMonitorConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("WebSocket connecting...")
        context[0]=""
        lastConfidence[0]=""
        await self.accept()
        print("WebSocket connected!")

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected with code: {close_code}")

    async def receive(self, text_data):
        print(f"Received message: {text_data}")
        print(context)
        try:
            data = json.loads(text_data)
            command = data.get('command')

            if command == 'stop':
                # Create new CallLog entry
                await database_sync_to_async(CallLog.objects.create)(
                    call_log=context[0],
                    confidence_level=int(lastConfidence[0][:-1]),
                    user=self.scope["user"]
                )
                print("HEFHESIFHOESI")
                context[0]=""
                lastConfidence[0]=""
            elif command == 'start':
                sentence = data.get('context')
                print(sentence,1)
                context[0]+=sentence+"\n"
            elif command == 'mute':
                print(1)
                sentence = data.get('context')
                print(sentence,2)
                print(2)
                gemResponse = ask_gemini(sentence, context[0])
                for i in range(len(gemResponse)):
                    if gemResponse[i]=="{":
                        gemResponse=gemResponse[i:]
                        break
                for i in range(len(gemResponse)-1,-1,-1):
                    if gemResponse[i]=="}":
                        gemResponse=gemResponse[:i+1]
                        break
                try:
                    gemResponse = json.loads(gemResponse)
                except Exception as e:
                    pass
                response=""
                context[0]+= sentence+"\n"
                print(context[0])
                print(type(gemResponse))
                for i in gemResponse:
                    response+=" " + gemResponse[i]
                    if i=="confidence_level":
                        lastConfidence[0]=gemResponse[i]
                    print(4)
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': response
                }))

        except Exception as e:
            print(f"Error: {str(e)}")
