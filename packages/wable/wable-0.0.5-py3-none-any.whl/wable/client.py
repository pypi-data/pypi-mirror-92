import requests
"""
A client to communicate with https://wable.org api.
"""

root = 'https://api.wable.org/api/v1'


class Wable:
    customer = {
        'auth_token': None,
        'phone_number': None,
        'is_new': None,
        'has_requested_reset': None
    }

    def customer_exists(self, phone_number):
        r = requests.post(
            f'{root}/user_exists', json={'phone_number': phone_number}
        )
        if (not r.ok):
            raise Exception('Invalid credentials')
        c = r.json()
        self.customer = {**self.customer, **c}
        return c['is_new']


def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial
