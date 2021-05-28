import base64
import os
from pathlib import Path

from nonebot import on_command, on_message
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp import GroupMessageEvent, Message, Event
from nonebot.rule import to_me
from nonebot.typing import T_State
import src.plugins as cfg

keys = on_command('圣经')
save = on_command('记录', rule=to_me())
load = on_message(priority=10)


@keys.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    mes_list = cfg.format_group_message(cfg.ls)
    await bot.send_group_forward_msg(group_id=event.group_id, messages=Message(mes_list))


@save.handle()
async def _(bot: Bot, event: Event, state: T_State):
    pair = str(event.get_message()).strip().split(' ', 1)
    if len(pair) < 2:
        pair = str(event.get_message()).strip().split('\n', 1)
    if len(pair) < 1:
        await save.finish(message=Message('错误的格式'))
    state['instruct'] = pair[0].strip()
    if len(pair) < 2:
        return
    state['content'] = pair[1].strip()


@save.got('content', prompt='请发送要记录的数据')
async def _(bot: Bot, event: Event, state: T_State):
    instruct = state['instruct']
    content = state['content']
    file = os.path.join(r'./src/data/store', instruct)
    try:
        with open(file, 'w', encoding='utf-8') as f:
            data = base64.b64encode(content.encode()).decode()
            f.write(data)
    except:
        return
    await save.send(message=Message('👌'))
    await cfg.append_ls(instruct)


@load.handle()
async def _(bot: Bot, event: Event):
    key = str(event.get_message()).strip()
    for f in cfg.ls:
        if f in key:
            file = os.path.join(r'./src/data/store', f)
            if Path(file).is_file():
                with open(file, 'r', encoding='utf-8') as f:
                    data = base64.b64decode(f.read()).decode()
                await save.finish(message=Message(data))
