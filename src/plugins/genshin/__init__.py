from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, Message, Event
from .query import get_resource_map_mes, get_resource_list_mes, up_label_and_point_list, up_map
import src.plugins as cfg

res_pot = on_command('哪有')
res_list = on_command('素材资源列表')
res_refre = on_command('刷新素材资源列表', rule=to_me())
map_refre = on_command('更新原神地图', rule=to_me())


@res_pot.handle()
async def _(bot: Bot, event: Event):
    res = event.get_message().extract_plain_text().strip()
    if res == '':
        return

    msg = get_resource_map_mes(res)
    await res_pot.finish(message=Message(msg))


@res_list.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    resources = dict.fromkeys(get_resource_list_mes().split('\n'))
    mes_list = cfg.format_group_message(resources)
    await bot.send_group_forward_msg(group_id=event.group_id, messages=Message(mes_list))


@res_refre.handle()
async def _(bot: Bot, event: Event):
    up_label_and_point_list()
    await res_refre.finish('刷新成功')


@map_refre.handle()
async def _(bot: Bot, event: Event):
    up_map(True)
    await map_refre.finish('更新成功')
