#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import threading
import socket
import time
import random

from VitaProtocol import VitaProtocol
from DataLocalHandler import DataLocalHandler
from StreamSocket import StreamSocket

class VitaClientHandler(object):
    def __init__(self, host="0.0.0.0", port=5233, myUid="000000"):
        # 用户 uid
        self.MyUid = myUid
        # 客户端ip地址设置
        self.Host = host
        # 客户端端口号设置
        self.Port = int(port)
        # 所有用户列表，格式为 {uid:User(uid, uname, pic, profile), }
        self.AllUsersList = {}
        # 所有在线用户，格式为 {uid:[host,port], }
        self.OnLineUsers = {}
        # 所有聊天记录，格式为 {uid:[[uid, time, chatMsg], ], }
        self.ChatLogsDic = {}
        # 所有正在聊天用户，格式为 {uid:streamsocket}
        self.ChattingUsers = {}
        # 启动标志，只有函数 stop 可以改变，方便控制监听子线程。
        self.StartFlag = False
        # 监听 socket
        self.listenSocket = None

        # VitaProtocol 类实例
        self.vitaprotocol = VitaProtocol()

        # DataLocalHandler 类实例
        self.datalocalhandler = DataLocalHandler()

    def start(self):
        if not self.StartFlag:
            self.AllUsersList = self.datalocalhandler.readAllUsers()
            self.OnLineUsers = {}
            self.ChatLogsDic = self.datalocalhandler.readAllChatLogs()
            self.ChattingUsers = {}
            self.StartFlag = True
            threading.Thread(target=self.startListener, args=()).start()


    def startListener(self):
        self.listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listenSocket.bind((self.Host, self.Port))
        self.listenSocket.listen(7)
        print("Listen Socket is set up in port %s.\nWaiting for connection..." %self.Port)
        while (self.StartFlag):
            # 接受一个新连接
            sock, addr = self.listenSocket.accept()
            tempUid = str(random.randint(10000000,99999999))
            self.ChattingUsers[tempUid] = StreamSocket(sock)
            threading.Thread(target=self.oneRecvHandler, args=(tempUid,)).start()
            print("A new connection in %s:%s." %addr)

    def stop(self):
        if (self.StartFlag):
            self.StartFlag = False
            for one in self.ChattingUsers:
                self.ChattingUsers[one].close()
            self.datalocalhandler.writeAllUsers(self.AllUsersList)
            self.datalocalhandler.writeAllChatLogs(self.ChatLogsDic)
            time.sleep(2)
            self.AllUsersList.clear()
            self.ChattingUsers.clear()
            self.ChatLogsDic.clear()
            self.OnLineUsers.clear()
            
            self.listenSocket.close()

    def oneRecvHandler(self, hisUid):
        temp = ""
        uid = hisUid
        while (not self.ChattingUsers[uid].isClosed()):
            temp = temp + self.ChattingUsers[uid].receiveMessage()
            while (True):
                temp,method,content = self.vitaprotocol.handleRawData(temp)
                if method == "Indentity":
                    if (self.MyUid == content[1] and content[0] in self.AllUsersList):
                        self.ChattingUsers[content[0]] = self.ChattingUsers[uid]
                        self.ChattingUsers.pop(uid)
                        uid = content[0]
                elif method == "ChatMsg":
                    self.addOneChatLog(uid, [uid, time.strftime("%Y-%m-%d %H:%M:%S"), content[0]])
                elif method == "Close":
                    self.ChattingUsers.pop(uid).close()
                elif method == "":
                    break


    def oneSendMsgHandler(self, uid, Msg):
        if (uid not in self.ChattingUsers and uid in self.OnLineUsers):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.OnLineUsers[uid][0],int(self.OnLineUsers[uid][1])))
            self.ChattingUsers[uid] = StreamSocket(s)
            self.ChattingUsers[uid].sendMessage(self.vitaprotocol.handleIdentity(self.MyUid, uid))
            threading.Thread(target=self.oneRecvHandler, args=(uid,)).start()
        if uid in self.ChattingUsers:
            self.ChattingUsers[uid].sendMessage(self.vitaprotocol.handleChatMsg(Msg))
            self.addOneChatLog(uid, [self.MyUid, time.strftime("%Y-%m-%d %H:%M:%S"), Msg])


    def addOneChatLog(self, uid, oneChatLog):
        if (uid not in self.ChatLogsDic):
            self.ChatLogsDic[uid] = []
        self.ChatLogsDic[uid].append(oneChatLog)

    def printOneChatLog(self, uid):
        if uid in self.ChatLogsDic:
            for one in self.ChatLogsDic[uid]:
                print("%s %s\n%s" %(one[0], one[1], one[2]))





#test

# myUid = raw_input("输入你的id:")
# myHost = raw_input("输入你的Host:")
# myPort = raw_input("输入你的Port:")
#
# hisUid = raw_input("输入他的id:")
# hisHost = raw_input("输入他的Host:")
# hisPort = raw_input("输入他的Port:")
#
# v = VitaClientHandler(myHost, myPort, myUid)
# v.start()
# v.OnLineUsers[hisUid] = [hisHost, int(hisPort)]
#
# while (True):
#     print "我的Uid："+str(v.MyUid)+" 我的Host："+v.Host+" 我的Port："+str(v.Port)
#
#     print "-------所有用户列表如下-------"
#     print "Uid--Uname--Pic--Profile"
#     for one in v.AllUsersList:
#         print v.AllUsersList[one].getUid() + "--" + v.AllUsersList[one].getUname() + "--" + v.AllUsersList[one].getPic() + "--" + v.AllUsersList[one].getProfile()
#     print "----------------------------"
#
#     print "---------所有在线用户---------"
#     print "Uid--Host--Port"
#     for one in v.OnLineUsers:
#         print one+"--"+v.OnLineUsers[one][0]+"--"+str(v.OnLineUsers[one][1])
#     print "----------------------------"
#
#     print "---------正在聊天用户---------"
#     print "Uids"
#     for one in v.ChattingUsers:
#         print one
#     print "----------------------------"
#
#     print "输入 chat  ---  和某人聊天"
#     print "输入 start ---  启动客户端"
#     print "输入 stop  ---  停止客户端"
#     print "输入 quit  ---  退出程序"
#
#     q = raw_input("请输入命令:")
#
#     if (q == "chat"):
#         print "---------所有在线用户---------"
#         print "Uid--Host--Port"
#         for one in v.OnLineUsers:
#             print one+"--"+v.OnLineUsers[one][0]+"--"+str(v.OnLineUsers[one][1])
#         print "----------------------------"
#         who = raw_input("请输入在线用户的uid:")
#         if who in v.OnLineUsers:
#             while True:
#                 print "---------正在和"+v.AllUsersList[who].getUname()+"聊天---------"
#                 v.printOneChatLog(who)
#                 print "---------正在和"+v.AllUsersList[who].getUname()+"聊天---------"
#                 msg = raw_input("输入消息:(输入q结束聊天！)")
#                 if (msg == "q"):
#                     break
#                 v.oneSendMsgHandler(who, msg)
#         else:
#             print "输入有误！"
#     elif (q == "stop"):
#         v.stop()
#     elif (q == "start"):
#         v.start()
#     elif (q == "quit"):
#         v.stop()
#         break
#     else:
#         print "输入有误，请重新输入:"
# print "程序退出！"
