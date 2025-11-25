from mitmproxy import http, websocket
import os
import time
import base64

DUMP_DIR = "dumps"

def save_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)

class MITMLogger:
    def __init__(self):
        os.makedirs(DUMP_DIR, exist_ok=True)

    # HTTP REQUEST LOG
    def request(self, flow: http.HTTPFlow):
        ts = int(time.time() * 1000)
        fname = f"{DUMP_DIR}/requests/{ts}_{flow.request.method}.txt"
        text = f"{flow.request.method} {flow.request.url}\n\nHeaders:\n{flow.request.headers}"
        save_file(fname, text.encode())

    # HTTP RESPONSE — SAVE ALL FILES
    def response(self, flow: http.HTTPFlow):
        ts = int(time.time() * 1000)
        url = flow.request.url
        body = flow.response.content or b""

        safe = url.replace("://", "_").replace("/", "_").replace("?", "_")
        fname = f"{DUMP_DIR}/files/{ts}_{safe}"
        save_file(fname, body)

        meta = f"URL: {url}\nStatus: {flow.response.status_code}\nHeaders:\n{flow.response.headers}"
        save_file(f"{DUMP_DIR}/responses/{ts}_meta.txt", meta.encode())

    # WEBSOCKET CONNECT
    def websocket_handshake(self, flow: websocket.WebSocketFlow):
        ts = int(time.time() * 1000)
        text = f"WS CONNECT: {flow.server_conn.address}\nURL: {flow.request.url}\n\n{flow.request.headers}"
        save_file(f"{DUMP_DIR}/ws/{ts}_connect.txt", text.encode())

    # WEBSOCKET MESSAGES
    def websocket_message(self, flow: websocket.WebSocketFlow):
        ts = int(time.time() * 1000)
        for msg in flow.messages:
            direction = "IN" if msg.from_server else "OUT"

            if msg.is_text:
                content = msg.text.encode()
                fname = f"{DUMP_DIR}/ws/{ts}_{direction}_text.txt"
                save_file(fname, content)
            else:
                b64 = base64.b64encode(msg.content)
                fname = f"{DUMP_DIR}/ws/{ts}_{direction}_binary.b64"
                save_file(fname, b64)

addons = [
    MITMLogger()
]