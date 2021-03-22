from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.typing import T_State

fuben = on_command("fuben", rule=to_me())


@fuben.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["name"] = args


@fuben.got("name", prompt="你想查询哪个城市的天气呢？")
async def got(bot: Bot, state: T_State):
    name = state["name"]
