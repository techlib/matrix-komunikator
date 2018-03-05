#!/usr/bin/python3

import zmq
import click

#import os.path
#from sys import exit

@click.command()
@click.option('--message', '-m', default='dummy text',
              help='Send message to matrix.')
@click.version_option('0.1.0')
def speak(message):
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
    socket.send_multipart([message.encode('utf8')])

if __name__ == '__main__':
    speak()
