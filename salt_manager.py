# -*- coding:utf-8 -*-
import json
import urllib
import urllib2


class SaltApi(object):
    """
    管理SaltStack请求信息
    """
    def __init__(self, url, username, password):
        params = {'eauth': 'pam', 'username': username, 'password': password}
        req = urllib2.Request(url + '/login', urllib.unquote(urllib.urlencode(params)))
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())

        self.url = url
        self.__token = content['return'][0]['token']
        self.headers = {
            'User-agent': 'Mozilla/5.0 (Macintosh; KHTML, like Gecko) Chrome/57.0.2987.110',
            'Accept': 'application/json',
            'X-Auth-Token': self.__token
        }

    def do_request(self, url, data=None):
        req = urllib2.Request(url, data, headers=self.headers)
        opener = urllib2.urlopen(req)
        return json.loads(opener.read())

    def run_cmd(self, encode_data):
        """
        参见salt.models.SaltAction.run
        """
        return self.do_request(self.url, encode_data.strip())

    def job(self, jid=''):
        return self.do_request('%s/jobs/%s' % (self.url, jid))

    def jobs(self):
        return self.do_request(self.url + '/jobs')

    def minion(self, mid):
        return self.do_request('%s/minions/%s' % (self.url, mid))

    def minions(self):
        return self.do_request(self.url + '/minions')

    def events(self):
        return self.do_request(self.url + '/events')

    def keys(self):
        content = self.do_request(self.url + '/keys')
        accepted = content['return']['minions']
        denied = content['return']['minions_denied']
        unaccept = content['return']['minions_pre']
        rejected = content['return']['minions_rejected']
        return accepted, denied, unaccept, rejected

    def accept_key(self, key_id):
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': key_id}
        content = self.do_request(self.url, urllib.unquote(urllib.urlencode(params)))
        return content['return'][0]['data']['success']

    def delete_key(self, key_id):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': key_id}
        content = self.do_request(self.url, urllib.unquote(urllib.urlencode(params)))
        return content['return'][0]['data']['success']

    def cp_url_file(self, url, dst_name, minions):
        """
        salt minions cp.get_url url dst_name makedirs=True
        """
        params = {
            'tgt': ','.join(minions),
            'fun': 'cp.get_url',
            'client': 'local',
            'expr_form': 'list',
        }
        params_str = urllib.unquote(urllib.urlencode(params))
        params_str += '&arg=' + url + '&arg=' + dst_name + '&arg=' + urllib.quote('makedirs=True')
        response = self.run_cmd(params_str)
        return response['return'][0]
