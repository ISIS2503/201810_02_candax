from tornado import websocket, web, ioloop
import json

ws_clients=[]
class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print('Hola')
        if self not in ws_clients:
            ws_clients.append(self)


    def on_close(self):
        print('chao')
        if self in ws_clients:
            ws_clients.remove(self)
