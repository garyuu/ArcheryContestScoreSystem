'''
Author: Garyuu
Date:   2016/8/30
Name:   dbaccess
Descr.: Connection to database for data access.
        Use SHA-256 for signature.
'''
import requests
import hmac
import hashlib
import configuration
import json

class DBAccess:
    config = configuration.SectionConfig('db', 'DB')

    def generate_signature(command_string):
        signature = hmac.new(DBAccess.config['shakey'].encode('utf-8'),
                             command_string,
                             hashlib.sha256).hexdigest()
        return signature

    def request(data):
        command = json.dumps(data).encode('utf-8')
        signature = DBAccess.generate_signature(command)
        message = {'command': command, 'signature': signature}
        response = requests.post(DBAccess.config['url'], data=message)
        print(response.text)
        return json.loads(response.text)

def main():
    data = {
        'action': 'allplayerlist',
        'stage': 'practice',
        'team': False,
    }
    print(DBAccess.request(data))

if __name__ == '__main__':
    main()
