'''
Author: NekOrz
Date:   2016/8/14
Name:   sql_function
Descr.: This file contain many function to let SQL really eazy(?)
'''
import MySQLdb

class SqlWrapper():
    def __init__(self):
        try:
            self.db = MySQLdb.connect(host="localhost", user="python", passwd="admin", db="ccsu99_cs_archery_contest")
        except:
            print("cannot login!")
            return
        self.cur= self.db.cursor()
    
    def Add_Entry(self,name,department,position,id):
        self.cur.execute("INSERT INTO players (name,department,position,id) VALUES ('%s','%s','%s',%d);"%(name,department,position,id))
        self.db.commit()
    
    def Add_Entry_By_Player(self,player):
        self.Add_Entry(player[0],player[1],player[2],player[3]);
        
def main():
    a = SqlWrapper()
    a.Add_Entry_By_Player(['joe3','r','w',45])
    print("??")

if __name__ == '__main__':
    main()
    


