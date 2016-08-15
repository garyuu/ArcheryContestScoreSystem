'''
Author: Garyuu
Date:   2016/8/15
Name:   message_generator
Descr.: To generate a message string from a dictionary.
        The message string will be published to mqtt server.
'''
def score_sequence(scorelist):
    scoreSeq = ''
    for score in scorelist:
        scoreSeq += "{:0>3}".format(score)
    return scoreSeq

def gen(msg):
    if msg['mode'] == 0:
        message = "{}i{}{}s".format(
            msg['target'],
            msg['mode'],
            msg['wave'],
        )
    else:
        message = "{}i{}{}s{}t{}{}".format(
            msg['target'],
            msg['mode'],
            msg['wave'],
            msg['position'],
            msg['num_players'],
            score_sequence(msg['score'])
        )

