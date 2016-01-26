#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import os
import re

from User import User

class DataLocalHandler(object):
    def __init__(self):
        self.BaseDirPath = os.path.dirname(__file__)
        self.UsersInfoFilePath = os.path.join(self.BaseDirPath, "resources/usersInfo.txt")
        self.ChatLogsPath = os.path.join(self.BaseDirPath, "resources/chatLogs")
        self.itemSplitFlag = "<itemSplitFlag>"
        self.groupSplitFlag = "<groupSplitFlag>"

    def readAllUsers(self):
        allUsers = {}
        with open(self.UsersInfoFilePath, 'r') as f:
            rawIn = f.read()
        for one in rawIn.split(self.groupSplitFlag):
            one = one.split(self.itemSplitFlag)
            if len(one) >= 4:
                allUsers[one[0]]=User(one[0], one[1], one[2], one[3])
        return allUsers

    def writeAllUsers(self, allUsers):
        rawOut = ""
        if allUsers:
            for one in allUsers:
                rawOut = rawOut + self.groupSplitFlag + allUsers[one].getUid() + self.itemSplitFlag + allUsers[one].getUname() + self.itemSplitFlag + allUsers[one].getPic() + self.itemSplitFlag + allUsers[one].getProfile() + self.groupSplitFlag
            with open(self.UsersInfoFilePath, 'w') as f:
                f.write(rawOut)

    def addOneUser(self, oneUser):
        if oneUser:
            rawOne = self.groupSplitFlag + oneUser.getUid() + self.itemSplitFlag + oneUser.getUname() + self.itemSplitFlag + oneUser.getPic() + self.itemSplitFlag + oneUser.getProfile() + self.groupSplitFlag
            with open(self.UsersInfoFilePath, 'a') as f:
                f.write(rawOne)

    def readAllChatLogs(self):
        files = os.listdir(self.ChatLogsPath)
        chatLogsDic = {}
        for one in files:
            match = re.match(r'((\d)\.txt)', one)
            if match:
                chatLogName, LogId = match.groups()
                chatLogsDic[LogId] = self.readOneChatLogs(chatLogName)
        return chatLogsDic

    def readOneChatLogs(self, chatLogName):
        path = os.path.join(self.ChatLogsPath, chatLogName)
        logs = []
        with open(path, 'r') as f:
            rawLogs = f.read()
        for one in rawLogs.split(self.groupSplitFlag):
            one = one.split(self.itemSplitFlag)
            if len(one) >= 3:
                logs.append(one)
        return logs

    def writeAllChatLogs(self, allChatLogs):
        for key in allChatLogs:
            self.writeOneChatLog(key, allChatLogs[key])

    def writeOneChatLog(self, chatLogId, oneChatLog):
        filePath = os.path.join(self.ChatLogsPath, chatLogId+".txt")
        rawLogs = ""
        for one in oneChatLog:
            one = self.groupSplitFlag + self.itemSplitFlag.join(one) + self.groupSplitFlag
            rawLogs = rawLogs + one
        with open(filePath, 'w') as f:
            f.write(rawLogs)


# Test
# d = DataLocalHandler()
# allUser = d.readAllUsers()
# aU = allUser
# for one in allUser:
#     t = allUser[one]
#     print t.getUid(),t.getUname(), t.getPic(), t.getProfile()
# d.addOneUser(User("3","3name","3.jpg","3profile"))
# print "添加一个用户后："
# allUser = d.readAllUsers()
# for one in allUser:
#     t = allUser[one]
#     print t.getUid(),t.getUname(), t.getPic(), t.getProfile()
# print "写入所有用户："
# d.writeAllUsers(aU)
# allUser = d.readAllUsers()
# for one in allUser:
#     t = allUser[one]
#     print t.getUid(),t.getUname(), t.getPic(), t.getProfile()
#
# chatlogs = c = d.readAllChatLogs()
# for one in chatlogs:
#     print one, chatlogs[one]
# print d.readOneChatLogs("2.txt")[0]
#
# d.writeOneChatLog('1', [['2', "time", "something"]])
# for one in d.readAllChatLogs():
#     print one, chatlogs[one]
# print d.readOneChatLogs("2.txt")[0]
#
# c['3'] = [['2',"3time", "something"]]
#
# d.writeAllChatLogs(c)
# for one in d.readAllChatLogs():
#     print one, chatlogs[one]
