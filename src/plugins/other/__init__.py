from random import choice

from nonebot import on_notice, on_message
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, FriendRecallNoticeEvent, PokeNotifyEvent, \
    GroupRecallNoticeEvent
from nonebot.rule import to_me

import src.plugins as cfg

poke = on_notice(rule=to_me())
recall = on_notice(priority=10)
flashimg = on_message(priority=10)


# 群聊撤回
@recall.handle()
async def _(bot: Bot, event: GroupRecallNoticeEvent):
    msg = await bot.get_msg(message_id=event.message_id)
    if event.user_id == event.self_id or ',type=flash' in msg['message']:
        return
    msg_list = [
        MessageSegment.node_custom(cfg.bot_info['user_id'], cfg.bot_info['nickname'], f'群{event.group_id}检测到撤回消息'),
        MessageSegment.node(event.message_id)]
    await bot.send_group_forward_msg(group_id=cfg.center_group_id, messages=Message(msg_list))

    switch_map = cfg.check_switcher(event.group_id, '防撤回')
    if len(switch_map) != 0:
        await recall.finish(message=Message('刚刚说了:\n' + msg['message']), at_sender=True)


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
        '你再戳！', '？再戳试试？', '别戳了再戳就坏了555', '球球别再戳了', '你戳你🐎呢？！',
        '那里...不能戳...', '欸很烦欸！', '?', '差不多得了😅', '这好吗？这不好！', '我希望你耗子尾汁'
    ])
    await poke.finish(msg, at_sender=True)


# 偷闪照
@flashimg.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = str(event.get_message())
    if ',type=flash' not in msg:
        return
    msg = msg.replace(',type=flash', '')
    msg_list = cfg.format_group_message({msg: f'群{event.group_id}检测到闪照'}, event.sender.user_id, event.sender.nickname)
    await bot.send_group_forward_msg(group_id=cfg.center_group_id, messages=Message(msg_list))

    switch_map = cfg.check_switcher(event.group_id, '偷闪照')
    if len(switch_map) != 0:
        await flashimg.finish(message=Message('不要发闪照，好东西就要大家一起分享。' + msg), at_sender=True)
