from random import choice

from nonebot import on_notice, on_message, on_command
from nonebot.adapters.cqhttp import Bot, Message, Event, \
    GroupRecallNoticeEvent, FriendRecallNoticeEvent, PokeNotifyEvent, MessageEvent
from nonebot.rule import to_me
from nonebot.typing import T_State

from .getPic import ghs_pic3

# permission=SUPERUSER
switch_on = on_command('功能开启', aliases={'功能启动', '启动功能', '开启功能'})
switch_off = on_command('功能关闭', aliases={'关闭功能'})
setu = on_command('setu', aliases={'无内鬼', '涩图', '色图', '瑟图'})
recall = on_notice()
poke = on_notice(rule=to_me())
flashimg = on_message()

switch_map = {'色图': False, '防撤回': True, '戳一戳': True, '偷闪照': True, 'r18': False}


@switch_on.handle()
async def _(bot: Bot, event: Event, state: T_State):
    key = str(event.get_message()).strip()
    if key:
        state["switch_on"] = key


@switch_on.got("switch_on", prompt='请输入要开启的功能：\n1.色图\n2.防撤回\n3.戳一戳\n4.偷闪照\n5.r18')
async def _(bot: Bot, event: Event, state: T_State):
    key = state["switch_on"]
    global switch_map
    try:
        if switch_map[key]:
            await switch_on.finish(f'{key}已经开启')
    except Exception as err:
        if str(err) != "":
            await switch_on.finish(f'派蒙没有{key}这种功能')
        else:
            return
    switch_map[key] = True
    await switch_on.finish(f'{key}启动成功')


@switch_off.handle()
async def _(bot: Bot, event: Event, state: T_State):
    key = str(event.get_message()).strip()
    if key:
        state["switch_off"] = key


@switch_off.got("switch_off", prompt='请输入要关闭的功能：\n1.色图\n2.防撤回\n3.戳一戳\n4.偷闪照\n5.r18')
async def _(bot: Bot, event: Event, state: T_State):
    key = state["switch_off"]
    global switch_map
    try:
        if not switch_map[key]:
            await switch_off.finish(f'{key}已经关闭')
    except Exception as err:
        if str(err) != "":
            await switch_off.finish(f'派蒙没有{key}这种功能')
        else:
            return
    switch_map[key] = False
    await switch_off.finish(f'{key}关闭成功')


# 涩图
@setu.handle()
async def _(bot: Bot, event: Event):
    global switch_map
    if not switch_map['色图']:
        await setu.finish(message=Message('该功能未开启'))
    key = str(event.get_message()).strip()
    pic = await ghs_pic3(key, switch_map['r18'])
    try:
        await setu.send(message=Message(pic))
    except Exception as err:
        print(err)
        await setu.finish(message=Message('消息被风控，派蒙不背锅'))


# 群聊撤回
@recall.handle()
async def _(bot: Bot, event: GroupRecallNoticeEvent):
    global switch_map
    if not switch_map['防撤回']:
        await recall.finish(message=Message('该功能未开启'))
    mid = event.message_id
    meg = await bot.get_msg(message_id=mid)
    if event.user_id != event.self_id and ',type=flash' not in meg['raw_message']:
        # if ',type=flash' in meg['raw_message']:
        #     meg['raw_message'] = meg['raw_message'].replace(',type=flash', '')
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
    global switch_map
    if not switch_map['戳一戳']:
        await poke.finish(message=Message('该功能未开启'))
    msg = choice([
        "你再戳！", "？再戳试试？", "别戳了别戳了再戳就坏了555", "我爪巴爪巴，球球别再戳了", "你戳你🐎呢？！",
        "那...那里...那里不能戳...绝对...", "(。´・ω・)ん?", "有事恁叫我，别天天一个劲戳戳戳！", "欸很烦欸！",
        "?", "差不多得了😅", "欺负派蒙这好吗？", "我希望你耗子尾汁"
    ])
    await poke.finish(msg, at_sender=True)


# 闪照
@flashimg.handle()
async def _(bot: Bot, event: MessageEvent):
    global switch_map
    if not switch_map['偷闪照']:
        await flashimg.finish(message=Message('该功能未开启'))
    msg = str(event.get_message())
    if ',type=flash' in msg:
        msg = msg.replace(',type=flash', '')
        await flashimg.finish(message=Message("不要发闪照，好东西就要分享。" + msg), at_sender=True)
