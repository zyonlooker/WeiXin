#/usr/bin/env python3
#coding=utf8

import os, requests, json, base64

class Audio:

    def __init__(self):
        '''
        A BaiduAudio Class
        '''
        return

    def speech_recognise(self, audio_file):
        self.audio_file = audio_file

        baidu = eval(open('baidu_api.key', 'r').read().strip('\n'))
        app_id = baidu['Audio']['app_id']
        api_key = baidu['Audio']['api_key']
        secret_key = baidu['Audio']['secret_key']

        host = 'https://aip.baidubce.com/oauth/2.0/token?' + \
               'grant_type=client_credentials&client_id=' + \
               api_key + '&client_secret=' + secret_key
        token = requests.get(host).json()['access_token']
        cuid = 'YAOWEIXIN'
        headers = {'Content-Type': 'application/json'}
        url = 'https://vop.baidu.com/server_api'
        audio_size = os.path.getsize(audio_file)
        audio64 = base64.b64encode(open(audio_file, 'rb').read())
        audio = audio64.decode('utf-8')

        data = {
                'format': 'pcm',
                'rate': 16000,
                'channel': 1,
                'token': token,
                'cuid': cuid,
                'len': audio_size,
                'speech': audio,
               }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        result = eval(r.text)
        return result
