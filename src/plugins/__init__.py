import os

from nonebot import get_driver
from nonebot.adapters.cqhttp.bot import Bot

driver = get_driver()
default_switch_map = {'色图': False, '防撤回': True, '戳一戳': True, '偷闪照': True, 'r18': False, 'proxy': False}
group_switcher = dict()
bot_info = dict()
ls = []
apikeys = []


async def append_ls(v):
    if v == '':
        return
    global ls
    ls.append(v)


async def reset_apikeys_default():
    global apikeys
    apikeys = driver.config.apikeys


@driver.on_bot_connect
async def _(bot: Bot):
    global bot_info, ls, apikeys
    bot_info = await bot.get_login_info()
    ls = os.listdir(r'./src/data/store')
    apikeys = driver.config.apikeys
    default_switch_map['proxy'] = driver.config.setu_proxy


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


async def set_switch(group_id, key, status) -> str:
    global group_switcher
    status_ret = '启动' if status else '关闭'
    try:
        switch_map = group_switcher[group_id]
    except:
        switch_map = default_switch_map.copy()
    try:
        if switch_map[key] == status:
            return f'{key}已经{status_ret}'
    except:
        return f'没有{key}这种功能'
    switch_map[key] = status
    group_switcher[group_id] = switch_map
    return f'{key}{status_ret}成功'


def check_switch(group_id, key) -> dict:
    global group_switcher
    try:
        switch_map = group_switcher[group_id]
    except:
        switch_map = default_switch_map.copy()
        group_switcher[group_id] = switch_map
    try:
        if switch_map[key]:
            return switch_map
    except:
        return dict()
    return dict()
