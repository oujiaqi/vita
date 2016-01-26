#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

class VitaProtocol(object):

    def __init__(self):
        self.splitRe = re.compile('<\$\$(?P<id>\w+)\$\$>\n\n([\s|\S]*?)\n\n</\$\$(?P=id)\$\$>')


    # 输入一串连续字符串，输入字符串格式不定
    # 首先处理成"<$$Method$$>\n\nContent\n\n</$$Method$$>"的单条字符串
    # 再对单挑字符串处理
    # 返回 (AfterRawData, Method, Content)
    # AfterRawData 是 rawData 从开头截取到 OneRawData 的剩余字符串
    # 截取具有最小性
    # 其中Content会对应相应的数据，该类型为list [content]
    # Method 数据类型为string，表示类型
    def handleRawData(self, RawData):
        Data = self.splitRe.search(RawData)
        if Data:
            method, content = Data.groups()
            AfterRawData = RawData[Data.end():]
            if method == "ChatMsg":
                return (AfterRawData, method, [content])
            if method == "Close":
                return (AfterRawData, method, [content])
            if method == "Indentity":
                return (AfterRawData, method, content.split("\n"))
        else:
            return (RawData, "", [])

    def handleChatMsg(self, chatMsg):
        return "<$$ChatMsg$$>\n\n"+chatMsg+"\n\n</$$ChatMsg$$>"

    def handleClose(self):
        return "<$$Close$$>\n\n\n\n</$$Close$$>"

    def handleIdentity(self, myId, yourId):
        return "<$$Indentity$$>\n\n"+myId+"\n"+yourId+"\n\n</$$Indentity$$>"
