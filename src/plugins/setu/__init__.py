from nonebot import on_command
from nonebot.adapters.cqhttp.exception import NetworkError
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.message import Message
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from .get_pic import setu_pic
import src.plugins as cfg

setu = on_command('setu', aliases={'无内鬼', '涩图', '色图', '瑟图'})


# 涩图
@setu.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    switch_map = cfg.check_switcher(event.group_id, '色图')
    if len(switch_map) == 0:
        return
    key = str(event.get_message()).strip()
    pic = await setu_pic(key, switch_map['r18'], switch_map['proxy'])
    try:
        await setu.send(message=Message(pic))
    except NetworkError:
        pass
    except Exception as err:
        print(err)
        await setu.send(message=Message('消息被风控，我可不背锅'))
