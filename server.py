from json import loads, dumps
from quart import Quart, send_from_directory, websocket, Response
import asyncio
import os


global MessageCounter
global WsWebQueue
global ServerInputMessageQueue
global ServerOutputMessageQueue
ServerInputMessageQueue     = asyncio.Queue()   #  arduino -> web
ServerOutputMessageQueue    = asyncio.Queue()   #  web -> arduino
TIMEOUT = 0.1
FILEPATH = "data/"
FILENAME = "data.csv"
FILES = next(os.walk(FILEPATH), (None, None, []))[2]  # [] if no file
# FILES = [ FILENAME ]

app = Quart(__name__, static_folder="public")

def saveData(stringData):
    global FILENAME
    global FILEPATH
    with open(FILEPATH + FILENAME, "a") as file:
        file.write(stringData)

def init_file():
    global FILENAME
    global FILEPATH
    with open(FILEPATH + FILENAME, "a") as file:
        file.write("s1,s2,s3,s4,s5,s6,timestamp\n")

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

@app.route('/<path:filename>')
async def send_file(filename):  
    return await send_from_directory("public", filename)

@app.route("/api")
async def json():
    return {"hello": "world"}

@app.route("/api/files/start/<filename>")
async def change_filename(filename):
    global FILENAME
    global FILEPATH
    global FILES
    FILENAME = f'data.{filename}.csv'
    FILES.append(FILENAME)
    init_file()
    return Response("ok",status=200)

@app.route("/api/files/<filename>/remove")
async def remove_filename(filename):
    global FILENAME
    global FILEPATH
    global FILES
    # tmpFilename = f'data.{filename}.csv'
    FILES.remove(filename) 
    os.remove(FILEPATH + filename)
    return Response("ok",status=200)


@app.route("/api/files/list")
async def files_list():
    global FILES
    FILES = next(os.walk(FILEPATH), (None, None, []))[2]  # [] if no file
    return Response(dumps(FILES),  mimetype='application/json')

@app.route("/api/files/<filename>")
async def files_get(filename):
    global FILENAME
    global FILEPATH
    return await send_from_directory(FILEPATH, FILENAME)


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



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
#     async with websockets.serve(echo, "192.168.4.8", 31310):
#         await asyncio.Future()  # run forever



# if __name__ == '__main__':
#     app.run(debug=False,host="192.168.4.8", port=5000, use_reloader=False)
