#!/usr/bin/python
# coding: utf-8
import time
import json

def handle_websocket(ws):
    while True:
        message = ws.receive()
        if message is None:
            break
        else:
            message = json.loads(message)
            try:
                if message["type"] == "ping":
                    t = time.time() * 1000 - message["time"]
                    print message["time"]
                    ws.send(json.dumps({"type": "pong", "timedelta": t}))
                else:
                    raise KeyError()
            except KeyError:
                    r = "Unknown type in this message: %s"
                    r %= message
                    ws.send(json.dumps({'output': r}))
