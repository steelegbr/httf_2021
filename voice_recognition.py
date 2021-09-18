from time import sleep
from azure.cognitiveservices.speech import ResultReason, SpeechConfig, SpeechRecognizer, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import requests
from playsound import playsound
from settings import BOT_URL, HANDOVER, INTRO, OUTRO, RING_SFX, SUBSCRIPTION, REGION
from typing import Tuple

speech_config = SpeechConfig(SUBSCRIPTION, REGION)
audio_config = AudioOutputConfig(use_default_speaker=True)
speech_recogniser = SpeechRecognizer(speech_config)
synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

def convert_speech_to_text() -> str:
    result = speech_recogniser.recognize_once_async().get()

    if result.reason == ResultReason.RecognizedSpeech:
        print(f'Speech to text: "{result.text}"')
        return result.text

    print(f'Failed: {result.reason}')


def convert_text_to_speech(text: str):
    print(f'Text to speech: "{text}"')
    synthesizer.speak_text_async(text).get()


def make_api_call(text: str, conversation_id: str) -> Tuple[str, bool, str]:
    body = {
        'message': text
    }

    if conversation_id:
        body['conversation_id'] = conversation_id,

    response = requests.post(BOT_URL, body)
    print(f'From chatbot: {response.text}')

    if response.status_code == 200:
        json_response = response.json()
        return json_response['message'], json_response.get('conversation_end'), json_response['conversation_id']
    return 'I am sorry. Something went wrong!', True, None


if __name__ == "__main__":
    conversation_id = None
    completed = False
    response = None

    if INTRO:
        convert_text_to_speech(INTRO)

    while not completed:
        print('Starting recording...')
        text = convert_speech_to_text()
        print('Stopped recording.')
        response, completed, conversation_id = make_api_call(text, conversation_id)
        convert_text_to_speech(response)

    if 'emergency' in response or 'transfer' in response:
        playsound(RING_SFX)
        sleep(1)
        synthesizer.speak_ssml_async(HANDOVER)
    elif OUTRO:
        convert_text_to_speech(OUTRO)
