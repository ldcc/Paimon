from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.typing import T_State

import src.plugins as cfg

auths = 'allow - 允许管理员权限\ndenies - 撤销管理员权限'
set_auth = on_command('管理员设置', rule=to_me(), permission=SUPERUSER)

features = '- 防撤回\n- 戳一戳\n- 偷闪照\n- proxy'
switch_on = on_command('功能开启', aliases={'功能启动', '启动功能', '开启功能'})
switch_off = on_command('功能关闭', aliases={'关闭功能'})


@set_auth.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = state["_prefix"]["command_arg"]
    if len(msg) == 0:
        await set_auth.finish(message=f'格式错误，参考输出\n{auths}')
    pair = str(msg).strip().split(' ', 1)
    if str(pair[0]) == "allow":
        state['auth'] = True
    elif str(pair[0]) == "denies":
        state['auth'] = False
    else:
        await set_auth.finish(message=f'格式错误，参考输出\n{auths}')
    if len(pair) > 1:
        state['uin'] = pair[1]


@set_auth.got('uin', prompt='请输入 uin')
async def _(bot: Bot, state: T_State):
    auth = state['auth']
    uin = str(state['uin'])
    ret = await cfg.set_manager(uin, auth)
    await set_auth.finish(message=('设置' + '成功' if ret else '失败'))


@switch_on.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if str(event.user_id) in cfg.managers:
        key = state["_prefix"]["command_arg"]
        if len(key) > 0:
            state['switch_on'] = key[0]
    else:
        await switch_on.finish('你没有该权限')


@switch_on.got('switch_on', prompt=f'请输入要开启的功能：\n{features}')
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    key = str(state['switch_on']).strip()
    if key in '色图r18' and str(event.user_id) not in cfg.supersuers:
        await switch_on.finish(f'摇了我吧，爷8想蹲局子')
    ret = await cfg.set_switcher(event.group_id, key, True)
    await switch_on.finish(message=Message(ret))


@switch_off.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    key = state["_prefix"]["command_arg"]
    if len(key) > 0:
        state['switch_off'] = key[0]


@switch_off.got('switch_off', prompt=f'请输入要关闭的功能：\n{features}')
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    key = str(state['switch_off']).strip()
    ret = await cfg.set_switcher(event.group_id, key, False)
    await switch_on.finish(message=Message(ret))
