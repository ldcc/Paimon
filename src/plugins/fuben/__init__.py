import os
from datetime import datetime
from nonebot.adapters.cqhttp import Bot, Event, Message
from nonebot.rule import to_me
from nonebot import on_command

FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "fuben")).replace("\\","/")
# FILE_PATH = ""

zb = on_command('周本')
tf = on_command('天赋', rule=to_me())
we = on_command('武器', rule=to_me())


@zb.handle()
async def _(bot: Bot, event: Event):
    print(f'[CQ:image,file=file:///{FILE_PATH}/zb.png]')
    await zb.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/zb.png]'))


@tf.handle()
async def _(bot: Bot, event: Event):
    mes = str(event.get_message())
    if '一' in mes:
        await tf.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/tf1.png]'))
    elif '二' in mes:
        await tf.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/tf2.png]'))
    elif '三' in mes:
        await tf.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/tf3.png]'))
    elif '四' in mes:
        await tf.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/tf4.png]'))
    elif '五' in mes:
        await tf.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/tf5.png]'))
    elif '六' in mes:
        await tf.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/tf6.png]'))
    else:
        day = str(datetime.now().isoweekday())
        if day != '7':
            await tf.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/tf{day}.png]'))
        else:
            await tf.finish('今天星期天所有副本都可以刷哦！')


@we.handle()
async def _(bot: Bot, event: Event):
    mes = str(event.get_message())
    if '一' in mes:
        await we.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/we1.png]'))
    elif '二' in mes:
        await we.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/we2.png]'))
    elif '三' in mes:
        await we.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/we3.png]'))
    elif '四' in mes:
        await we.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/we4.png]'))
    elif '五' in mes:
        await we.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/we5.png]'))
    elif '六' in mes:
        await we.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/we6.png]'))
    else:
        day = str(datetime.now().isoweekday())
        if day != '7':
            await we.finish(message=Message(f'[CQ:image,file=file:///{FILE_PATH}/we{day}.png]'))
        else:
            await we.finish('今天星期天所有副本都可以刷哦！')
