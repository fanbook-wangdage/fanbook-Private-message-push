import json
import requests
import threading
import time
import warnings

# 禁止警告输出
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

def get_members(token='',tabs=[{"start":0, "end":99}],guid='',chlid='',userid=''):#获取成员列表
    url=f'https://a1.fanbook.mobi/api/bot/{token}/v2/guild/members'
    headers={'Content-Type': 'application/json'}
    body={
    "guild_id":guid,
    "channel_id":chlid,
    "user_id":userid,
    "ranges":tabs
}
    body=json.dumps(body)
    r=requests.post(url,headers=headers,data=body,verify=False)
    return json.loads(r.text)

def getGuildMembersCount(token='',guid=''):
    '''
    url=f'https://a1.fanbook.mobi/api/bot/{token}/getGuildMembersCount'#获取成员数量
    headers={'Content-Type': 'application/json'}
    body=json.dumps({"guild_id":guid})
    r=requests.post(url,headers=headers,data=body)
    print(r.text)
    return json.loads(r.text)
'''
    return {'result':0}

def sendMessage(token='',chlid='',text='',sl=0,yz=0):
    global rok,err,texttype
    url=f'https://a1.fanbook.mobi/api/bot/{token}/getPrivateChat'#获取私聊频道
    headers={'Content-Type': 'application/json'}
    print(chlid)
    body=json.dumps({"user_id":int(chlid)})
    r=requests.post(url,headers=headers,data=body,verify=False)
    da=json.loads(r.text)
    #print(da)
    if yz==1:
        if da["ok"]==true or da["ok"]==True:
            pass
        else:
            print(f'发送第{str(sl+1)}条消息失败，获取私信频道失败')
            err+=1
            print(da)
            return da
        chlid=da["result"]["id"]
    url=f'https://a1.fanbook.mobi/api/bot/{token}/sendMessage'#发送消息
    headers={'Content-Type': 'application/json'}
    if texttype==1 and yz==1:
        body=json.dumps({"chat_id":int(chlid),"text":str(text),"parse_mode":"Fanbook"})
    else:
        body=json.dumps({"chat_id":int(chlid),"text":text})
    r=requests.post(url,headers=headers,data=body,verify=False)
    da=json.loads(r.text)
    if da["ok"]==true or da["ok"]==True:
        print(f'发送第{str(sl+1)}条消息成功')
        rok+=1
    else:
        print(f'发送第{str(sl+1)}条消息失败')
        print(da)
        err+=1
    return json.loads(r.text)

true=True
rok=0
err=0
sl=0
texttype=0

token=input('请输入机器人token')
textdata=input('请输入消息或者消息json数据')
try:
    textdata=json.loads(textdata)
    texttype=1
except:
    pass
chlid=input('请输入被通知成员所在的频道id')
gid=input('请输入服务器id')
botid=input('请输入bot id')

qx=sendMessage(token=token,chlid=chlid,text='1')

notend=True
userids=[]
tabsdata=0

try:
    if qx["ok"]==true or qx["ok"]==True:
        print('验证成功，机器人有权限发送消息')
        rok-=1
        try:
            cysl=getGuildMembersCount(token=token,guid=int(gid))['result']
            print('服务器总成员数量：',str(cysl))
            try:
                while notend:
                    cylb=get_members(token=token,guid=gid,userid=botid,chlid=chlid,tabs=[{"start":tabsdata, "end":tabsdata+99}])
                    rangesdata=cylb['result']["ops"][0]
                    #rangesdata=json.loads(rangesdata[0])
                    rangesdata=rangesdata['items']
                    #print(rangesdata)
                    for x in rangesdata:
                        datatype=x.keys()
                        datatype=list(datatype)
                        if datatype[0]=='User':
                            userids.append(x['User']['user_id'])
                    if len(rangesdata)<99:
                        print('获取完成')
                        notend=False
                        #print(userids)
                    tabsdata+=99
                #启动多个线程运行sendMessage
                for x in userids:
                    #print(x)
                    threading.Thread(target=sendMessage,args=(token,x,textdata,sl,1,)).start()
                    sl+=1
                    time.sleep(0.01)
                time.sleep(5)
                print(f'发送完成，成功{str(rok)}次，失败{str(err)}次')
            except:
                print('获取成员数量失败，你应该检查机器人id和频道id')
                print(cylb)
        except:
            print('获取成员数量失败，你应该检查服务器id')
    else:
        print('机器人没有权限发送消息或没有发送消息白名单')
        print(qx)
except:
    print('token不正确')

input()