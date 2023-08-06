#!/usr/bin/env Python
# coding=utf-8
#作者： tony
# -*- coding: utf-8 -*-
import os, sys,json,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os, sys,types,json
import Utils.classmake as cmake
import threading
import asyncio
import websockets
from websocket import create_connection
from Utils.Common import is_json, objtoLowerCase
from Utils.IRenderControlEventClass import *

class Event_Thead(threading.Thread):
    def __init__(self, e,_ws):
        super().__init__()
        self.e = e
        self.ws=_ws
        # self.eventloop = asyncio.new_event_loop()
        # self.eventloop.run_until_complete(self.evnet_initWs())

        # t = threading.Thread(target=start_loop, args=(newloop,))
        # t.start()
        # asyncio.run_coroutine_threadsafe(sendMessage(json.dumps(postData)), newloop)
        # asyncio.run_coroutine_threadsafe(recvMessage(fn, fnName, eventArgs, postData), newloop)

        # msg = json.dumps({"model": 1, "Token": "d7b501d2-fe5d-4a26-a799-1e67e037bfb5"})
        # self.ws.send(msg)

    def run(self):
        while True:
            if not self.e.is_set():
                # model =asyncio.run_coroutine_threadsafe(recvMessage(self.fn, self.fnName, self.eventArgs,self.postData),mainloop)
                model=self.ws.recv()
                backData = json.loads(model).get("api")
                if self.fnName == "on" + backData:
                    if hasattr(self, "eventArgs"):
                        cmake.AddRenderEventCB_ep(model, self.fn, self.fnName, self.eventArgs)
                    else:
                        cmake.AddRenderEventCB_ep(model, self.fn, self.fnName, None)
                self.e.wait()
                # self.e.clear()
            else:
                self.e.set()
                # print('runing')




    # async def initWs(self):
    #     self._event_ws = await websockets.connect(self.address)

    # async def initWs(self):
    #     self._event_ws = await websockets.connect(self.address)

class Event_Recv(threading.Thread):
    def __init__(self,ws,e):
        self.e = e
        self.ws=ws
        # 使用super函数调用父类的构造方法，并传入相应的参数值。
        super().__init__()

    def run(self):
        # _ws = create_connection("ws://127.0.0.1:8181/")
        while True:
            # feature = asyncio.run_coroutine_threadsafe(recvMessage(), eventloop)
            # rcEvent.recvData = feature.result()
            rcEvent.recvData = self.ws.recv()
            aa=rcEvent.recvData
            rcEvent.set()

class Event_TheadData(threading.Thread):
    def __init__(self,ws,e,func,args,name=''):
        self.e = e
        self.ws=ws
        self.func=func
        # 使用super函数调用父类的构造方法，并传入相应的参数值。
        super().__init__(target = func,name=name,args=args)

    def run(self):
        # _ws = create_connection("ws://127.0.0.1:8181/")
        while True:
            # self.e.wait()
            if hasattr(self.e, "recvData") and self.e.recvData is not None:  # not self.e.is_set():
                # self.e.wait()
                viewmodel = self.e.recvData  # self.ws.recv()
                backData = json.loads(viewmodel).get("api")
                if self.name == "on" + backData:
                    model = json.loads(viewmodel).get("Result")
                    args = []
                    if len(self._args) > 0:
                        for key, arg in self._args.items():
                            m = cmake.dict2obj(model.get(key[0].upper() + key[1:]), arg["t"])
                            args.append(m)
                    # self._target(*args)
                    self.func(*args)
                    self.e.recvData=None
                # self.e.wait()
                # self.e.clear()
            # else:
            #     self.e.wait()
                # self.e.set()






    # async def initWs(self):
    #     self._event_ws = await websockets.connect(self.address)


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def SocketApiServe_init(config):
    global eventprocess,mainloop,eventloop,_global_ws,ws_address,_event_ws,event_ws,rcEvent,recvData
    try:
        rcEvent = threading.Event()
        recvData={}
        # ws= websocket.WebSocket()
        mainloop = asyncio.new_event_loop()
        t = threading.Thread(target=start_loop, args=(mainloop,))
        t.start()
        featrue=asyncio.run_coroutine_threadsafe(main_initWs(config.serverAddress),mainloop)
        _global_ws = featrue.result()
        eventloop = asyncio.new_event_loop()
        t1 = threading.Thread(target=start_loop, args=(eventloop,))
        t1.start()
        featrue1=asyncio.run_coroutine_threadsafe(event_initWs(config.serverAddress),eventloop)
        _event_ws=featrue1.result()
        ws_address=config.serverAddress
        event_ws=create_connection("ws://127.0.0.1:8181/")

        rectP=Event_Recv(event_ws,rcEvent)
        rectP.start()
        # eventloop = asyncio.new_event_loop()
        # eventprocess = Event_Thead(rcEvent,event_ws)
        # _event_ws= create_connection("ws://127.0.0.1:8181/")
        # _global_ws.run_forever()
    except Exception:
        pass

def getrcEvent():
    return rcEvent

def recvData():
    print("recv start")
    rcEvent.recvData = _global_ws.recv()
    print("recv ok")
    print(rcEvent.recvData)
    rcEvent.set()

async def main_initWs(serverAddress):
    try:
        _ws= await websockets.connect(serverAddress)
    except KeyboardInterrupt:
        await _ws.close(reason="user exit")
    return _ws

async def event_initWs(serverAddress):
    try:
        _ws= await websockets.connect(serverAddress)
    except KeyboardInterrupt:
        await _ws.close(reason="user exit")
    return _ws

async def sendMessage(_ws,msg):
    await  _ws.send(msg)
    return await _ws.recv()

async def recvMessage():
    return await _event_ws.recv()


# async def recvMessage(fn,fnName,eventArgs,postData):
#     str=await _global_ws.recv()
#     if is_json(str):
#         apiData = json.loads(str)
#         resultmodel = objtoLowerCase(apiData.get("Result"))
#         backData = json.loads(resultmodel).get("api")
#         if postData["EventName"] == "on" + backData:
#             cmake.AddRenderEventCB_ep(resultmodel, fn, fnName, eventArgs)

def postMessage(Props, callName, obj, isMain=True):
        # obj["CallBack"] = "API-{}".format(uuid.uuid1())
        # if Props is not None and callName is not None:
        #     sdkInfo(Props, obj.get("CallBack"), callName, "push")
        # loop = asyncio.get_event_loop()
        # str=loop.run_until_complete(send_msg(obj))
        # str = eventprocess.SendMessage(json.dumps(obj))
        # if isMain:
        feature=asyncio.run_coroutine_threadsafe(sendMessage(_global_ws,json.dumps(obj)),mainloop)
        # else:
        #     feature=asyncio.run_coroutine_threadsafe(sendMessage(_event_ws,json.dumps(obj)),eventloop)
        str=feature.result()
        if is_json(str):
            apiData = json.loads(str)
            result = objtoLowerCase(apiData.get("Result"))
            # if apiData.get("CallBack") is not None:
            #     sdkInfo(None, apiData.get("CallBack"), "", "pull")
            #     apiCallback[apiData.get("CallBack")](result)
            #     del apiCallback[apiData.get("CallBack")]
            return result
        else:
            return str





