#/usr/bin/env python3
#coding=utf8
 
import http.client
import hashlib
import urllib.parse
import random


class BaiduTranslator:

    def __init__(self, fromLang='auto', toLang='en'):
        '''
        A BaiduTranslator Class
        '''
        return

    def translate(self, q, fromLang='auto', toLang='en'):
        q = q.replace('\n', '~~~~~')
        self.fromLang = fromLang
        self.toLang = toLang
        myurl = '/api/trans/vip/translate'
        baidu = eval(open('baidu_api.key', 'r').read().strip('\n'))
        app_id = baidu['app_id']
        key = baidu['key']
        salt = random.randint(32768, 65536)
        sign = app_id + q + str(salt) + key
        m1 = hashlib.md5()
        m1.update(bytes(sign, 'utf-8'))
        sign = m1.hexdigest()
        myurl = myurl + '?appid=' + app_id + '&q=' + urllib.parse.quote(q) + '&from=' + self.fromLang + '&to=' + self.toLang + '&salt=' + str(salt) + '&sign=' + sign
        api = 'api.fanyi.baidu.com'
 
        try:
            httpClient = http.client.HTTPConnection(api)
            httpClient.request('GET', myurl)
 
            #response is an HTTPResponse object
            response = httpClient.getresponse()
            result = eval(response.read())
            result['trans_result'][0]['dst'] = result['trans_result'][0]['dst'].replace('~~~~~', '\n')
        except Exception as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()
        return result
