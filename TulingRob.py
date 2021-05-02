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

        return result
