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

    def request(data):
        command = json.dumps(data).encode('utf-8')
        signature = hmac.new(DBAccess.config['shakey'].encode('utf-8'),
                             command,
                             hashlib.sha256).hexdigest()
        message = {'command': command, 'signature': signature}
        response = requests.post(DBAccess.config['url'], data=message)
        print(response.text)
        return json.loads(response.text)

def main():
    data = {"A": 123, "ZZZ": "AAAAAsadsa"}
    print(DBAccess.request(data))

if __name__ == '__main__':
    main()
