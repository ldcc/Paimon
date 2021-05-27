import base64
import os
from pathlib import Path

from nonebot import on_command, on_message
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp import GroupMessageEvent, Message, Event
from nonebot.rule import to_me
import src.plugins as cfg

keys = on_command('圣经')
save = on_command('记录', rule=to_me())
load = on_message()


@keys.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    mes_list = cfg.format_group_message(cfg.ls)
    await bot.send_group_forward_msg(group_id=event.group_id, messages=Message(mes_list))


@save.handle()
async def _(bot: Bot, event: Event):
    pair = str(event.get_message()).strip().split(' ', 1)
    if len(pair) < 2:
        pair = str(event.get_message()).strip().split('\n', 1)
    if len(pair) < 2:
        await save.finish(message=Message('错误的格式'))
    pair[0] = pair[0].strip()
    pair[1] = pair[1].strip()
    file = os.path.join(r'./src/data/store', pair[0])
    with open(file, 'w', encoding='utf-8') as f:
        data = base64.b64encode(pair[1].encode()).decode()
        f.write(data)
    try:
        await save.send(message=Message('👌'))
    except:
        return
    await cfg.append_ls(pair[0])


# @save.got('d', prompt='')
# async def _(bot: Bot, event: Event):
#     pass


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
