import base64
import os

from nonebot import require, get_driver
from nonebot.adapters.cqhttp import Bot, Message

driver = get_driver()

bot_me: Bot = None
FILE_PATH = r'./src/data/cron'


@driver.on_bot_connect
async def _(bot: Bot):
    global bot_me
    bot_me = bot


@driver.on_bot_disconnect
async def _(bot: Bot):
    global bot_me
    bot_me = None


scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job('cron', hour='*')
async def _():
    if bot_me is not None:
        groups = await bot_me.get_group_list()
        for g in groups:
            await bot_me.send_group_msg(group_id=g['group_id'], message='整点报时咕咕咕')


@scheduler.scheduled_job('cron', hour='15', minute='*/16')
async def _():
    if bot_me is not None:
        groups = await bot_me.get_group_list()
        for g in groups:
            with open(os.path.join(FILE_PATH, '3.j.jpg'), "rb") as j3:
                pic = base64.b64encode(j3.read()).decode()
                message = Message(f'[CQ:image,file=base64://{pic}]')
                await bot_me.send_group_msg(group_id=g['group_id'], message=message)
