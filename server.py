from json import loads, dumps
from quart import Quart, send_from_directory, websocket, Response
import asyncio
import os

if not os.path.exists("data"):

    # if the data directory is not present
    # then create it.
    os.makedirs("data")

global MessageCounter
global WsWebQueue
global ServerInputMessageQueue
global ServerOutputMessageQueue
ServerInputMessageQueue = asyncio.Queue()  # arduino -> web
ServerOutputMessageQueue = asyncio.Queue()  # web -> arduino
TIMEOUT = 0.1
FILEPATH = "data/"
FILENAME = "data.csv"
FILES = next(os.walk(FILEPATH), (None, None, []))[2]  # [] if no file

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
                saveData(obj["data"] + "," + str(obj["timestamp"]) + "\n")
        ServerInputMessageQueue.put_nowait(data)


async def sensorSend():
    while True:
        try:
            data = await ServerOutputMessageQueue.get()
            print("SENSOR SEND MESSAGE : " + str(data))
            await websocket.send(data)
        except KeyboardInterrupt:
            exit()
        except asyncio.QueueEmpty as e:
            pass


async def webReceive():
    global ServerOutputMessageQueue
    while True:
        data = await websocket.receive()
        print("WEB RECEIVE MESSAGE : " + str(data))
        if ServerOutputMessageQueue.qsize() > 10:
            ServerOutputMessageQueue = asyncio.Queue()
        ServerOutputMessageQueue.put_nowait(data)


async def webSend():
    while True:
        try:
            data = await ServerInputMessageQueue.get()
            print("WEB SEND MESSAGE : " + str(data))
            await websocket.send(data)
        except KeyboardInterrupt:
            exit()
        except asyncio.QueueEmpty as e:
            pass


@app.route("/")
async def hello():
    return await send_from_directory("public", "index.html")


@app.route("/<path:filename>")
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
    FILENAME = f"data.{filename}.csv"
    FILES.append(FILENAME)
    init_file()
    return Response("ok", status=200)


@app.route("/api/files/<filename>/remove")
async def remove_filename(filename):
    global FILENAME
    global FILEPATH
    global FILES
    FILES.remove(filename)
    os.remove(FILEPATH + filename)
    return Response("ok", status=200)


@app.route("/api/files/list")
async def files_list():
    global FILES
    FILES = next(os.walk(FILEPATH), (None, None, []))[2]  # [] if no file
    return Response(dumps(FILES), mimetype="application/json")


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
    r.headers["Cache-Control"] = "public, max-age=0"
    return r


@app.websocket("/sensor")
async def ws_sensor():
    producer = asyncio.create_task(sensorReceive())
    consumer = asyncio.create_task(sensorSend())
    await asyncio.gather(producer, consumer)


@app.websocket("/web")
async def ws_web():
    producer = asyncio.create_task(webReceive())
    consumer = asyncio.create_task(webSend())
    await asyncio.gather(producer, consumer)


if __name__ == "__main__":
    app.run(port=31310, host="192.168.5.8")
