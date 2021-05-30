from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.message import Message
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.typing import T_State

import src.plugins as cfg

auths = 'allow - 允许管理员权限\ndrop - 撤销管理员权限\n'
set_auth = on_command('管理员设置', rule=to_me(), permission=SUPERUSER)

features = '- 色图\n- 防撤回\n- 戳一戳\n- 偷闪照\n'
switch_on = on_command('功能开启', aliases={'功能启动', '启动功能', '开启功能'}, rule=to_me())
switch_off = on_command('功能关闭', aliases={'关闭功能'})


@set_auth.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg == '':
        await set_auth.finish(message=f'格式错误，参考输出\n{auths}')
    pair = msg.split(' ', 1)
    state['instruct'] = pair[0].strip()
    if len(pair) < 2:
        return
    state['uin'] = pair[1].strip()


@set_auth.got('uin', prompt='请输入 uin')
async def _(bot: Bot, state: T_State):
    action = state['instruct']
    uin = state['uin']
    ret = await cfg.set_manager(uin, action == 'allow')
    await set_auth.finish(message=('设置' + '成功' if ret else '失败'))


@switch_on.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if event.user_id in cfg.managers:
        key = str(event.get_message()).strip()
        if key:
            state['switch_on'] = key
    else:
        await switch_on.finish('你没有该权限')


@switch_on.got('switch_on', prompt=f'请输入要开启的功能：\n{features}')
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    key = state['switch_on']
    if key == 'r18' and event.user_id not in cfg.supersuers:
        await switch_on.finish(f'摇了我吧，{cfg.bot_info["nickname"]}不想蹲局子')
    ret = await cfg.set_switch(event.group_id, state['switch_on'], True)
    await switch_on.finish(message=Message(ret))


@switch_off.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    key = str(event.get_message()).strip()
    if key:
        state['switch_off'] = key


@switch_off.got('switch_off', prompt=f'请输入要关闭的功能：\n{features}')
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    ret = await cfg.set_switch(event.group_id, state['switch_off'], False)
    await switch_on.finish(message=Message(ret))
