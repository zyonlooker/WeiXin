import time, datetime, requests, itchat
from itchat.content import *

class WeixinInfo():

    def __init__(self):
        # Fetch Myself's Information
        myself = itchat.search_friends()
        self.myself = myself
        print('Login Information:')
        print('-------------------')
        print('UserName:    %s' % self.myself['UserName'])
        print('NickName:    %s' % self.myself['NickName'])
        print('Signature:   %s' % self.myself['Signature'])
        print('-------------------')


    # Fetch Friends' Information
    def get_friends(self):
        return itchat.get_friends()

    # Fetch Official Accounts' Information
    def get_official_accounts(self):
        return itchat.get_mps()


    # Search Friend
    def search_friend(self, name_str):
        friend = itchat.search_friends(name = name_str)
        #for i in range(0, len(friend)):
        #    print('UserName:    %s' % friend[i]['UserName'])
        #    print('NickName:    %s' % friend[i]['NickName'])
        #    print('Alias:       %s' % friend[i]['Alias'])
        #    print('RemarkName:  %s' % friend[i]['RemarkName'])
        return friend


    # Search Official Accounts
    def search_OfficialAccount(self, name_str):
        official_account = itchat.search_mps(name = name_str)
        #for i in range(0, len(official_account)):
        #    print('UserName:    %s' % official_account[i]['UserName'])
        #    print('NickName:    %s' % official_account[i]['NickName'])
        #    print('Signature:   %s' % official_account[i]['Signature'])
        return official_account


    # Search Groups
    def search_group(self, name_str):
        group = itchat.search_chatrooms(name = name_str)
        #for i in range(0, len(group)):
        #    print('UserName:    %s' % group[i]['UserName'])
        #    print('NickName:    %s' % group[i]['NickName'])
        #    print('%s Members in total' % group[i]['MemberCount'])
        #    print('Owner:       %s' % group[i]['Self']['NickName'])
        return group

