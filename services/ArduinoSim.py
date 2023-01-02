import json
import time
import asyncio
import websockets
import random

COMMAND_START = "START"
COMMAND_END = "END"
COMMAND_START_EXPERIMENT = "StartExperiment"
COMMAND_STOP_EXPERIMENT = "StopExperiment"
COMMAND_STATUS = "STATUS"

# arduino -> server


class SensorCommand:
    def __init__(self, data, timestamp):
        self.data = data
        self.timestamp = timestamp


# server -> arduino
class ServerCommand:
    def __init__(self, command, error=False):
        self.command = command
        self.error = error


def parse_server_message(message):
    message = message.replace(COMMAND_START, "")
    message = message.replace(COMMAND_END, "")
    print(message)

    doc = json.loads(message)

    command = ServerCommand(doc["command"])
    command.error = False

    return command


def parse_sensor_message(message, timestamp):
    doc = {"data": message, "timestamp": timestamp}

    response = json.dumps(doc)
    return response


sonda1 = 350
sonda2 = 370
sonda3 = 390
sonda4 = 410
sonda5 = 430
sonda6 = 450

server_address = "192.168.5.8"
server_path = "/sensor"
port = 31310

server_message = ""
global start_experiment
start_experiment = False


def get_time():
    now = time.time()
    return now


def generate_sensor_data(status=False):
    global sonda1, sonda2, sonda3, sonda4, sonda5, sonda6
    sonda1 += random.randint(-12, 12)
    sonda2 += random.randint(-12, 12)
    sonda3 += random.randint(-12, 12)
    sonda4 += random.randint(-12, 12)
    sonda5 += random.randint(-12, 12)
    sonda6 += random.randint(-12, 12)

    sonda1 = min(max(sonda1, 1), 500)
    sonda2 = min(max(sonda2, 1), 500)
    sonda3 = min(max(sonda3, 1), 500)
    sonda4 = min(max(sonda4, 1), 500)
    sonda5 = min(max(sonda5, 1), 500)
    sonda6 = min(max(sonda6, 1), 500)
    message = f"{sonda1},{sonda2},{sonda3},{sonda4},{sonda5},{sonda6}"
    if status:
        message = COMMAND_STATUS
    return parse_sensor_message(message, get_time())


#! drugi timeout prebacuje vrijeme unaprijed, ne sprema u isto vrijeme
async def ws_loop():
    async with websockets.connect(
        f"ws://{server_address}:{port}{server_path}"
    ) as websocket:
        while True:
            print(start_experiment)
            if start_experiment:
                # Send a message every 2 seconds
                await asyncio.sleep(2)
                await send_ws_message(websocket, generate_sensor_data())

            # Set a timeout of 0.1 seconds on the receive call
            try:
                await asyncio.wait_for(receive_ws_message(websocket), timeout=0.1)
            except asyncio.TimeoutError:
                # No message was received within the timeout
                pass


async def send_ws_message(websocket, message):
    await websocket.send(message)


# read commands from websocket
async def receive_ws_message(websocket):
    global server_message
    global start_experiment
    message = await websocket.recv()
    server_message += message
    if server_message.startswith(COMMAND_START) and server_message.endswith(
        COMMAND_END
    ):
        command = parse_server_message(server_message)
        if not command.error:
            if command.command == COMMAND_START_EXPERIMENT:
                start_experiment = True
            if command.command == COMMAND_STOP_EXPERIMENT:
                start_experiment = False
            if command.command == COMMAND_STATUS:
                await send_ws_message(websocket, generate_sensor_data(True))
        server_message = ""
    if len(server_message) > len(COMMAND_START):
        server_message = ""  # in case of wrong or invalid command


async def main():
    await ws_loop()


if __name__ == "__main__":
    asyncio.run(main())
