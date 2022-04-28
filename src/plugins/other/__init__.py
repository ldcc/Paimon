from random import choice

from nonebot import on_notice, on_message
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, FriendRecallNoticeEvent, PokeNotifyEvent, GroupRecallNoticeEvent
from nonebot.rule import to_me

import src.plugins as cfg

poke = on_notice(rule=to_me())
recall = on_notice(priority=10)
flashimg = on_message(priority=10)


# 群聊撤回
@recall.handle()
async def _(bot: Bot, event: GroupRecallNoticeEvent):
    switch_map = cfg.check_switcher(event.group_id, '防撤回')
    if len(switch_map) == 0:
        return
    mid = event.message_id
    msg = await bot.get_msg(message_id=mid)
    if event.user_id != event.self_id and ',type=flash' not in msg['message']:
        re = '刚刚说了:\n' + msg['message']
        await recall.finish(message=Message(re), at_sender=True)


# 私聊撤回
@recall.handle()
async def _(bot: Bot, event: FriendRecallNoticeEvent):
    mid = event.message_id
    msg = await bot.get_msg(message_id=mid)
    if event.user_id != event.self_id and 'type=flash,' not in msg['message']:
        re = '刚刚说了:' + msg['message']
        await recall.finish(message=Message(re))


# 戳一戳
@poke.handle()
async def _(bot: Bot, event: PokeNotifyEvent) -> None:
    switch_map = cfg.check_switcher(event.group_id, '戳一戳')
    if len(switch_map) == 0:
        return
    msg = choice([
        '你再戳！', '？再戳试试？', '别戳了别戳了再戳就坏了555', '我爪巴爪巴，球球别再戳了', '你戳你🐎呢？！',
        '那...那里...那里不能戳...绝对...', '欸很烦欸！', '?', '差不多得了😅', '这好吗？这不好！', '我希望你耗子尾汁'
    ])
    await poke.finish(msg, at_sender=True)


# 闪照
@flashimg.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    switch_map = cfg.check_switcher(event.group_id, '偷闪照')
    if len(switch_map) == 0:
        return
    msg = str(event.get_message())
    if ',type=flash' in msg:
        msg = msg.replace(',type=flash', '')
        await flashimg.finish(message=Message('不要发闪照，好东西就要大家一起分享。' + msg), at_sender=True)
