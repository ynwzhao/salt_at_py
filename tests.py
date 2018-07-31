# -*- coding:utf-8 -*-
import urllib
from salt_manager import SaltApi

SALT_URL = 'http://dn:port'
SALT_USER = 'xxx'
SALT_PASS = 'xxx'

salt_api = SaltApi(SALT_URL, SALT_USER, SALT_PASS)


def md5_of_file(salt, minion_id, filename):
    cmd = 'md5sum %s' % filename
    params = {
        'tgt': minion_id,
        'fun': 'cmd.run',
        'client': 'local',  # 同步方式执行
        'expr_form': 'list',
    }
    params_str = urllib.unquote(urllib.urlencode(params))
    params_str += '&arg=' + urllib.quote(cmd)
    response = salt.run_cmd(params_str)
    return response



if __name__ == '__main__':
    # print salt_api.keys()
    # print salt_api.minions()['return'][0].keys()
    # print salt_api.minion('cn-ali-sh-qwzl-all-redis-s-106-15-182-3-xhhd')
    print md5_of_file(salt_api, 'cn-ali-sh-qwzl-all-redis-s-106-15-182-3-xhhd', '/etc/hosts')
