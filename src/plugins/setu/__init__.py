from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Message, Event

from .getPic import ghs_pic3

setu = on_command('ghs', aliases={'无内鬼', '涩图', '色图', '瑟图'})
withdraw = on_command('撤回')


@setu.handle()
async def _(bot: Bot, event: Event):
    key = str(event.get_message()).strip()
    pic = await ghs_pic3(key)
    await setu.finish(message=Message(pic))
