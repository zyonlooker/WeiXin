# Weixin Functions
import datetime, itchat
from itchat.content import *
import BaiduTranslate
import BaiduAudio
import TulingRob

# Chinese Detect
def chinese_detect(text):
    zh = 0
    other = 0
    for char in text:
        # include general symbols and digits that from 0020 to 0040
        if (char >= '\u4e00' and char <= '\u9fff') \
                or (char > '\u0020' and char <= '\u0040'):
            zh += 1
        else:
            other += 1
    if other > 4 * zh:
        return False
    else:
        return True


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


# Message Reply

# Temporary Reply
def temporary():
    #message = u'YAO在户外旅行，一切消息等他回来回复。\nYAO is traveling. You will be replied when YAO comes back.'
    message = 'test message'
    msg_reply = u'YAO之助:\n'
    msg_reply += message
    return msg_reply

# Translated Messages
def text_translation(text):
    translate = BaiduTranslate.BaiduTranslator()
    result = translate.translate(text, toLang='zh')
    msg_reply = ''
    msg_reply += 'YAO is not here.\nNLP is under Construction...\n'
    msg_reply += 'Did you mean:\n'
    msg_reply += '--------------------------\n'
    msg_reply += result['trans_result'][0]['dst']
    msg_reply += '\n--------------------------\n'
    return msg_reply

# Tuling Robot Reply
def rob_reply(text):
    rob = TulingRob.Robot()
    result = rob.get_message(text)
    # News and Recipe, delete the '?' followed sub-string
    if str(result['code']) == '302000' or str(result['code']) == '308000':
        text_rob_replied = result['text']
        text_rob_replied += '\n'
        for item in result['list']:
            text_rob_replied += '\n'
            for key in item:
                if key != 'icon':
                    # delete the reference
                    url = item[key].split('?')
                    text_rob_replied += url[0] + '\n'
    else:
        text_rob_replied = result['text']
        if 'url' in result.keys():
            text_rob_replied += '\n'
            text_rob_replied += result['url']
    if str(result['code']) != '40004':
                msg_reply = u'YAO之助:\n'
                msg_reply += text_rob_replied
    else:
        msg_reply = u'YAO之助:\n我累了，等YAO回来自己和你说......'
    return msg_reply

# Audio Reply
def audio_to_text(audio_file):
    audio = BaiduAudio.Audio()
    result = audio.speech_recognise(audio_file)
    if result['err_no'] != 0:
        text = 'YAO\'s Assistant:\nPardon? I couldn\'t hear clearly. I\'m sorry!'
        msg_reply = text + '\n'
    else:
        text = result['result'][0].strip('，')
        msg_reply = ''
        msg_reply += u'YAO之助收到！你可能说的是：\n'
        msg_reply += '--------------------------\n'
        msg_reply += text
        msg_reply += '\n--------------------------\n'
    return msg_reply
