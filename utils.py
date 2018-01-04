# Weixin Functions
import datetime, itchat
from itchat.content import *
import BaiduTranslate
import TulingRob

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
def text_translation(text):
    translate = BaiduTranslate.BaiduTranslator()
    result = translate.translate(text)
    source_language = result['from']
    target_language = result['to']
    if source_language == target_language:
        result = translate.translate(text, toLang='zh')
        translated_text = result['trans_result'][0]['dst']
    else:
        translated_text = result['trans_result'][0]['dst']
    return source_language, target_language, translated_text

# Tuling Robot Reply
def rob_reply(text):
    rob = TulingRob.Robot()
    replied_text = rob.get_message(text)
    return replied_text

# Reply Messages
def reply_message(text):
    translate = BaiduTranslate.BaiduTranslator()
    result = translate.translate(text)
    if result['from'] == result['en']:
        result = translate.translate(text, toLang='zh')
        replied_text = result['trans_result'][0]['dst']
    else:
        replied_text = rob_reply
    return replied_text
