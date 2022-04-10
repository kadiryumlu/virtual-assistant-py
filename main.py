import sys
import os
import time
import json
from numpy import random
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import special_commands


def load_json(file):
    with open(file, encoding='utf-8') as f:
        return json.loads(f.read())

def findResponse(commands, command):
    for key in commands.keys():
        if key.lower() in command.lower():
            return commands.get(key)
    return '-'

def listen(lang):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)
        command = ''

        try:
            command = r.recognize_google(audio, language=lang)
        except sr.UnknownValueError:
            print('I don\'t understand')
        except sr.RequestError:
            print('Request error!')

        print(command)
        return command

def speak(text, lang):
    tts = gTTS(text, lang=lang.split('-')[0])
    file = f'tts-{time.time()}.mp3'
    tts.save(file)
    playsound(file)
    os.remove(file)

def response(commands, command, lang):
    found = findResponse(commands, command)

    if(found != "-"):
        if(type(found) == list):
            choise = random.choice(found)
            print(choise)
            speak(choise, lang)
        elif(type(found) == dict):
            unformatted = found.get('txt')
            function_name = found.get('fun').get('name')
            function_param = found.get('fun').get('param')
            fun = getattr(special_commands, function_name)
            r = fun(function_param) if function_param  else fun()
            text = unformatted.format(r)
            print(text)
            speak(text, lang)
    else:
        getattr(special_commands, 'searchInGoogle')(command)
        print(commands.get(found))
        speak(commands.get(found), lang)

def main(argv):
    lang = 'en-EN'

    if(len(argv) > 1):
        lang = str(argv[1])

    command_file = f'./commands/{lang}.json'
    commands = load_json(command_file)
    #print(commands)

    while True:
        print("...")
        command = listen(lang)
        response(commands, command, lang)


if __name__ == "__main__":
   main(sys.argv)