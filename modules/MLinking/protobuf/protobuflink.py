import modules.MLinking.protobuf.audio2face_pb2 as a2f
import modules.MChatting.textChat as textChat
import modules.MLaughing.audio2face as facing
import modules.MSpeaking.voiceChat as voiceChat

def test():
    Request = a2f.Request()
    Request.content = "Hi!"
    Request.tts_type = "ms"
    print(Request.tts_type)
    print(Request.SerializeToString())

    pass

def parse_Request(request_Source):
    try:
        Request = a2f.Request()
        Request.ParseFromString(request_Source)
        #print("Request Parsed:\nContent = " + Request.content + "\nTTS_Type = " + Request.tts_type + "\n")
        return Request.content, Request.tts_type
    finally:
        pass

def encode_Response(requestContent, requestTTSType):
    Response = a2f.Response()

    ###SampleData:sample
    textResponse = textChat.textChat(requestContent)
    Response.content = textResponse
    Response.emotion = 1.0
    Response.wav_data = voiceChat.ttsLocal(textResponse)
    emoSample = facing.emoChat()
    for i in emoSample:
        Response.bs_value.append(i * 1.7)
    for i in facing.bs_keys:
        Response.bs_key.append(i)
        Response.bs_value.append(0)

    rDecoded = Response.SerializeToString()
    return rDecoded

    pass