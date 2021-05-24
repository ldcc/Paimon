from nonebot import on_command, get_driver
from nonebot.adapters.cqhttp import Bot, Message, Event

from .getPic import ghs_pic3

ghs = on_command('ghs', aliases={'无内鬼', '涩图', '色图', '瑟图'})


@ghs.handle()
async def _(bot: Bot, event: Event):
    setu_on = get_driver().config.setu_on
    if not setu_on:
        return

    key = str(event.get_message()).strip()
    pic = await ghs_pic3(key)
    try:
        await ghs.send(message=Message(pic))
    except Exception as err:
        print(err)
        await ghs.send(message=Message('消息被风控，派蒙不背锅'))
