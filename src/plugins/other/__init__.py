from random import choice

from nonebot import on_notice, on_message
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.message import Message
from nonebot.adapters.cqhttp.event import GroupMessageEvent, \
    FriendRecallNoticeEvent, PokeNotifyEvent, GroupRecallNoticeEvent
from nonebot.rule import to_me

import src.plugins as cfg

poke = on_notice(rule=to_me())
recall = on_notice(priority=10)
flashimg = on_message(priority=10)



# 群聊撤回
@recall.handle()
async def _(bot: Bot, event: GroupRecallNoticeEvent):
    switch_map = cfg.check_switch(event.group_id, '防撤回')
    if len(switch_map) == 0:
        return
    mid = event.message_id
    meg = await bot.get_msg(message_id=mid)
    if event.user_id != event.self_id and ',type=flash' not in meg['raw_message']:
        re = '刚刚说了:\n' + meg['raw_message'] + '\n不要以为派蒙没看见！'
        await recall.finish(message=Message(re), at_sender=True)


# 私聊撤回
@recall.handle()
async def _(bot: Bot, event: FriendRecallNoticeEvent):
    mid = event.message_id
    meg = await bot.get_msg(message_id=mid)
    if event.user_id != event.self_id and 'type=flash,' not in meg['message']:
        re = '刚刚说了:' + meg['message'] + '\n不要以为派蒙没看见！'
        await recall.finish(message=Message(re))


# 戳一戳
@poke.handle()
async def _(bot: Bot, event: PokeNotifyEvent) -> None:
    switch_map = cfg.check_switch(event.group_id, '戳一戳')
    if len(switch_map) == 0:
        return
    msg = choice([
        "你再戳！", "？再戳试试？", "别戳了别戳了再戳就坏了555", "我爪巴爪巴，球球别再戳了", "你戳你🐎呢？！",
        "那...那里...那里不能戳...绝对...", "(。´・ω・)ん?", "有事恁叫我，别天天一个劲戳戳戳！", "欸很烦欸！",
        "?", "差不多得了😅", "这好吗？这不好！", "我希望你耗子尾汁"
    ])
    await poke.finish(msg, at_sender=True)


# 闪照
@flashimg.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    switch_map = cfg.check_switch(event.group_id, '偷闪照')
    if len(switch_map) == 0:
        return
    msg = str(event.get_message())
    if ',type=flash' in msg:
        msg = msg.replace(',type=flash', '')
        await flashimg.finish(message=Message("不要发闪照，好东西就要分享。" + msg), at_sender=True)
