#!/usr/bin/env python
# -*- coding: utf-8 -*-

def PrintInfo(info):
    print info.decode('utf-8').encode('utf-8')  

import threading

#单例类
class Singleton():
    instance=None
    mutex=threading.Lock()

    def _init__(self):
        pass

    @staticmethod
    def GetInstance():
        if(Singleton.instance==None):
            Singleton.mutex.acquire()
            if(Singleton.instance==None):
                PrintInfo('初始化实例')
                Singleton.instance=Singleton()
            else:
                PrintInfo('单例已经实例化')
            Singleton.mutex.release()
        else:
            PrintInfo('单例已经实例化')

        return Singleton.instance

def clientUI():
    Singleton.GetInstance()
    Singleton.GetInstance()
    Singleton.GetInstance()
    return

if __name__=='__main__':
    clientUI();
    
