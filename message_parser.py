'''
Author: Garyuu
Date:   2016/8/15
Name:   message_parser
Descr.: To parse a message from mqtt server.
        The message will be parsed to a command.
        Message format will be like:
            10A: X,5,4,2,1,m set2 point:22
'''
def parse(message):
    raw = message.split()
    data = {
        'player'    : raw[0][:-1],
        'score'     : raw[1].split(','),
        'wave'      : raw[2][4:],
        'total'     : raw[3][6:],
    }
    return data
