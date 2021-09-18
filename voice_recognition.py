from azure.cognitiveservices.speech import ResultReason, SpeechConfig, SpeechRecognizer
from azure.cognitiveservices.speech.audio import AudioConfig
import requests
from settings import BOT_URL, SUBSCRIPTION, REGION

speech_config = SpeechConfig(SUBSCRIPTION, REGION)
speech_recogniser = SpeechRecognizer(speech_config)

def make_stt_call():
    result = speech_recogniser.recognize_once_async().get()

    if result.reason == ResultReason.RecognizedSpeech:
        body = {
            'content': result.text
        }
        response = requests.post(BOT_URL, body)
        print(response.text)
    else:
        print(f'Failed: {result.reason}')


make_stt_call()
