from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot
from nonebot.rule import to_me
import src.plugins as cfg

help = on_command('help', rule=to_me(), aliases={'帮助'})


@help.handle()
async def _(bot: Bot):
    await help.finish(f'1.发送 [功能<开启/关闭> 功能名] 开启/关闭{cfg.bot_info["nickname"]}的可选功能\n'
                      f'2.发送 [记录 <关键字> <数据>] 可以记录圣经，当对话中含有关键字时自动触发圣经\n'
                      f'3.发送 [删除记录 <关键字> ...] 批量删除已记录的圣经\n'
                      f'4.@{cfg.bot_info["nickname"]} 后发送 [圣经] 查看所有圣经\n'
                      # f'5.发送 [色图<关键词>] 。。。\n'
                      f'项目开源地址：https://github.com/ldcc/Lemon')
