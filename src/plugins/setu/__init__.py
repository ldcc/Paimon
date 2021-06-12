import base64
import os.path

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageSegment, GroupMessageEvent, ActionFailed

from .get_pic import setu_pic, anti_harmonious
import src.plugins as cfg

setu = on_command('setu', aliases={'无内鬼', '涩图', '色图', '瑟图'})
RETRY = 3


# 涩图
@setu.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    switch_map = cfg.check_switcher(event.group_id, '色图')
    if len(switch_map) == 0:
        return
    key = str(event.get_message()).strip()
    mseg = await setu_pic(key, switch_map['r18'], switch_map['proxy'])
    try:
        await setu.send(message=mseg)
    except ActionFailed:
        pic = mseg.data.get('file')
        if pic:
            retry = 0
            b64pic = base64.b64decode(pic.removeprefix('base64://'))
            while retry < RETRY:
                b64pic = anti_harmonious(b64pic)
                pic = f'base64://{base64.b64encode(b64pic).decode()}'
                try:
                    await setu.send(message=MessageSegment.image(pic))
                    return
                except ActionFailed:
                    retry += 1
            with open(os.path.join(cfg.IMAGE_PATH, 'setu.png'), 'rb') as pic:
                pic = f'base64://{base64.b64encode(pic.read()).decode()}'
                await setu.send(message=MessageSegment.image(pic))
    finally:
        await setu.finish()
