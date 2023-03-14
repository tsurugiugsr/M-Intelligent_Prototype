import sys
import base64

def tts(textInput):
    with open("/Users/tsurugiugushiro/Documents/HomeWork/2022.9/M-Intelligent_Prototype/modules/MSpeaking/YoimiyaSample16.wav", "rb") as f:
        audioData = f.read()
    audio64 = base64.b64encode(audioData)
    audio64.decode('utf-8')
    return audio64
    
if __name__ == "__main__":
    tts("Hello World!")