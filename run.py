import hashlib
import urllib
from urllib import parse
import urllib.request
import json
import time
#import itchat
import time, logging, random#, requests
from queue import Queue

from PyWeChatSpy import WeChatSpy
from PyWeChatSpy import spy
from PyWeChatSpy.command import *
from PyWeChatSpy.proto import spy_pb2
import re
import os
import base64

import lipstick
# from lipstick.compare import * 
from lipstick import getface

#PyWeChatSpy
my_response_queue = Queue()
WECHAT_PROFILE = r"F:\WeChat Files\WeChat Files"
TARGET_PATH = r"F:\WeChat Files\WeChat Files\wxid_v3z3560dy0j122\FileStorage\Image\Changed"

#腾讯智能闲聊接口
#api接口的链接
url_preffix='https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
url_pictalk='https://api.ai.qq.com/fcgi-bin/vision/vision_imgtotext'
#因为接口相应参数有要求，一开始是=我是封装在模块里的，但为了大家方便，就整合到了一起
def setParams(array, key, value):
    array[key] = value
#生成接口的sign签名信息方法，接口参数需要 可参考：https://ai.qq.com/doc/auth.shtml 
def genSignString(parser):
    uri_str = ''
    for key in sorted(parser.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, parse.quote(str(parser[key]), safe=''))
    sign_str = uri_str + 'app_key=' + parser['app_key']

    hash_md5 = hashlib.md5(sign_str.encode('utf-8'))
    return hash_md5.hexdigest().upper()
class AiPlat(object):
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.data = {}
        self.url_data = ''
    #调用接口并返回内容
    def invoke(self, params):
        self.url_data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(self.url, self.url_data)
        try:
            rsp = urllib.request.urlopen(req)
            str_rsp = rsp.read().decode('utf-8')
            dict_rsp = json.loads(str_rsp)
            print(dict_rsp)
            return dict_rsp
        except Exception as e:
            print(e)
            return {'ret': -1}
        #此方法生成为api接口准备串接所需的请求参数
    def Messagela(self,question):
        self.url = url_preffix
        setParams(self.data, 'app_id', self.app_id)#应用标识
        setParams(self.data, 'app_key', self.app_key)   
        setParams(self.data, 'time_stamp', int(time.time()))#时间戳
        setParams(self.data, 'nonce_str', int(time.time()))#随机字符串
        setParams(self.data, 'question', question)#聊天内容
        setParams(self.data, 'session', '135248')#session
        sign_str = genSignString(self.data)
        setParams(self.data, 'sign', sign_str)#签名
        return self.invoke(self.data)

    def Pictalk(self,image):
        self.url = url_pictalk
        setParams(self.data, 'app_id', self.app_id)#应用标识
        setParams(self.data, 'app_key', self.app_key)   
        setParams(self.data, 'time_stamp', int(time.time()))#时间戳
        setParams(self.data, 'nonce_str', int(time.time()))#随机字符串
        setParams(self.data, 'image', image)
        setParams(self.data, 'session_id', '135248')#session
        sign_str = genSignString(self.data)
        setParams(self.data, 'sign', sign_str)#签名
        return self.invoke(self.data)    

"""至此上面的部分就是通过腾讯AL获取聊天恢复内容,有些麻烦，之前是封装起来的，这里写在一起，方便你们看一下"""
#appid:2138952940
#APPKEY:BmpKFOHjDXW89ReW
#这是我自己申请的，大家可以随意使用，也可自行去ai.qq.com注册
def getmessage(messageall):
        try:
            Message=AiPlat('2166022015', 'dbcZ6he2OKDyUoCp')
            response=Message.Messagela(messageall)
            return response['data']['answer']           
        except Exception as ex :
            print(ex)
            print("你是不是有什么库没安装啊")
#@itchat.msg_register(itchat.content.TEXT)#微信聊天信息监听存放在msg[]里，当然也监听map picture,等内容，可自行了解itchat.
def tencent_reply(msg):
    # 设置一个默认回复，在出现问题仍能正常回复信息
    #defaultReply = '我不想回答' + msg['Text']
    defaultReply = '我只看得懂中文哦。。'
    #reply = getmessage(msg['Text'])
    reply = getmessage(msg)
    # a or b 表示，如有a有内容，那么返回a，否则返回b
    return reply or defaultReply

def getpictalk(messageall):
        try:
            Message=AiPlat('2166022015', 'dbcZ6he2OKDyUoCp')
            response=Message.Pictalk(messageall)
            return response['data']['text']           
        except Exception as ex :
            print(ex)
            print("你是不是有什么库没安装啊")


def tencent_pictalk(piclink64):
    defaultReply = '唔，没能看懂这个图'
    reply = getpictalk(piclink64)
    return reply or defaultReply

