#!/usr/bin/env python
# -*- coding: utf-8 -*-

class User(object):
    def __init__(self, uid, uname, pic, profile):
        self.uid = uid
        self.uname = uname
        self.pic = pic
        self.profile = profile

    def setUid(self, uid):
        self.uid = uid

    def setUname(self, uname):
        self.uname = uname

    def setPic(self, pic):
        self.pic = pic

    def setProfile(self, profile):
        self.profile = profile

    def getUid(self):
        return self.uid

    def getUname(self):
        return self.uname

    def getPic(self):
        return self.pic

    def getProfile(self):
        return self.profile

# Test
# t = User("1", "ou", "1.jpg", "jiaqi欧")
# print t.getUid(),t.getUname(), t.getPic(), t.getProfile()
# t.setUid("2")
# t.setPic("2.jpg")
# t.setUname("wang")
# t.setProfile("yujing")
# print t.getUid(),t.getUname(), t.getPic(), t.getProfile()
