'''
Author: Garyuu
Date:   2016/11/18
Name:   message_manager
Descr.: Manage status massages
'''

class MessageManager:
    def __init__(self):
        self.message = []

    def __str__(self):
        output = ""
        for i in range(-10, 0):
            try: 
                output += self.message[i]
            except:
                continue
        return output

    def __iadd__(self, other):
        self.message.append(other)
        return self
