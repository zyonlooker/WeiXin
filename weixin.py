#coding=utf-8

import os, time, datetime, requests, itchat
from utils import *
from BasicInfo import WeixinInfo

# Display the message on the screen
def display_message(text, sender_remarkname, sender_nickname):
    if sender_remarkname != '':
        print('{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
        print('Message from %s(%s):\n%s' % (sender_nickname, sender_remarkname, text))
    else:
        print('{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
        print('Message from %s:\n%s' % (sender_nickname, text))
    print('')
    return

# Receiving Messages and Replying

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, ATTACHMENT, VIDEO], isMpChat = True, isFriendChat = True)
def text_reply(msg):
    # Get the information of received messages
    MsgType = msg['MsgType']
    text = msg['Content']
    sender_name = msg['FromUserName']
    receiver_name = msg['ToUserName']

    friends = wx.get_friends()
    sender_nickname = u'微信团队'
    sender_remarkname = u'微信团队'
    for sender in friends:
        if sender['UserName'] == sender_name:
            sender_nickname = sender['NickName']
            sender_remarkname = sender['RemarkName']
            break
    else:
        official_accounts = wx.get_official_accounts()
        for sender in official_accounts:
            if sender['UserName'] == sender_name:
                sender_nickname = sender['NickName']
                sender_remarkname = sender['RemarkName']
                break

    # Switch on-off for auto-reply control.
    # Off
    if text == u'闭嘴':
        not_in_acl = None
        with open('acl.cfg', 'r') as f:
            for line in f:
                if sender_nickname == line.strip('\n') \
                    or \
                (sender_remarkname and sender_remarkname == line.strip('\n')):
                    break
            else:
                not_in_acl = True
        if not_in_acl:
            with open('acl.cfg', 'a') as f:
                f.write(sender_nickname)
                f.write('\n')
                if sender_remarkname:
                    f.write(sender_remarkname)
                f.write('\n')
                prompt = 'YAO之助:\n好，我走了。呼唤"YAO之助"我就回来了～'
                display_message(text, sender_remarkname, sender_nickname)
                print(prompt + '\n')
                return prompt
    # On                
    if text == u'YAO之助':
        in_acl = None
        with open('acl.cfg', 'r') as f:
            for line in f:
                if sender_nickname == line.strip('\n') \
                    or \
                (sender_remarkname and sender_remarkname == line.strip('\n')):
                    in_acl = True
        if in_acl:
            f = 'acl.cfg'
            if sender_remarkname:
                s = sender_remarkname
                os.system('sed -i \'/%s/d\' %s' % (s, f))
                s = sender_nickname
                os.system('sed -i \'/%s/d\' %s' % (s, f))
            else:
                s = sender_nickname
                os.system('sed -i \'/%s/d\' %s' % (s, f))
            prompt = 'YAO之助:\n我回来了～'
            display_message(text, sender_remarkname, sender_nickname)
            print(prompt + '\n')
            return prompt
           
    # ACL. Senders in the list will not be replied.
    acl = open('acl.cfg', 'r').read().split('\n')
    if sender_nickname in acl or (sender_remarkname and sender_remarkname in acl):
        if sender_name == wx.myself['UserName']:
            return
        else:
            display_message(text, sender_remarkname, sender_nickname)
        print('Replied: No Reply')
        print('')
        return 

    # Auto reply if the message was not from myself
    # Store the image from mobile
    if sender_name == wx.myself['UserName']:
        if str(MsgType) == '3' and\
            receiver_name == sender_name: # Picture send to myself
            msg['Text']('image/%s' % msg.fileName)
            display_message('Image', '', 'YAO')
            print('Image has been downloaded.')
            print('')
        return
    else:
        if str(MsgType) == '1':
            if chinese_detect(text):
                msg_replied = rob_reply(text)
                msg_replied += '\n（你可以让我闭嘴～）'
            else:
                msg_replied = text_translation(text)
            display_message(text, sender_remarkname, sender_nickname)
            print('Replied:\n%s' % msg_replied)
            print('')
            return msg_replied
        else:
            msg_replied = 'Message received, YAO will handle it when he comes back!'
            display_message(text, sender_remarkname, sender_nickname)
            print('Replied:\n%s' % msg_replied)
            print('')
            return msg_replied

@itchat.msg_register(TEXT, isGroupChat = True)
def text_reply(msg):
    if msg['isAt']:
        text = msg['Content']
        if chinese_detect(text):
            msg_replied = rob_reply(text)
        else:
            msg_replied = text_translation(text)
        itchat.send(msg_replied)


# Audio Messages reply

@itchat.msg_register([RECORDING], isMpChat = True, isFriendChat = True)
def audio_reply(msg):
    # Get the information of the received audio
    text = msg['Content']
    sender_name = msg['FromUserName']
    friends = wx.get_friends()
    sender_nickname = None
    sender_remarkname = None
    for sender in friends:
        if sender['UserName'] == sender_name:
            sender_nickname = sender['NickName']
            sender_remarkname = sender['RemarkName']
            break
    else:
        official_accounts = wx.get_official_accounts()
        for sender in official_accounts:
            if sender['UserName'] == sender_name:
                sender_nickname = sender['NickName']
                sender_remarkname = sender['RemarkName']
                break
    # Download the audio
    msg['Text']('audio/%s' % msg.fileName)
    current_path = os.path.abspath('.')
    audio_file_s = current_path + '/audio/' + msg.fileName
    audio_file_d = current_path + '/audio/'\
                + os.path.split(audio_file_s)[1].split('.')[0]\
                + '.pcm'
    os.system('ffmpeg -y -i %s -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s > /dev/null 2>&1' % (audio_file_s, audio_file_d))
    msg_replied = audio_to_text(audio_file_d)
    os.system('rm -f %s %s' % (audio_file_s, audio_file_d))
    display_message(text, sender_remarkname, sender_nickname)
    print('Replied:\n%s' % msg_replied)
    print('')
    return msg_replied


def main():
    global wx
    # Log in via QR code
    itchat.auto_login(hotReload = True)    # hotReload=True: Keep the login state after the program quits

    wx = WeixinInfo()

    # Listening
    itchat.run()


if __name__ == '__main__':
    main()
