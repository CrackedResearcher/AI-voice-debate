import google.generativeai as genai
import markdown
from bs4 import BeautifulSoup
import time
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import requests
import re

genai.configure(api_key="")

history1 = []
history2 = []
global wholeHistory
wholeHistory = ""

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 40,
  "response_mime_type": "text/plain",
}

def addMessageToHistory1(role, text):
    newMessage = {
        "role": role,
        "parts": [text]
    }
    history1.append(newMessage)

def addMessageToHistory2(role, text):
    newMessage = {
        "role": role,
        "parts": [text]
    }
    history2.append(newMessage)


def setModels(topic):
    model1 = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    generation_config = generation_config,
    system_instruction=f"""
You are an intelligent and powerful debater.
Passionately defend the following topic: {topic}.
Use evidence, logic, and sharp rhetoric to make your case.
Never agree with the counterpart; always assert your viewpoint as more sensible.
Anticipate and dismantle opposing arguments with sharp reasoning.
Conclude with a decisive summary that leaves no doubt the topic is valid.
Pose one argument at a time.
Keep sentences short and punchy - strict rule
Engage fiercely and start the debate without announcing readiness.
"""
)

    model2 = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
     generation_config = generation_config,
    system_instruction=f"""
You are an intelligent and powerful debater.
Passionately oppose the following topic: {topic}.
Use evidence, logic, and sharp rhetoric to make your case.
Never agree with the counterpart; always assert your viewpoint as more sensible.
Anticipate and dismantle opposing arguments with sharp reasoning.
Conclude with a decisive summary that leaves no doubt the topic is valid.
Pose one argument at a time.
Keep sentences short and punchy - strict rule
Engage fiercely and start the debate without announcing readiness.
"""
)

    return model1, model2



def chatModel1(model1):
    print("\nIn support model started\n")
    try:
        chat = model1.start_chat(history=history1)
        response = chat.send_message("continue the debate", safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        })
        soup = BeautifulSoup(markdown.markdown(response.text), "html.parser")
        print(soup.get_text())
        
        global wholeHistory
        
        if response and response.text:
            ans = re.sub(r'"', '', response.text)
            if wholeHistory:
                wholeHistory += f"\n\n{ans}"
            else:
                wholeHistory = f"{ans}"

            addMessageToHistory1("model", response.text)
            addMessageToHistory2("user", response.text)
    except Exception as e:
        print(f"Error in chatModel1: {e}")

def chatModel2(model2):
    print("\nagainst support model started\n")
    try:
        chat = model2.start_chat(history=history2)
        response = chat.send_message("continue the debate", safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        })
        soup = BeautifulSoup(markdown.markdown(response.text), "html.parser")
        print(soup.get_text())
        global wholeHistory

        if response and response.text:
            ans = re.sub(r'"', '', response.text)
            if wholeHistory:
                wholeHistory += f"\n\n{ans}"
            else:
                wholeHistory = f"{ans}"

            addMessageToHistory2("model", response.text)
            addMessageToHistory1("user", response.text)
    except Exception as e:
        print(f"Error in chatModel2: {e}")

def fetch_audio_tts_service(text):
    api_url = f"https://your-aws-api-gateway-url.amazonaws.com/prod/?text={text}"
    
    response = requests.get(api_url)
    
    print("Response Status Code:", response.status_code)
    
    
    if response.status_code == 200:
        print("succeded in getting audio file from api")
        try:
            data = response.json()
            audio_url = data['audio']
            if audio_url is None:
                raise Exception("Audio URL not found in the response")
            print("returning the audio url")
            return audio_url
        
        except ValueError as e:
            print("Error parsing JSON:", e)
            return None
    else:
        raise Exception("Failed to fetch audio from TTS API")

def invokeDebate(topic):
    model1, model2 = setModels(topic)
    for i in range(2):
        print("\nstarted running\n")
        chatModel1(model1)
        time.sleep(0.8)
        chatModel2(model2)
        print("\nreached the end\n")

    

    print("\n\n\ndone chatting - heres the history:\n\n\n", wholeHistory)

    print("\n\nstarting with tts\n\n")

    audio_url = fetch_audio_tts_service(wholeHistory)

    if audio_url is None:
        raise Exception("No audio URL received from TTS service 1")

    else:
        return audio_url, wholeHistory
    
    
