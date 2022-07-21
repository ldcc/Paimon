import json
import os

from nonebot import get_driver
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.bot import Bot

driver = get_driver()
default_switcher_map = {'色图': False, '防撤回': False, '戳一戳': False, '偷闪照': False, 'r18': False, 'proxy': False}
group_switcher = dict()
bot_info = dict()
managers = dict()
supersuers = set()
ls = set()
center_group_id = 0
apikeys = []
snao_apikey = ''

IMAGE_PATH = r'./src/data/images'
STORE_PATH = r'./src/data/store'


@driver.on_bot_connect
async def _(bot: Bot):
    global bot_info, managers, group_switcher, supersuers, ls, center_group_id, apikeys, snao_apikey
    default_switcher_map['proxy'] = driver.config.setu_proxy
    bot_info = await bot.get_login_info()
    managers = await load_manager()
    group_switcher = await load_switcher()
    supersuers = driver.config.superusers
    ls = set(os.listdir(STORE_PATH))
    center_group_id = driver.config.center_group_id
    apikeys = driver.config.apikeys
    snao_apikey = driver.config.snao_apikey


async def stash_ls(v):
    if v == '':
        return
    global ls
    ls.add(v)


async def drop_ls(v):
    if v == '':
        return
    global ls
    ls.discard(v)


async def reset_apikeys_default():
    global apikeys
    apikeys = driver.config.apikeys


def format_group_message(msg_pairs: dict, user_id=None, user_name='纯路人'):
    nodes = []
    if user_id is None:
        user_id = bot_info['user_id']
        user_name = bot_info['nickname']
    for key, data in msg_pairs.items():
        nodes.append(MessageSegment.node_custom(user_id, user_name, key))
        if data:
            nodes.append(MessageSegment.node_custom(bot_info['user_id'], bot_info['nickname'], data))
    return nodes


async def load_manager() -> dict:
    with open(r'./src/data/auth/managers.json', 'r') as f:
        return json.load(f)


async def set_manager(uin, status) -> bool:
    global managers
    managers[uin] = status
    try:
        with open(r'./src/data/auth/managers.json', 'w') as f:
            json.dump(managers, f)
            return True
    except Exception as err:
        print(err)
        return False


async def load_switcher() -> dict:
    with open(r'./src/data/auth/switchers.json', 'r') as f:
        return json.load(f)


async def set_switcher(group_id, key, status) -> str:
    global group_switcher
    group_id = str(group_id)
    status_ret = '启动' if status else '关闭'
    try:
        switcher_map = group_switcher[group_id]
    except:
        switcher_map = default_switcher_map.copy()
    try:
        if switcher_map[key] == status:
            return f'{key}已经{status_ret}'
    except:
        return f'没有{key}这种功能'
    switcher_map[key] = status
    group_switcher[group_id] = switcher_map
    with open(r'./src/data/auth/switchers.json', 'w') as f:
        json.dump(group_switcher, f)
    return f'{key}{status_ret}成功'


def check_switcher(group_id, key) -> dict:
    global group_switcher
    group_id = str(group_id)
    try:
        switcher_map = group_switcher[group_id]
    except:
        switcher_map = default_switcher_map.copy()
        group_switcher[group_id] = switcher_map
    try:
        if switcher_map[key]:
            return switcher_map
    except:
        return dict()
    return dict()
