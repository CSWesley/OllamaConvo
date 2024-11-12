import sys
import subprocess
import speech_recognition as sr
import pyttsx3


class TextToSpeech:
    engine: pyttsx3.Engine

    def __init__(self, voice, rate: int, volume: float):
        self.engine = pyttsx3.init()
        if voice:
            self.engine.setProperty('voice', voice)
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def list_voices(self):
        voices: list = [self.engine.getProperty('voices')]

        for i, voice in enumerate(voices[0]):
            print(f'{i+1} {voice.name} {voice.age}: {voice.languages[0]} ({voice.gender}) [{voice.id}]')

    def text_to_speech(self, text: str, save: bool = False, file_name='output.mp3'):
        self.engine.say(text)
        print('I am speaking...')
        if save:
            self.engine.save_to_file(text, file_name)
        self.engine.runAndWait()

r = sr.Recognizer()

def record_text():
    while(1):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                mytext = r.recognize_google(audio2)
                return mytext


        except sr.RequestError as e:
            print("Could not request results: {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occured")

    return


def run_ollama_command():
    print("Ready to start receiving input...")
    while(1):
        user_input = record_text()
        if user_input == "exit":
            sys.exit()
        elif user_input == "quit":
            sys.exit()
        print("Received input...")
        command = f"ollama run llama3.2 \"{user_input}\" > output.txt"
        subprocess.run(command, shell=True)

        with open('output.txt', 'r') as file:
            file_contents = file.read()

        tts = TextToSpeech(None, 200, 0.5)
        tts.text_to_speech(file_contents)
        print("Ready to receive more input")


if __name__ == "__main__":
    run_ollama_command()
