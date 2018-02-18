#!/usr/bin/python

import socket
import argparse
import time
from struct import pack 

HOST, PORT = "localhost", 9999


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ipaddr',
        type=str,
        help='IP address of a requesting server', 
        default='localhost')
    parser.add_argument(
        '--port',
        type=int,
        help='Listening port in the requesting server',
        default=9999)
    parser.add_argument(
        '--imgdir',
        type=str,
        help='Image location/directory',
        default='Rocky.jpg')
    parser.add_argument(
        '--cont',
        type=str,
        help='Continuous asking for the same image sets',
        default='No')

    args = parser.parse_args()
    start = time.time()

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.ipaddr, args.port))
    f = open(args.imgdir, 'rb')
    #data = f.read()
    #f.close()

    # Thanks for the stackoverflow answer:
    # https://stackoverflow.com/questions/42459499/what-is-the-proper-way-of-sending-a-large-amount-of-data-over-sockets-in-python

    try:
        # Connect to server and send data
        if args.cont == 'No':
            data = f.read()
            f.close()
            # Use struct to make sure we have a consistent endiannes on the length
            length = pack('>Q', len(data))
            # sendall to make sure it blocks if there's back-pressure on the socket
            sock.sendall(length)
            sock.sendall(data)
            print "Sent:     {}".format(len(data))
            # Receive data from the server and shut down
            data = []
            received = sock.recv(1024)
            print("Received: {}".format(received))
            print("Total RTT: {} [s]".format(time.time() - start))
        else:
            while True:
                # Use struct to make sure we have a consistent endiannes on the length
                f = open(args.imgdir, 'rb')
                data = f.read()
                f.close()
                length = pack('>Q', len(data))
                # sendall to make sure it blocks if there's back-pressure on the socket
                sock.send(length)
                sock.send(data)
                print "Sent:     {}".format(len(data))
                data = []
                # Receive data from the server and shut down
                received = sock.recv(1024)
                print("Received: {}".format(received))
                print("Total RTT: {} [s]".format(time.time() - start))
                time.sleep(2)
    finally:
        #sock.close()
        pass

if __name__ == '__main__':
    main()
