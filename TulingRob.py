#coding=utf-8

import requests

class Robot:
    def __init__(self, user='YAO'):
        self.user = user

    def get_message(self, text):
        api = eval(open('tuling_api.key', 'r').read())
        api_url = api['url']
        api_key = api['key']

        user = self.user
        data = {
                'key': api_key,
                'userid': user,
                'info': text,
        }

        r = requests.post(api_url, data = data).json()
        r['text'] = r['text'].replace('图灵工程师妈妈', '冬雪腊梅')
        r['text'] = r['text'].replace('图灵工程师爸爸', '绿水青山')
        code = r['code']
        content = r['text']
        # News and Recipe, delete the '?' followed sub-string
        if str(code) == '302000' or str(code) == '308000':
            content += '\n'
            for item in r['list']:
                content += '\n'
                for key in item:
                    if key != 'icon':
                        # delete the reference
                        url = item[key].split('?')
                        content += url[0] + '\n'
        return code, content
