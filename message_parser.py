'''
Author: Garyuu
Date:   2016/8/15
Name:   message_parser
Descr.: To parse a message from mqtt server.
        The message will be parsed to a command.
        Message format will be like:
            10A: X,5,4,2,1,m set2 point:22
'''
def wave(raw):
    data = {
        'type'      : 'wave',
        'player'    : raw[0][:-1],
        'score'     : raw[1].split(','),
        'wave'      : raw[2][4:],
        'total'     : raw[3][6:],
        'message'   : message,
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

def parse(message):
    raw = message.split()
    if len(raw) > 2:
        return wave(raw)
    else:
        return short(raw)
