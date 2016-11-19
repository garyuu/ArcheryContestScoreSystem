'''
Author: Garyuu
Date:   2016/8/15
Name:   message_parser
Descr.: To parse a message from mqtt server.
        The message will be parsed to a command.
        Message format will be like:
            10;11;2;11A;X,10,6,4,3,m

        [Abandoned version]
            10A: X,10, 4, 2, 1, m set2 point:27
        --> 10A:X,10,4,2,1,mset2point:27
        --> [10A, 'X,10,4,2,1,m', 2, 27]
'''
import re

def wave(raw):
    print(raw)
    data = {
        'type'      : 'wave',
        'machine'   : int(raw[0]),
        'position'  : int(raw[1]),
        'wave'      : int(raw[2]),
        'player'    : raw[3],
        'score'     : raw[4].split(','),
    }
    for i in range(0, len(data['score'])):
        if data['score'][i] == 'X':
            data['score'][i] = 11
        elif data['score'][i] == 'm':
            data['score'][i] = 0
        else:
            data['score'][i] = int(data['score'][i])
    data['score'] += [-1] * (6-len(data['score']))
    return data

def short(raw):
    data = {}
    sender = raw[0].split('t')
    data['machine'] = int(sender[0])
    if len(sender) > 1:
        data['position'] = int(sender[1])
    else:
        data['position'] = 0
    if raw[1] == "ready":
        data['type'] = 'ready'
    else:
        data['type'] = 'ok'
    return data

def parse(b_message):
    message = b_message.decode("utf-8")
    if re.search(';', message):
        raw = message.split(';')
        msg = wave(raw)
        msg['message'] = message
    else:
        raw = message.split()
        msg = short(raw)
    return msg

def main():
    print(parse(b"10;11;2;11A;X,10,8,4,2,m"))
    print(parse(b"10t11 ready"))
    print(parse(b"10t11 received"))

if __name__ == "__main__":
    main()
