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


##########################################
@on_command('周本', aliases=('龙狼', '龙狼公子'))
async def zhouben(session: CommandSession):
    await session.send('[CQ:image,file=file:///E:/program/PaimonBot/awesome/plugins/fuben/zb.png]')


@on_command('武器', aliases=('武器本', '武器材料', '武器突破', '今日武器'))
async def wuqi(session: CommandSession):
    if datetime.now().isoweekday() == 1 or datetime.now().isoweekday() == 4:
        await session.send('[CQ:image,file=file:///E:/program/PaimonBot/awesome/plugins/fuben/wq14.png]')
    elif datetime.now().isoweekday() == 2 or datetime.now().isoweekday() == 5:
        await session.send('[CQ:image,file=file:///E:/program/PaimonBot/awesome/plugins/fuben/wq25.png]')
    elif datetime.now().isoweekday() == 3 or datetime.now().isoweekday() == 6:
        await session.send('[CQ:image,file=file:///E:/program/PaimonBot/awesome/plugins/fuben/wq36.png]')
    else:
        await session.send("今天的副本想打什么打什么哦！[CQ:image,file=file:///E:program/PaimonBot/face/face3]")


@on_command('天赋', aliases=('天赋本', '天赋材料', '今日天赋'))
async def tianfu(session: CommandSession):
    if datetime.now().isoweekday() == 1 or datetime.now().isoweekday() == 4:
        await session.send(
            '[CQ:image,file=file:///E:/program/PaimonBot/awesome/plugins/fuben/tf14.png]')
    elif datetime.now().isoweekday() == 2 or datetime.now().isoweekday() == 5:
        await session.send(
            '[CQ:image,file=file:///E:/program/PaimonBot/awesome/plugins/fuben/tf25.png]')
    elif datetime.now().isoweekday() == 3 or datetime.now().isoweekday() == 6:
        await session.send(
            '[CQ:image,file=file:///E:/program/PaimonBot/awesome/plugins/fuben/tf36.png]')
    else:
        await session.send("今天的副本想打什么打什么哦![CQ:image,file=file:///E:program/PaimonBot/face/face3]")
