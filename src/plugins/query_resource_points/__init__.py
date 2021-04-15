from nonebot import on_keyword
from nonebot.rule import to_me
from .query_resource_points import get_resource_map_mes, get_resource_list_mes, up_label_and_point_list

respot = on_keyword({'在哪', '在哪里', '哪有', '哪里有'}, rule=to_me())


@respot.handle()
async def respot_handle(bot, event):
    res = event.get_message().extract_plain_text().strip()
    if res == "":
        return

    msg = get_resource_map_mes(res)
    await respot.finish(msg)

# @sv.on_fullmatch('原神资源列表')
# async def inquire_resource_list(bot, event):
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
#     await bot.send_group_forward_msg(group_id=event['group_id'], messages=mes_list)
#
#
# @sv.on_fullmatch('刷新原神资源列表')
# async def inquire_resource_list(bot, event):
#     up_label_and_point_list()
#     await bot.send(event, '刷新成功', at_sender=True)
