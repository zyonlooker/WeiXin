#coding=utf-8

import time, datetime, requests, itchat
from utils import *
from BasicInfo import WeixinInfo

# Receiving Messages and Replying

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO], isMpChat = True, isFriendChat = True)
def text_reply(msg):
    MsgType = msg['MsgType']
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
            
    # ACL. Senders in the list will not be replied.
    acl = open('acl.cfg', 'r').read().split('\n')
    if sender_nickname in acl or sender_remarkname in acl:
        if sender_remarkname != '':
            print('Message from %s(%s):\n%s' % (sender_nickname, sender_remarkname, text))
        else:
            print('Message from %s:\n%s' % (sender_nickname, text))
        print('')
        print('Replied: No Reply')
        print('')
        return 

    if sender_name != wx.myself['UserName']:
        if str(MsgType) == '1':
            if chinese_detect(text):
                msg_replied = rob_reply(text)
            else:
                msg_replied = text_translation(text)
            if sender_remarkname != '':
                print('Message from %s(%s):\n%s' % (sender_nickname, sender_remarkname, text))
            else:
                print('Message from %s:\n%s' % (sender_nickname, text))
            print('')
            print('Replied:\n%s' % msg_replied)
            print('')
            return msg_replied
        else:
            msg_replied = 'Message received, Yao will handle it when he comes back!'
            if sender_remarkname != '':
                print('Message from %s(%s):\n%s' % (sender_nickname, sender_remarkname, text))
            else:
                print('Message from %s:\n%s' % (sender_nickname, text))
            print('')
            print('Replied:\n%s' % msg_replied)
            print('')
            return msg_replied
    else:
        return

@itchat.msg_register(TEXT, isGroupChat = True)
def text_reply(msg):
    if msg['isAt']:
        text = msg['Content']
        if chinese_detect(text):
            msg_replied = text_rob_reply(text)
        else:
            msg_replied = text_translation(text)
        itchat.send(msg_reply)

def main():
    global wx
    # Log in via QR code
    itchat.auto_login(hotReload = True)    # hotReload=True: Keep the login state after the program quits

    wx = WeixinInfo()

    # Listening
    itchat.run()


if __name__ == '__main__':
    main()
