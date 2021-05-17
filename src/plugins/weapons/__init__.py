from nonebot import on_command
from .get_data import get_weapon
from nonebot.adapters.cqhttp import Event, Bot, Message

wea = on_command('武器资料', aliases={'武器查询'})


@wea.handle()
async def _(bot: Bot, event: Event):
    name = event.get_message().extract_plain_text().strip()
    re = await get_weapon(name)
    await wea.finish(Message(re))
