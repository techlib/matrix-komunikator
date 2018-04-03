#!/usr/bin/python3

import zmq
import click
import json

#import os.path
#from sys import exit

@click.command()
@click.option('--message', '-m', default='dummy text',
              help='Send message to matrix.')
@click.option('--room', '-r', default='#zabbix:techlib.cz',
              help='Room to send message to.')
@click.version_option('0.1.1')
def speak(message, room):
    '''
    uncomment following lines and imports if you want to 
    detect existence of socket on client side
    '''
    #if not os.path.exists('/tmp/matrix-relay.sock'):
    #    print('Listener service is not running.\n\
    #Exiting...')
    #    exit(1)
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.setsockopt(zmq.LINGER, 2000)
    socket.connect('ipc:///tmp/matrix-relay.sock')
    outgoing = {'message':message, 'room': room}
    out_js = json.dumps(outgoing)
    socket.send_multipart([out_js.encode('utf8')])

if __name__ == '__main__':
    speak()
