from json import loads
from quart import Quart, send_from_directory, websocket
import asyncio


global MessageCounter
global WsWebQueue
global ServerInputMessageQueue
global ServerOutputMessageQueue
ServerInputMessageQueue     = asyncio.Queue()   #  arduino -> web
ServerOutputMessageQueue    = asyncio.Queue()   #  web -> arduino
TIMEOUT = 0.1


app = Quart(__name__)

def saveData(stringData):
    with open("data.csv", "a") as file:
        file.write(stringData)


async def sensorReceive():
    while True:
        data = await websocket.receive()
        print("SENSOR RECEIVE MESSAGE : " + str(data))
        obj = loads(data)
        if "data" in obj:
            if obj["data"] != "STATUS":
                saveData(obj["data"] + "," + str(obj["timestamp"]) + '\n')
        ServerInputMessageQueue.put_nowait(data)

async def sensorSend():
    while True:
        try:
            data = await ServerOutputMessageQueue.get()
            print("SENSOR SEND MESSAGE : " + str(data))
            await websocket.send(data)
        except asyncio.QueueEmpty as e:
            pass

async def webReceive():
    global ServerOutputMessageQueue
    while True:
        data = await websocket.receive()
        print("WEB RECEIVE MESSAGE : " + str(data))
        if(ServerOutputMessageQueue.qsize() > 10) :
            ServerOutputMessageQueue = asyncio.Queue();
        ServerOutputMessageQueue.put_nowait(data)

async def webSend():
    while True:
        try:
            data = await ServerInputMessageQueue.get()
            print("WEB SEND MESSAGE : " + str(data))
            await websocket.send(data)
        except asyncio.QueueEmpty as e:
            pass


@app.route("/")
async def hello():
    return await send_from_directory("public","index.html")

@app.websocket("/sensor")
async def ws_sensor():
    producer = asyncio.create_task(sensorReceive())
    consumer = asyncio.create_task(sensorSend())
    await asyncio.gather(producer, consumer)
    # global ServerOutputMessageQueue
    # while True:
    #     # data = await websocket.receive()
    #     try:
    #         print("WAITING")
    #         data = await asyncio.wait_for(websocket.receive(), timeout=TIMEOUT)
    #         print(data)
    #         ServerInputMessageQueue.put_nowait(data)
    #     except asyncio.exceptions.TimeoutError:
    #         pass
        

        # try:
        
            

        # for ws in WsWebQueue:
        #     print("Sending to WS web")
        #     await ws.send(data)
        # await websocket.send(data)

@app.websocket("/web")
async def ws_web():
    producer = asyncio.create_task(webReceive())
    consumer = asyncio.create_task(webSend())
    await asyncio.gather(producer, consumer)
    # global WsWebQueue
    # print("WS web connected")
    # WsWebQueue.append(websocket)
    # while True:
    #     try:
    #         tmp = await ServerInputMessageQueue.get()
    #         print("GOT MESSAGE : " + str(tmp))
    #         await websocket.send(tmp)
    #     except asyncio.QueueEmpty as e:
    #         pass

        # await asyncio.Future()
        # data = await websocket.receive()
        # print(data)
        


if __name__ == "__main__":
    app.run(port=31310, host='192.168.4.8')


# import json
# from flask import Flask, send_from_directory
# import websockets


# loop = asyncio.get_event_loop()
# app = Flask(__name__, static_folder="./www")

# @app.route('/')
# def hello_world():
#     return send_from_directory('www', 'index.html')






# async def echo(websocket):
#     global MessageCounter
#     async for message in websocket:
#         print("GOT MESSAGE : " + str(message))
#         if MessageCounter == 0:
#             await websocket.send("START{\"command\":\"StartExperiment\",\"arguments\":[]\"}END")
#         elif MessageCounter == 10 :
#             await websocket.send("START{\"command\":\"StopExperiment\",\"arguments\":[]\"}END")
#         MessageCounter = MessageCounter + 1


# async def main():
#     async with websockets.serve(echo, "0.0.0.0", 31310):
#         await asyncio.Future()  # run forever



# if __name__ == '__main__':
#     app.run(debug=False,host="0.0.0.0", port=5000, use_reloader=False)
