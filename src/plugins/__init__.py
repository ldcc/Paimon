import os

from nonebot import get_driver
from nonebot.adapters.cqhttp.bot import Bot

driver = get_driver()
bot_info = dict()
ls = os.listdir(r'./src/data/store')


async def append_ls(v):
    if v == '':
        return
    global ls
    ls.append(v)


@driver.on_bot_connect
async def _(bot: Bot):
    global bot_info
    bot_info = await bot.get_login_info()


def format_group_message(msgs):
    nodes = []
    for msg in msgs:
        data = {
            'type': 'node',
            'data': {
                'name': bot_info['nickname'],
                'uin': str(bot_info['user_id']),
                'content': msg
            }
        }
        nodes.append(data)
    return nodes
