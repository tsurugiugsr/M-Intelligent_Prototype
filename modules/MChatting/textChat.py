# -*- coding: utf-8 -*

import asyncio
import base64
import hashlib
import json
import time

import websockets


class IflyWebsocketAIUI:
    def __init__(self):
        self.auth_id = "2894c985bf8b1111c6728db79d3479ab"
        self.app_id = "045ea9c1"
        self.api_key = "68108ee1816da6a4ea66a1d0ea4ebb89"
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
        async with websockets.connect(
                uri,
                origin="http://wsapi.xfyun.cn",
                compression=None,
                subprotocols=["chat"],
        ) as websocket:
            await self.producer_handler(websocket, text)
            result = await self.consumer_handler(websocket)
        return result.get("nlp", {})


def scene_if(text):
    result = 0
    for i in ["发型", "衣服", "近景", "中景", "远景"]:
        if i in text:
            result = 1
            break
    return result


def run_xunfei_dm(text):
    # print(text)
    if '路特斯' in text:
        return '路特斯始终忠于品牌创始人柯林· 查普曼“一切为了驾驶者”的理念，成为一个专注于纯粹驾驶的汽车品牌。 创新的工程、尖端的技术和先进的材料，确保每一台路特斯都能证明通过轻量化实现性能的价值。'
    elif scene_if(text) == 1:
        return '好了'
    elif '会做' in text:
        return '我会的可多了，我能查询非常多的内容，比如天气和新闻等等、唱歌、换发型、换衣服、切换镜头等等，我还在学习更多的能力'
    elif '介绍' in text:
        return '我叫莱纳，来自卢米沃斯数字人项目组'
    else:
        # 对话平台的通用内容
        AIUI = IflyWebsocketAIUI()
        return asyncio.run(AIUI.nlp(text))['data']['intent']['answer']['text']

# main
if __name__ == "__main__":
    AIUI = IflyWebsocketAIUI()
    st = time.time()
    test_text = "上海天气"
    # test_text = "路特斯"
    dm_text = run_xunfei_dm(test_text)
    print(dm_text)
    print('dm time used: {}'.format(time.time() - st))

# wss://wsapi.xfyun.cn/v1/aiui?appid=045ea9c1&checksum=6bddc6a6a038b003ab2ca0accb30de55&param=eyJzY2VuZSI6ICJtYWluX2JveCIsICJhdXRoX2lkIjogIjI4OTRjOTg1YmY4YjExMTFjNjcyOGRiNzlkMzQ3OWFiIiwgImRhdGFfdHlwZSI6ICJ0ZXh0In0=&curtime=1657447134&signtype=md5
# wss://wsapi.xfyun.cn/v1/aiui?appid=045ea9c1&checksum=3bdf69641ace55649b8181ccc2eb018b&param=eyJzY2VuZSI6ICJtYWluX2JveCIsICJhdXRoX2lkIjogIjI4OTRjOTg1YmY4YjExMTFjNjcyOGRiNzlkMzQ3OWFiIiwgImRhdGFfdHlwZSI6ICJ0ZXh0In0=&curtime=1657447148&signtype=md5

def textChat(textInput):
    ###SampleData

    if textInput == "sample":
        return "Hello World!"
    else:
        return run_xunfei_dm(textInput)


    pass