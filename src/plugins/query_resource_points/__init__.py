from nonebot import on_command, on_endswith
from nonebot.rule import to_me
# from .query_resource_points import get_resource_map_mes#, get_resource_list_mes, up_label_and_point_list

respot = on_endswith('在哪')
reslist = on_command('素材资源列表', rule=to_me())
resrefre = on_command('刷新素材资源列表', rule=to_me())


# @respot.handle()
# async def _(bot, event):
#     res = event.get_message().extract_plain_text().strip()
#     if res == "":
#         return
#
#     msg = get_resource_map_mes(res[:-2])
#     print(msg)
#     await respot.finish(msg)


# @reslist.handle()
# async def _(bot, event):
#     # 长条消息经常发送失败，所以只能这样了
#     mes_list = []
#     txt_list = get_resource_list_mes().split("\n")
#     for txt in txt_list:
#         data = {
#             "type": "node",
#             "data": {
#                 "name": "色图机器人",
#                 "uin": "2854196310",
#                 "content": txt
#             }
#         }
#         mes_list.append(data)
#     # await bot.send(event, get_resource_list_mes(), at_sender=True)
#     await reslist.finish(mes_list)
#
#
# @resrefre.handle()
# async def _(bot, event):
#     up_label_and_point_list()
#     await resrefre.finish('刷新成功')
