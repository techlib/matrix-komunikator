#!/usr/bin/python3

import zmq
import click
import sys
import os

from configparser import ConfigParser

from matrix_client.client import MatrixClient
from matrix_client.api import MatrixRequestError
from requests.exceptions import MissingSchema

class Komunikator:
    def __init__(self, username, password, room_name, client):
        self. username = username
        self.password = password
        self.room_name = room_name
        self.client = client
        self.room = None

    def connect(self):
        try:
            self.client.login_with_password(username=self.username,
                                            password=self.password)

        except MatrixRequestError as e:
            print(e)
            if e.code == 403:
                print("Bad username or password.")
                sys.exit(4)
            else:
                print("Check that your sever details are correct.")
                sys.exit(2)

        except MissingSchema as e:
            print("Bad URL format.")
            print(e)
            sys.exit(3)

        try:
            self.room = self.client.join_room(self.room_name)

        except MatrixRequestError as e:
            print(e)
            if e.code == 400:
                print("Room ID/Alias in the wrong format")
                sys.exit(11)
            else:
                print("Couldn't find room.")
                sys.exit(12)

    def send_message(self, message):
        try:
            self.room.send_text(message)
        except MatrixRequestError as e:
            print('{0} Retrying...'.format(e))
            self.connect()
            self.send_message(message)
                


@click.command()
@click.option('--config', '-c', default='/etc/matrix-notifikator.ini',
              metavar='PATH', help='Load a configuration file.',
              type=click.File('r'))
@click.version_option('0.1.0')
def listen(config):
    ini = ConfigParser()
    ini.read_file(config)
    komunikator = Komunikator(
        ini.get('matrix', 'username'), ini.get('matrix', 'password'), 
        ini.get('matrix', 'room'), MatrixClient(ini.get('matrix', 'server')))
    komunikator.connect()
    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.setsockopt_unicode(zmq.IDENTITY, 'server')
    socket.bind('ipc:///tmp/matrix-relay.sock')

    while True:
        sender, message = socket.recv_multipart()
        komunikator.send_message(message.decode('utf8'))

if __name__ == '__main__':
    listen()
