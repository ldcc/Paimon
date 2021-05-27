from nonebot import on_command, on_startswith
from nonebot.rule import to_me
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp import GroupMessageEvent, Message, Event
from .query import get_resource_map_mes, get_resource_list_mes, up_label_and_point_list
import src.plugins as cfg

respot = on_startswith('哪有')
reslist = on_command('素材资源列表', aliases={'素材列表', "资源列表", "资源素材列表"})
resrefre = on_command('刷新素材资源列表', rule=to_me())


@respot.handle()
async def _(bot: Bot, event: Event):
    res = event.get_message().extract_plain_text().strip()
    if res == "":
        return

    msg = get_resource_map_mes(res[2:])
    await respot.finish(Message(msg))


@reslist.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    resources = get_resource_list_mes().split('\n')
    mes_list = cfg.format_group_message(resources)
    await bot.send_group_forward_msg(group_id=event.group_id, messages=Message(mes_list))


@resrefre.handle()
async def _(bot: Bot, event: Event):
    up_label_and_point_list()
    await resrefre.finish('刷新成功')
