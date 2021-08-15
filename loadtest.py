import websocket
import time
import requests
import json
import os
from coolname import generate_slug
from random import uniform, choice

PY_ENV = os.environ.get('PY_ENV')
ROOM_COUNT = int(os.environ.get('ROOM_COUNT'))
ROOM_SIZE = int(os.environ.get('ROOM_SIZE'))
ROOM_TICKS = int(os.environ.get('ROOM_TICKS'))
PY_DOMAIN = '127.0.0.1:8000'
if PY_ENV == 'prod':
    PY_DOMAIN = 'ineedempathy.com'

class EmpathyRoom:
    @classmethod
    def build(cls, room_size):
        try:
            url = 'http://' + PY_DOMAIN + '/api/rooms'
            room_name = json.loads(requests.post(url).text)['name']
            print('OPEN | Room: ' + room_name)
            klass = cls(room_name, room_size)
            klass.fill_room()
            return klass
        except requests.exceptions.RequestException as e:
            print('ERROR: ')
            print(e)

    def __init__(self, room_name, room_size):
        self.room_name = room_name
        self.room_size = room_size
        self.users = []

    # complete a random action
    def tick(self):
        print('TICK | Room: ' + self.room_name)
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
            self.users.append(RoomUser.build(self.room_name))
            self.receive()

class RoomUser:
    @classmethod
    def build(cls, room_name):
        return cls(room_name, generate_slug(2))

    def __init__(self, room_name, user_name):
        self.room_name = room_name
        self.user_name = user_name
        print('OPEN | Room: ' + self.room_name + '; User: ' + self.user_name)
        self.url = 'ws://' + PY_DOMAIN + '/api/rooms/' + \
            self.room_name + '/users/' + \
            self.user_name + '.ws'
        self.ws = websocket.create_connection(self.url)

    def close(self):
        print('CLOSE | Room: ' + self.room_name + '; User: ' + self.user_name)
        return self.ws.close(1005)

    def receive(self):
        if self.ws.connected:
            result =  self.ws.recv()
            #print("Received '%s'" % result)

    def toggle(self, card_id):
        self.ws.send('{"toggleCard": ' + str(card_id) + '}')

def run(room_count, room_ticks, room_size):
    rooms = []

    for x in range(0, room_count):
        time.sleep(0.1)
        room = EmpathyRoom.build(room_size=room_size)
        rooms.append(room)

    for x in range(0, room_ticks):
        time.sleep(0.05)
        for room in rooms:
            room.tick()

    for room in rooms:
        room.close()

run(room_count=ROOM_COUNT, room_ticks=ROOM_TICKS, room_size=ROOM_SIZE)