#因为网页版被封itchat无法使用
#主程序
# 使用热启动，不需要多次扫码
'''如启动失败，可将hotReload=True删掉，这是热启动，再次启动时无需在次扫码，具体情况自行考虑'''
#itchat.auto_login()#hotReload=True
#itchat.run()

#wx图片处理，异或需要手动算
def imageDecode(dat_dir,target_path):
    dat_file_name = os.path.basename(dat_dir)
    dat_file_name = dat_file_name.split('.')[0]
    dat_read = open(dat_dir, "rb")
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    out=target_path+"\\"+dat_file_name+".png"
    png_write = open(out, "wb")
    for now in dat_read:
        for nowByte in now:
            newByte = nowByte ^ 0xE6
            png_write.write(bytes([newByte]))
    dat_read.close()
    png_write.close()
    return out

#WechatAPI调用
def my_parser():
    while True:
        data = my_response_queue.get()
        if data.type == CHAT_MESSAGE:  # 判断是微信消息数据
            chat_message = spy_pb2.ChatMessage()
            chat_message.ParseFromString(data.bytes)
            for message in chat_message.message:  # 遍历微信消息
                _type = message.type  # 1文本3图片43视频49Xml37好友请求10000系统消息...自行探索
                _from = message.wxidFrom.str  # 消息发送方
                _to = message.wxidTo.str  # 消息接收方
                content = message.content.str  # 消息内容
                print(_type, _from, _to, content)
                if _from.endswith("@chatroom"):  # 群聊消息
                    _from_group_member = message.content.str.split(':\n', 1)[0]  # 群内发言人
                    content = message.content.str.split(':\n', 1)[-1]  # 群聊消息内容

                if _type == 1: #&&:
                    spy.send_text(_from, tencent_reply(content))
                elif _type == 47: #表情
                    spy.send_text(_from, "检测到表情，功能正在修复 = =")
                    # if random.randint(0,1) == 0:
                    #     image_path = f"meme/{random.randint(1, 13)}.gif"
                    # else:
                    #     image_path = f"meme/{random.randint(1, 2)}.jpg"
                    # spy.send_file(_from, image_path)  # 发送图片
                elif _type == 3:  # 图片消息
                    file_path = message.file
                    file_path = os.path.join(WECHAT_PROFILE, file_path)
                    print(file_path)
                    time.sleep(1)
                    with open(imageDecode(file_path,TARGET_PATH), "rb") as rf:  # 读取图片
                        base64_data = base64.b64encode(rf.read())  # 转化为base64
                        ImageBase64 = base64_data.decode()
                    temppictalk = tencent_pictalk(ImageBase64)
                    spy.send_text(_from, temppictalk)
                    if temppictalk != '唔，没能看懂这个图':
                        spy.send_text(_from, tencent_reply(temppictalk))
                    if lipstick.getface.find_faces(imageDecode(file_path,TARGET_PATH)) > 0:
                        spy.send_text(_from, "检测到人像喽，帮你找找色号叭")
                        spy.send_text(_from, lipstick.getface.do_getface(imageDecode(file_path,TARGET_PATH)))

                elif _type == 10000:  # 判断是微信拍一拍系统提示
                    # 因为微信系统消息很多 因此需要用正则匹配消息内容进一步过滤拍一拍提示
                    #m = re.search('".*" 拍了拍我发现是rigidbody', content)
                    m = re.search('".*" 拍了拍我发现是智障机器人', content)
                    if m:  # 搜索到了匹配的字符串 判断为拍一拍
                        image_path = f"images/{random.randint(1, 7)}.jpg"  # 随机选一张回复用的图片
                        spy.send_file(_from, image_path)  # 发送图片                    
                elif _type == 43:  # 视频消息
                    spy.send_text(_from, "检测到视频消息，相关功能正在完善")
                # elif _type == 49:  # XML报文消息
                #     print(_from, _to, message.file)
                #     xml = etree.XML(content)
                #     xml_type = xml.xpath("/msg/appmsg/type/text()")[0]
                #     if xml_type == "5":
                #         xml_title = xml.xpath("/msg/appmsg/title/text()")[0]
                #         print(xml_title)
                #         if xml_title == "邀请你加入群聊":
                #             url = xml.xpath("/msg/appmsg/url/text()")[0]
                #             print(url)
                #             time.sleep(1)
                #             spy.get_group_enter_url(_from, url)                
                # elif _type == 37:  # 好友申请
                #     print("新的好友申请")
                #     obj = etree.XML(message.content.str)
                #     encryptusername, ticket = obj.xpath("/msg/@encryptusername")[0], obj.xpath("/msg/@ticket")[0]
                #     spy.accept_new_contact(encryptusername, ticket)  # 接收好友请求
                else:
                    print(data)
                    print(_type)
                


if __name__ == '__main__':
    spy = WeChatSpy(response_queue=my_response_queue)
    spy.run(r"F:\WeChat\WeChat.exe")
    my_parser()