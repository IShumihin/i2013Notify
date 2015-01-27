# -*- coding: utf-8 -*-

import requests

from .exception import i2013NotifyError


try:
    from django.conf import settings

    if not settings.configured:
        settings.configure()
    dj = True
except:
    dj = False


class i2013Notify(object):
    """Sending message to hubs of the company by xmpp protocol"""

    def __init__(self, url=None, login=None, passwd=None, referer='python notyfy', debug=False):
        if dj == False:
            self.url = url
            self.login = login
            self.passwd = passwd
            self.referer = referer
            self.debug = debug
        else:
            self.url = getattr(settings, 'I_2013_NOTIFY_URL', url)
            self.login = getattr(settings, 'I_2013_NOTIFY_LOGIN', login)
            self.passwd = getattr(settings, 'I_2013_NOTIFY_PASSWD', passwd)
            self.referer = getattr(settings, 'I_2013_NOTIFY_REFERER', referer)
            self.debug = getattr(settings, 'I_2013_NOTIFY_DEBUG', debug)
        if self.url is None or len(self.url) == 0:
            raise i2013NotifyError("url must be a string greater than zero, {0} given".format(str(self.url)))
        if self.login is None or len(self.login) == 0:
            raise i2013NotifyError("login must be a string greater than zero, {0} given".format(str(self.login)))
        if self.passwd is None or len(self.passwd) == 0:
            raise i2013NotifyError("passwd must be a string greater than zero, {0} given".format(str(self.passwd)))


    def send_message(self, message='error message', hub=None):
        if message is None or len(message) < 6:
            raise i2013NotifyError("message must be a string greater than 6, {0} given".format(str(self.passwd)))
        if dj == True:
            hub = getattr(settings, 'I_2013_NOTIFY_HUB', hub)
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