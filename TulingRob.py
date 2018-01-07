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

        result = requests.post(api_url, data = data).json()
        result['text'] = result['text'].replace('图灵工程师妈妈', '冬雪腊梅')
        result['text'] = result['text'].replace('图灵工程师爸爸', '绿水青山')
        return result
