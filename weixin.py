import time, datetime, requests, itchat
from utils import *
from BasicInfo import WeixinInfo

# Receiving Messages and Replying

@itchat.msg_register(TEXT, isMpChat = True, isFriendChat = True)
def text_reply(msg):
    text = msg['Content']
    sender_name = msg['FromUserName']
    friends = wx.get_friends()
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
    if sender_name != wx.myself['UserName']:
        translated_text = text_translation(text)
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
        return msg_reply
    else:
        return

@itchat.msg_register(TEXT, isGroupChat = True)
def text_reply(msg):
    if msg['isAt']:
        msg_reply = ''
        msg_reply += 'YAO is not here. Debugging...\n'
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
