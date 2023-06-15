import asyncio
import base64
import hashlib
import json
import time

import websockets

qDic = []
aDic = []
with open("/Users/tsurugiugushiro/Documents/HomeWork/2022.9/M-Intelligent_Prototype/modules/MLearning/Extension.txt", "rb") as f:
    extData = f.read()
extDic = extData.decode().split(";\n")
for i in extDic:
    exttemp = i.split(":\n")
    qDic.append(exttemp[0])
    aDic.append(exttemp[1])

class IflyWebsocketAIUI:
    def __init__(self):
        #self.auth_id = "2894c985bf8b1111c6728db79d3479ab"
        self.auth_id = "31e5430c7f34912991f22bd3291f9711"
        #self.app_id = "045ea9c1"
        self.app_id = "f3f01ded"
        #self.api_key = "68108ee1816da6a4ea66a1d0ea4ebb89"
        self.api_key = "4c68521992c384993751ad14142dd35d"
        self.END_TAG = "--end--"

    def build_aiui_url(self):
        base_url = "wss://wsapi.xfyun.cn/v1/aiui"
        curtime = int(time.time())
        signtype = "md5"
        param = {
            "scene": "main_box",
            "auth_id": self.auth_id,
            "data_type": "text",
        }
        param = json.dumps(param).encode("UTF8")
        param_base64 = base64.b64encode(param).decode()
        checksum_pre = self.api_key + str(curtime) + param_base64
        checksum = hashlib.md5(checksum_pre.encode("UTF8")).hexdigest()
        params = ("?appid=" + self.app_id + "&checksum=" + checksum
                  + "&param=" + param_base64 + "&curtime=" + str(curtime) + "&signtype=" + signtype)
        return base_url + params

    async def producer_handler(self, websocket, text):
        await websocket.send(bytes(text, encoding="utf-8"))
        # 发送结束的标志
        await websocket.send(bytes(self.END_TAG.encode("utf-8")))

    async def consumer_handler(self, websocket):
        result = {}
        async for message in websocket:
            message = json.loads(message)
            action = message["action"]
            if action == "result":
                data = message["data"]
                sub = data["sub"]
                if sub == "nlp":
                    result["nlp"] = message

        return result

    async def nlp(self, text):
        uri = self.build_aiui_url()
        # print(uri)
        async with websockets.connect( # type: ignore
                uri,
                origin="http://wsapi.xfyun.cn",
                compression=None,
                subprotocols=["chat"],
        ) as websocket:
            await self.producer_handler(websocket, text)
            result = await self.consumer_handler(websocket)
        return result.get("nlp", {})


def run_xunfei_dm(text):
    for i in range(0,  len(qDic)):
        if qDic[i] in text:
            return aDic[i]
    
    AIUI = IflyWebsocketAIUI()
    #print(asyncio.run(AIUI.nlp(text))['data'])
    return asyncio.run(AIUI.nlp(text))['data']['intent']['answer']['text']

# main
if __name__ == "__main__":
    AIUI = IflyWebsocketAIUI()
    st = time.time()
    test_text = "上海天气"
    dm_text = run_xunfei_dm(test_text)
    print(dm_text)
    print('dm time used: {}'.format(time.time() - st))

def textChat(textInput):
    print(textInput)
    try:
        if textInput == "sample":
            return "Hello World!"
        else:
            return run_xunfei_dm(textInput)
    except:
        return("抱歉，我目前无法回答")
