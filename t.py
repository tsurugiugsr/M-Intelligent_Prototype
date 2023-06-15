from TTS.api import TTS

model_name = TTS.list_models()[28]
# Init TTS
#tts2 = TTS(model_path = model_Alhaitham, config_path = config_Alhaitham)
tts = TTS(model_name)


tts.tts_with_vc_to_file(
    "我是教令院的书记官艾尔海森。",
    speaker_wav="/Users/tsurugiugushiro/Documents/HomeWork/2022.9/M-Intelligent_Prototype/Yoimiya3.mp3",
    file_path="outputAlhaitham.wav"
)
# tts2.tts_to_file("我是教令院的书记官艾尔海森。",file_path="outputAlhaitham.wav")