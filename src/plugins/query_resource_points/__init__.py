from nonebot import on_command, on_endswith
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Message
from .query import get_resource_map_mes, get_resource_list_mes, up_label_and_point_list

respot = on_endswith('在哪')
reslist = on_command('素材资源列表', rule=to_me())
resrefre = on_command('刷新素材资源列表', rule=to_me())


@respot.handle()
async def _(bot, event):
    res = event.get_message().strip()
    if res == "":
        return

    msg = get_resource_map_mes(res[:-2])
    await respot.finish(Message(message=msg))


@reslist.handle()
async def _(bot, event):
    mes_list = []
    txt_list = get_resource_list_mes().split("\n")
    for txt in txt_list:
        data = {
            "type": "node",
            "data": {
                "name": "派蒙",
                "uin": "2854196310",
                "content": txt
            }
        }
        mes_list.append(data)
    await reslist.finish(str(mes_list))


@resrefre.handle()
async def _(bot, event):
    up_label_and_point_list()
    await resrefre.finish('刷新成功')
