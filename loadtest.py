import websocket
import time
import requests
import json
import os
from coolname import generate_slug
from random import uniform, choice

PY_ENV = os.environ.get("PY_ENV")
ROOM_COUNT = int(os.environ.get("ROOM_COUNT"))
ROOM_SIZE = int(os.environ.get("ROOM_SIZE"))
ROOM_TICKS = int(os.environ.get("ROOM_TICKS"))
PY_DOMAIN = "127.0.0.1:8000"
if PY_ENV == "prod":
    PY_DOMAIN = "ineedempathy.com"


class EmpathyRoom:
    @classmethod
    def build(cls, room_size, room_id):
        klass = cls(room_id, generate_slug(3), room_size)
        klass.fill_room()
        return klass

    def __init__(self, room_id, room_name, room_size):
        self.room_id = room_id
        self.room_name = room_name
        self.room_size = room_size
        self.users = []

    # complete a random action
    def tick(self):
        print("TICK | Room: " + self.room_name)
        choice(self.users).toggle(int(uniform(0, 80)))
        self.receive()

    def receive(self):
        for user in self.users:
            user.receive()

    def close(self):
        for user in self.users:
            user.close()
            self.receive()

    def fill_room(self):
        for x in range(0, self.room_size):
            user = RoomUser.build(self.room_name)
            if user.connect():
                self.users.append(user)
                self.receive()
            else:
                print(f"DROP | User: {user}")
        print(f"CREATED | Room: {self.room_id} - {self.room_name} Users: {len(self.users)}")


class RoomUser:
    @classmethod
    def build(cls, room_name):
        return cls(room_name, generate_slug(2))

    def __init__(self, room_name, user_name):
        self.room_name = room_name
        self.user_name = user_name
        # print('OPEN | Room: ' + self.room_name + '; User: ' + self.user_name)
        self.url = "ws://" + PY_DOMAIN + "/api/rooms/" + self.room_name + ".ws"

    def connect(self):
        try:
            #print(self.url)
            self.ws = websocket.create_connection(self.url)
            self.identify()
        except Exception as err:
            print(err)
            return False
        return True

    def close(self):
        print("CLOSE | Room: " + self.room_name + "; User: " + self.user_name)
        return self.ws.close(1005)

    def receive(self):
        if self.ws.connected:
            self.ws.recv()
            #print("Received '%s'" % result)

    def identify(self):
        self.ws.send('{"setName": "' + self.user_name + '"}')

    def toggle(self, card_id):
        self.ws.send('{"toggleCard": ' + str(card_id) + "}")


def run(room_count, room_ticks, room_size):
    rooms = []

    for x in range(0, room_count):
        time.sleep(0.1)
        room = EmpathyRoom.build(room_size=room_size, room_id=x)
        rooms.append(room)

    time.sleep(3)
    for x in range(0, room_ticks):
        time.sleep(0.05)
        for room in rooms:
            room.tick()

    for room in rooms:
        room.close()


run(room_count=ROOM_COUNT, room_ticks=ROOM_TICKS, room_size=ROOM_SIZE)
