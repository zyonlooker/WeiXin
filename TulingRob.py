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
        content = r['text']
        if 'list' in r.keys():
            content += '\n'
            for item in r['list']:
                content += '\n'
                for key in item:
                    if key != 'icon':
                        content += item[key].strip('?ref=tuling')+ '\n'
        if 'url' in r.keys():
            content += '\n'
            content += r['url'] + '\n'
        return content
