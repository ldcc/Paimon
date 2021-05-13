import nonebot
from nonebot.adapters.cqhttp import Bot
from nonebot import require

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter('cqhttp', Bot)
nonebot.load_plugins("src/plugins")
bot_me: Bot


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


if __name__ == '__main__':
    nonebot.run()
