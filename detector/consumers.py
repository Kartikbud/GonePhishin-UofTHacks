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

knowledge_base_json = str(
{
  "strategies": {
    "request_for_verbal_confirmation": {
      "description": "The caller tries to get you to say 'yes' or another affirmative response, potentially to record it for fraudulent purposes.",
      "examples": ["Hello, can you hear me?", "Is this [your name]?", "Are you the account owner?"],
      "recommended_action": "Acknowledge neutrally, such as saying 'I can hear you,' without using the word 'yes.'"
    },
    "creating_a_sense_of_urgency": {
      "description": "Callers create pressure by claiming immediate consequences if action isn't taken.",
      "examples": ["Your account will be suspended unless you act now!", "Pay your overdue bill immediately to avoid penalties."],
      "recommended_action": "Stay calm, do not provide information, and verify claims directly with the alleged organization using official contact methods."
    },
    "mention_of_names": {
      "description": "The caller mentions a name, which could be yours, a family member’s, or a trusted entity, to build trust or manipulate the conversation.",
      "examples": ["Hi [your name], this is John from your bank.", "Your nephew [name] is in trouble and needs your help."],
      "recommended_action": "If you recognize the name, proceed with caution. Verify the authenticity of the caller through an independent and trusted method, but do not immediately disregard the call based solely on the familiarity of the name."
    },
    "unsolicited_offers": {
      "description": "Scammers offer prizes, loans, or rewards to lure victims into providing sensitive information or making payments.",
      "examples": ["You’ve won a prize! Just pay a small fee to claim it.", "We’re offering low-interest loans with no credit checks."],
      "recommended_action": "Politely decline and do not provide any payment or personal information. Research the offer independently if interested."
    },
    "imposter_claims": {
      "description": "The caller pretends to be from a trusted organization to gain your confidence and request sensitive data.",
      "examples": ["This is the IRS. You owe taxes and must pay immediately.", "I’m calling from your bank to verify suspicious transactions."],
      "recommended_action": "Do not share personal information. Contact the organization directly through a verified phone number to confirm the claim."
    },
    "technical_support_scam": {
      "description": "The caller claims your device is compromised and offers to fix it by gaining remote access or requesting payment.",
      "examples": ["Your computer has a virus. Let us access it remotely to fix the issue.", "Your device warranty has expired. Renew it now to stay protected."],
      "recommended_action": "Do not grant access or make payments. Contact your device manufacturer or service provider directly for support."
    },
    "family_emergency_scam": {
      "description": "The caller impersonates a family member or friend in distress, requesting immediate financial help.",
      "examples": ["It’s your grandson. I’m in trouble and need money urgently.", "I’ve been arrested abroad; please send bail money."],
      "recommended_action": "Verify the caller's identity by asking questions only they would know or contacting them directly through a known phone number."
    },
    "lottery_or_prize_scam": {
      "description": "The caller claims you’ve won a lottery or prize and requests a fee or sensitive details to claim it.",
      "examples": ["Congratulations! You’ve won a car. Pay the registration fee to claim it.", "You’ve been selected for a free vacation. Provide your credit card for booking."],
      "recommended_action": "Do not share personal details or make payments. Legitimate lotteries do not require upfront fees to claim prizes."
    },
    "caller_id_spoofing": {
      "description": "Scammers fake caller IDs to impersonate legitimate sources or local numbers.",
      "examples": ["The caller ID shows your bank’s name, but the caller requests sensitive details.", "The number looks local, but the caller speaks about unrelated topics."],
      "recommended_action": "Do not rely on caller ID for verification. Independently contact the organization or person through trusted channels."
    },
    "charity_scam": {
      "description": "The caller claims to represent a charity and requests donations, often exploiting recent events to appear legitimate.",
      "examples": ["We’re raising money for disaster relief. Can we count on your support?", "Help injured veterans with a small donation today."],
      "recommended_action": "Research the charity independently through trusted platforms like Charity Navigator before donating."
    },
    "investment_scam": {
      "description": "The caller offers high-return investment opportunities, often in cryptocurrency, stocks, or real estate.",
      "examples": ["Earn 20% returns monthly with our exclusive crypto investment platform!", "Invest in this real estate project for guaranteed profits."],
      "recommended_action": "Be skeptical of high-return promises. Research the investment thoroughly and consult a trusted financial advisor."
    },
    "legitimate_calls": {
      "description": "Genuine calls may come from legitimate organizations or individuals for valid reasons, and they typically offer identifiable and verifiable information.",
      "examples": ["A reminder call from your healthcare provider about an upcoming appointment.", "A delivery service calling to confirm a package delivery time.", "Your bank calling to verify unusual account activity."],
      "recommended_action": "Listen for professional, calm communication. Verify their claims independently using official contact methods, and avoid sharing sensitive information unless you initiated the call and trust the recipient."
    }
  },
  "case_scenarios": [
    {
      "scenario": "The caller says, 'Hello, can you hear me?'",
      "analysis": "The caller may be attempting to elicit a 'yes' response for misuse.",
      "recommended_action": "Respond neutrally with 'I can hear you' and avoid saying 'yes.'"
    },
    {
      "scenario": "The caller says, 'Hi [your name], this is John from your bank. There’s an issue with your account.'",
      "analysis": "The mention of your name may build trust, but the request could still be fraudulent.",
      "recommended_action": "Even if you recognize the name, verify their authenticity by contacting your bank directly using an official phone number."
    },
    {
      "scenario": "The caller claims you’ve won a prize and asks for your credit card to pay a fee.",
      "analysis": "The caller is likely running a prize scam that requires upfront payment.",
      "recommended_action": "Decline the offer and do not provide payment or personal details."
    },
    {
      "scenario": "The caller claims to be your grandson and asks for money to get out of jail.",
      "analysis": "The caller is likely impersonating a family member in distress to exploit your emotions.",
      "recommended_action": "Verify their identity by asking questions only they would know or contacting them directly through a known phone number."
    },
    {
      "scenario": "The caller claims to be from Microsoft and requests remote access to fix a virus on your computer.",
      "analysis": "This is likely a technical support scam attempting to gain control of your device.",
      "recommended_action": "Refuse remote access and contact your device manufacturer or trusted tech support directly."
    },
    {
      "scenario": "The caller is a delivery service confirming your package details.",
      "analysis": "This may be a legitimate call to ensure a smooth delivery.",
      "recommended_action": "Confirm only basic details, like the delivery time or partial address, and avoid sharing sensitive information. Call the service provider back through their official number if unsure."
    },
    {
      "scenario": "The caller identifies themselves as your doctor’s office to remind you about an appointment.",
      "analysis": "This is likely a legitimate call providing helpful information.",
      "recommended_action": "Note the details and verify with the clinic if you have doubts."
    }
  ]
}
)


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
    prompt = f'''
Analyze the following snippet from a call with an unknown caller ID. Use your expertise regarding scam calls, phishing methods, and conversational behavior to evaluate the snippet. Additionally, reference the provided JSON knowledge base ("knowledge_base_json") to enhance your analysis, but rely on your judgment and reasoning when the scenario is not explicitly covered.

Knowledge Base (for reference):
{knowledge_base_json}

Snippet:
"{snippet}"
Context:
"{context}"

Instructions:
Analyze the snippet for suspicious behavior, such as requests for sensitive information, urgency, or manipulation tactics.
Reference the knowledge base to inform your evaluation if applicable. If not explicitly covered, use your expertise to evaluate the snippet.
Provide a concise response that includes an evaluation and recommendation in one sentence. Format it as: "This activity is [suspicious/safe] because [reason], so [recommendation]."
Include a confidence level for your evaluation as a percentage (0-100%).

Your response must be structured like this:
{{
  "response": "This activity is [suspicious/safe] because [reason], so [recommendation].",
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
