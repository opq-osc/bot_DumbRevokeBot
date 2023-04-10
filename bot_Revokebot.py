# encoding=utf-8
import jieba
import base64
from botoy import GroupMsg,Action,S
from botoy import decorators as deco
from botoy.collection import MsgTypes
from botoy.decorators import these_msgtypes,from_these_groups
from botoy.contrib import plugin_receiver
def check_sensetive(text):
    with open("sensetive.txt","r") as sensetive_words:
        sensetive_list = []
        for line in sensetive_words.readlines():
            sensetive_list.append(line.replace("\n", ""))
    pre_seg_list = jieba.cut_for_search(text)
    seg_list = ",".join(pre_seg_list)
    print(seg_list)
    if any(element in seg_list for element in sensetive_list):  # 搜索引擎模式
        return True
    else:
        return False
@plugin_receiver.group
@from_these_groups("*********")           #这里为你需要监听的群聊
@deco.ignore_botself
@these_msgtypes(MsgTypes.TextMsg,               #接收信息类型
                MsgTypes.AtMsg,
                MsgTypes.PicMsg,
                MsgTypes.ReplyMsg,
                MsgTypes.ReplyMsgA
                )
def main(ctx=GroupMsg):
    msg = ctx.Content.strip()
    if check_sensetive(msg) == True:
        print("sensetive msg discover")
        Action(ctx.CurrentQQ).revokeGroupMsg(
            group=ctx.FromGroupId,
            msgSeq=ctx.MsgSeq,
            msgRandom=ctx.MsgRandom,
            )
        Action(ctx.CurrentQQ).shutUserUp(
            groupID=ctx.FromGroupId,
            userid=ctx.FromUserId,
            ShutTime=2                              #这里是你需要禁言的时长，单位为分钟
            )
        S.bind(ctx).text("根据结果，此发言不合规，已自动撤回。")
        S.bind(ctx).text("Base64后的原文： " + base64.b64encode(msg.encode('utf-8')).decode(),True)
    else:
        print("pass")