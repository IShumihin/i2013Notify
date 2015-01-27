# -*- coding: utf-8 -*-

import requests


class i2013Notify(object):
    """Sending message to hubs of the company by xmpp protocol"""

    def __init__(self, url='', login='', passwd='', referer='python notyfy', debug=False):
        self.url = url
        self.login = login
        self.passwd = passwd
        self.referer = referer
        self.debug = debug


    def sendMessage(self, message='error message', hub=''):
        hubUri = "http://{0}/hubs/{1}/message".format(self.url, hub)
        fields = {
            "message[text]": message
        }
        headers = {
            'Accept': 'application/vodka-style.1.0+json',
            'referer': self.referer
        }
        try:
            r = requests.post(url=hubUri, data=fields, headers=headers,
                              auth=requests.auth.HTTPBasicAuth(self.login, self.passwd),
                              timeout=(7.0, 10.0))
        except Exception as e:
            if self.debug:
                return e.message
            else:
                return False
        else:
            if self.debug:
                return r.content
            else:
                if r.status_code == 200:
                    return True
                else:
                    return False