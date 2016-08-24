'''
Author: NekOrz
Date:   2016/8/15
Name:   sql_wrapper
Descr.: This file contain many function to let SQL really eazy(?)
'''
import pymysql

class SQLWrapper():
    def __init__(self,host="localhost", user="python", passwd="admin", db="ccsu99_cs_archery_contest"):
        #try:
        self.db = pymysql.connect(host,user,passwd,db)
        #except:
        #    print("cannot login!")
        #    return
        self.cur = self.db.cursor()
    
    def AddPlayer(self,name,department,position,tag):
        self.cur.execute("INSERT INTO players (name,department,position,tag) VALUES ('{}','{}',{},'{}');".format(name,department,position,tag))
        self.db.commit()
    
    def AddPlayerByList(self,player):
        self.AddPlayer(player[0],player[1],player[2],player[3]);
       
    def AddWave(self,mode,number,pid,id,shots_raw): #shots_raw have to be a list.
        if type(shots_raw) is not list:
            print("Shots_raw have to be a list! Even a NULL list([]) will work!")
            return -1
        shots = [-1,-1,-1,-1,-1,-1]
        for i in range(0,len(shots_raw)):
            shots[i] = shots_raw[i]
        self.cur.execute("INSERT INTO waves (mode,number,pid,id,shot1,shot2,shot3,shot4,shot5,shot6) VALUES (%d,%d,%d,'%s',%d,%d,%d,%d,%d,%d);"%(mode,number,pid,id,shots[0],shots[1],shots[2],shots[3],shots[4],shots[5]))
        self.db.commit()
        
    def AddWaveByList(self,wave):
        self.AddWave(wave[0],wave[1],wave[2],wave[3],wave[4:])
    
    def GetScoreById(self,id,pid): #Shot can be -1, which means no score.
        self.cur.execute("SELECT shot1,shot2,shot3,shot4,shot5,shot6 FROM waves WHERE id == '{}' AND pid == {} ORDER BY number".format(id, pid))
        return self.cur.fetchall()
#        rr = []
#        for i in range(0,len(r)):
#            buf = []
#            for j in range(1,7):
#                buf.append(r[i]['shot{0}'.format(j)])
#            rr.append(buf)
#        return rr
    
    def GetPlayerTagByPos(self,pos): #1d-list
        self.cur.execute("SELECT tag FROM players WHERE position == {};".format(pos))
        r = self.cur.fetchall()
        rr = []
        for i in range(0,len(r)):
            rr.append(r[i][0])
        return rr
    
    def GetIdByTag(self,tag):
        self.cur.execute("SELECT id FROM players WHERE tag == '{}';".format(tag))
        r = self.cur.fetchall()
        return r[0][0]
    
def main():
    a = SQLWrapper()
    a.AddWaveByList([4,8,9,'j'])
    r = a.GetIdByPos('1C')
    print(r)
    for i in range(0,len(r)):
        for j in range(0,len(r[i])):
            print(r[i][j]),
        print("")
    print("??")

if __name__ == '__main__':
    main()
