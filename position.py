'''
Author: NekOrz
Date:   2016/8/15
Name:   position
Descr.: The object that serves as a signal/timer thingy
'''
#import time
import threading


class Position():
    def __init__(self,id=0):
        self.id = 0
        self.state = 1 # 1:OK, 0:waiting , -1:dead
    
    def __str__(self):
        if self.state == 1:
            return "OK"
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
    
    
        
def main():
    p = Position()
    
    p.ChangeStateToWait(1)
    print "YAY!"
    print p
    while p != -1:
        print p
    p.ChangeStateToOK()
    print p
    
if __name__ == '__main__':
    main()
    


    
    
    
    
    
    
    
    
    