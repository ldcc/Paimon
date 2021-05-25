import base64
import os
from pathlib import Path

from nonebot import on_command, on_message
from nonebot.adapters.cqhttp import Bot, Event, Message
from nonebot.rule import to_me

save = on_command('记录', rule=to_me())
load = on_message(rule=to_me())


@save.handle()
async def _(bot: Bot, event: Event):
    pair = str(event.get_message()).strip().split(' ', 1)
    if len(pair) < 2:
        pair = str(event.get_message()).strip().split('\n', 1)
    if len(pair) < 2:
        await save.finish(message=Message('错误的格式'))
    file = os.path.join(r'./src/data/store', pair[0])
    with open(file, 'w', encoding='utf-8') as f:
        data = base64.b64encode(pair[1].encode()).decode()
        f.write(data)
    await save.finish(message=Message('👌'))


@load.handle()
async def _(bot: Bot, event: Event):
    key = str(event.get_message()).strip()
    file = os.path.join(r'./src/data/store', key)
    if Path(file).is_file():
        with open(file, 'r', encoding='utf-8') as f:
            data = base64.b64decode(f.read()).decode()
        await save.finish(message=Message(data))
