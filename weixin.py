#coding=utf-8

import time, datetime, requests, itchat
from utils import *
from BasicInfo import WeixinInfo

# Receiving Messages and Replying

@itchat.msg_register(TEXT, isMpChat = True, isFriendChat = True)
def text_reply(msg):
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
    if sender_nickname in acl:
        if sender_remarkname != '':
            print('Message from %s(%s):\n%s' % (sender_nickname, sender_remarkname, text))
        else:
            print('Message from %s:\n%s' % (sender_nickname, text))
        print('')
        print('Replied: No Reply')
        print('')
        return 
    if sender_name != wx.myself['UserName']:
        source_language, target_language, translated_text = text_translation(text)
        code_rob_replied, text_rob_replied = rob_reply(text)
        if source_language == 'zh' and text_rob_replied != '':
            if str(code_rob_replied) != '40004':
                msg_reply = u'YAO之助:\n'
                msg_reply += text_rob_replied
            else:
                msg_reply = u'YAO之助:\n我累了，等YAO回来自己说......'
        else:
            msg_reply = ''
            msg_reply += 'YAO is not here.\nNLP is under Construction...\n'
            msg_reply += 'Did you mean:\n'
            msg_reply += '----------------------\n'
            msg_reply += translated_text
            msg_reply += '\n----------------------\n'
        if sender_remarkname != '':
            print('Message from %s(%s):\n%s' % (sender_nickname, sender_remarkname, text))
        else:
            print('Message from %s:\n%s' % (sender_nickname, text))
        print('')
        print('Replied:\n%s' % msg_reply)
        print('')
        return msg_reply
    else:
        return

@itchat.msg_register(TEXT, isGroupChat = True)
def text_reply(msg):
    if msg['isAt']:
        text = msg['Content']
        source_language, target_language, translated_text = text_translation(text)
        code_rob_replied, text_rob_replied = rob_reply(text)
        if source_language == 'zh' and text_rob_replied != '':
            if str(code_rob_replied) != '40004':
                msg_reply = u'YAO之助:\n'
                msg_reply += text_rob_replied
            else:
                msg_reply = u'YAO之助:\n我累了，等YAO回来自己说......'
        else:
            msg_reply = ''
            msg_reply += 'YAO is not here.\nNLP is under Construction...\n'
            msg_reply += 'Did you mean:\n'
            msg_reply += '----------------------\n'
            msg_reply += translated_text
            msg_reply += '\n----------------------\n'
            itchat.send(msg_reply)

def main():
    global wx
    # Log in via QR code
    itchat.auto_login(hotReload = True)    # hotReload=True: Keep the login state after the program quits

    wx = WeixinInfo()
#    official_account = wx.search_OfficialAccount(u'方脑壳被驴踢')

    # Listening
    itchat.run()


if __name__ == '__main__':
    main()
