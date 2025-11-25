from mitmproxy import http, websocket
import os
import time
import base64

DUMP_DIR = "dumps"

def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)

class MITMLogger:
    def request(self, flow: http.HTTPFlow):
        ts = time.time_ns()
        fname = f"{DUMP_DIR}/requests/{ts}_{flow.request.method}.txt"
        text = f"{flow.request.method} {flow.request.url}\n\n{flow.request.headers}"
        save(fname, text.encode())

    def response(self, flow: http.HTTPFlow):
        ts = time.time_ns()

        safe = (
            flow.request.url.replace("://", "_")
            .replace("/", "_")
            .replace("?", "_")
            .replace("&", "_")
        )

        body_path = f"{DUMP_DIR}/files/{ts}_{safe}"
        meta_path = f"{DUMP_DIR}/responses/{ts}_meta.txt"

        save(body_path, flow.response.content)

        info = f"URL: {flow.request.url}\nStatus: {flow.response.status_code}\n\nHeaders:\n{flow.response.headers}"
        save(meta_path, info.encode())

    def websocket_start(self, flow: websocket.WebSocketFlow):
        ts = time.time_ns()
        text = f"WS CONNECT:\n{flow.request.url}\n\n{flow.request.headers}"
        save(f"{DUMP_DIR}/ws/{ts}_connect.txt", text.encode())

    def websocket_message(self, flow: websocket.WebSocketFlow):
        ts = time.time_ns()
        msg = flow.messages[-1]

        direction = "IN" if msg.from_server else "OUT"

        if msg.is_text:
            save(f"{DUMP_DIR}/ws/{ts}_{direction}.txt", msg.text.encode())
        else:
            b64 = base64.b64encode(msg.content)
            save(f"{DUMP_DIR}/ws/{ts}_{direction}.b64", b64)

addons = [MITMLogger()]