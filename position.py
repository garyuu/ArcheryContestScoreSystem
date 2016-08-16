'''
Author: NekOrz, Garyuu
Date:   2016/8/15
Name:   position
Descr.: The object that serves as a signal/timer thingy
'''
#import time
import threading


class Position():
    count = 0

    def __init__(self,num,id=0):
        self.id = id
        self.state = 1 # 1:OK, 0:waiting , -1:dead
        self.num = num
    
    def __str__(self):
        if self.state == 1:
            if self.count == 0:
                return "OK"
            else:
                return "OK Got:{}".format(self.count)
        elif self.state == 0:
            return "Waiting"
        else:
            return "Dead"
    
    def ChangeStateToWait(self,sec = 10.0):
        self.state = 0
        self.timer = threading.Timer(sec,self.ChangeStateToDead)
        self.timer.start()
        
    def ChangeStateToDead(self):
        self.state = -1
    
    def ChangeStateToOK(self):
        self.timer.cancel()
        self.state = 1
    
    def AddCount(self):
        self.count += 1

    def ResetCount(self):
        self.count = 0
        
def main():
    p = Position()
    
    p.ChangeStateToWait(1)
    print("YAY!")
    print(p)
    while p != -1:
        print(p)
    p.ChangeStateToOK()
    print(p)
    
if __name__ == '__main__':
    main()
    


    
    
    
    
    
    
    

    
