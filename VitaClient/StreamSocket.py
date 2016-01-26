#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

class StreamSocket(object):
    def __init__(self, s):
        self.sock = s
        self.closedFlag = False

    def sendMessage(self, message):
        try:
            self.sock.send(message)
        except Exception:
            print "send message failed!"

    def receiveMessage(self):
        return self.sock.recv(1024)


    def sendBytes(self, filepath):
        with open(filepath, 'rb') as f:
            self.sock.send(f.read())
            return
        print "send bytes failed!"

    def close(self):
        self.sock.close()
        self.closedFlag = True

    def isClosed(self):
        return self.closedFlag

    def getSocket(self):
        return self.sock

    def setSocket(self, s):
        self.sock = s
