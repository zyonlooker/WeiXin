# Weixin Functions
import datetime, itchat
from itchat.content import *

# Sending Messages (Text, Pictures, Files, Videos)

# Text
def send_text(text, UserName):
    reply = itchat.send(text + '\n' + 'Sending Time:\n{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()), toUserName = UserName)
    print(text)
    print('Sending text ' + reply['BaseResponse']['ErrMsg'])

# Picture
def send_image(image, UserName):
    reply = itchat.send('@img@' + image, toUserName = UserName)
    print('Sending picture ' + reply['BaseResponse']['ErrMsg'])

# File
def send_file(file_name, UserName):
    reply = itchat.send('@fil@' + file_name, toUserName = UserName)
    print('Sending file ' + reply['BaseResponse']['ErrMsg'])

# Video
def send_video(video, UserName):
    reply = itchat.send('@vid@' + video, toUserName = UserName)
    print('Sending video ' + reply['BaseResponse']['ErrMsg'])


# Translate Messages
import BaiduTranslate
def text_translation(text):
    translate = BaiduTranslate.BaiduTranslator()
    result = translate.translate(text)
    if result['from'] == result['to']:
        result = translate.translate(text, toLang='zh')
        translated_text = result['trans_result'][0]['dst']
    else:
        translated_text = result['trans_result'][0]['dst']
    return translated_text

