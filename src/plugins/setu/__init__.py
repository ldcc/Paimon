import base64
import os.path

from PicImageSearch import SauceNAO, TraceMoe, Ascii2D, Google, Network
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, GroupMessageEvent, ActionFailed, Message
from nonebot.typing import T_State

from .get_pic import setu_pic, anti_harmonious
from .parse import format_data
import src.plugins as cfg

search = on_command('搜图', aliases={'搜番', '搜名场景', '识图'})
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


# 搜图
@search.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    pic = event.get_message()
    if pic:
        state['pic'] = pic
    state['cmd'] = state["_prefix"]["raw_command"]


@search.got('pic', prompt='请发送要搜索的图片')
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    engine = None
    apikey = ""
    re = MessageSegment.text("无法识别图片")
    if state['cmd'] == '搜图':
        engine = Ascii2D
    elif state['cmd'] == '搜番':
        engine = TraceMoe
    elif state['cmd'] == '搜名场景':
        engine = SauceNAO
        apikey = cfg.snao_apikey
    elif state['cmd'] == '识图':
        engine = Google
    pic = Message(state['pic']).pop()
    if pic.type == 'image':
        url = pic.data['url']
        async with Network() as client:
            session = engine(api_key=apikey, client=client)
            re = format_data(await session.search(url))
    await search.finish(re)
