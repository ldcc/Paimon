from nonebot import on_command
from .get_character import get_character, get_mz
from nonebot.adapters.cqhttp import Event, Bot, Message

chara = on_command('角色资料', aliases={'角色查询'})


@chara.handle()
async def _(bot: Bot, event: Event):
    name = str(event.get_message()).strip()
    re = get_character(name)
    re += await get_mz(name)
    await chara.finish(message=Message(re))
