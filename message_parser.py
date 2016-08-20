'''
Author: Garyuu
Date:   2016/8/15
Name:   message_parser
Descr.: To parse a message from mqtt server.
        The message will be parsed to a command.
        Message format will be like:
            10A: X,10, 4, 2, 1, m set2 point:27
        --> 10A:X,10,4,2,1,mset2point:27
        --> [10A, 'X,10,4,2,1,m', 2, 27]
'''
import re

def wave(raw):
    if __name__ == "__main__":
        print(raw)
    data = {
        'type'      : 'wave',
        'player'    : raw[0],
        'score'     : raw[1].split(','),
        'wave'      : raw[2],
        'total'     : raw[3],
    }
    for i in range(0, len(data['score'])):
        if data['score'][i] == 'X':
            data['score'][i] = 11
        elif data['score'][i] == 'm':
            data['score'][i] = 0
        else:
            data['score'][i] = int(data['score'][i])
    return data

def short(raw):
    if raw[1] == "ready":
        data = {'type': 'ready'}
    else:
        data = {'type': 'ok'}
    data['position'] = raw[0]
    return data

def parse(b_message):
    message = b_message.decode("utf-8")
    if re.search(":", message):
        nospace_message = re.sub(r"\s+", "", message)
        player_mark = nospace_message.find(':')
        wave_mark = re.search(r"set[0-9]+", nospace_message).start()
        total_mark = re.search(r"point:[0-9]+", nospace_message).start()
        raw = [
            nospace_message[:player_mark],
            nospace_message[player_mark+1:wave_mark],
            nospace_message[wave_mark+3:total_mark],
            nospace_message[total_mark+6:]
        ]
        msg = wave(raw)
        msg['message'] = message
    else:
        raw = message.split()
        msg = short(raw)
    return msg

def main():
    print(parse(b"10C: X, X, X, X,10,10 set1 point:60"))
    print(parse(b"10 ready"))
    print(parse(b"10 received"))

if __name__ == "__main__":
    main()
