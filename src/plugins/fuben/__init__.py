from datetime import datetime

from nonebot.adapters.cqhttp import Message
from nonebot.rule import to_me
from nonebot import on_command

# fuben_uri = 'https://raw.githubusercontent.com/ldcc/Paimon/master/src/data/fuben'

zb = on_command('周本', rule=to_me())
tf = on_command('天赋', rule=to_me())
we = on_command('武器', rule=to_me())


@zb.handle()
async def _(bot, event):
    await zb.finish(message=Message('[CQ:image,http://pic.xiaoxuan.xyz:88/image/zb.png]'))


@tf.handle()
async def _(bot, event):
    mes = str(event.get_message())
    if '一' in mes:
        await tf.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/tf1.png]'))
    elif '二' in mes:
        await tf.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/tf2.png]'))
    elif '三' in mes:
        await tf.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/tf3.png]'))
    elif '四' in mes:
        await tf.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/tf4.png]'))
    elif '五' in mes:
        await tf.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/tf5.png]'))
    elif '六' in mes:
        await tf.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/tf6.png]'))
    else:
        day = str(datetime.now().isoweekday())
        if day != '7':
            await tf.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/tf{day}.png]'))
        else:
            await tf.finish('今天星期天所有副本都可以刷哦！')


@we.handle()
async def _(bot, event):
    mes = str(event.get_message())
    if '一' in mes:
        await we.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/we1.png]'))
    elif '二' in mes:
        await we.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/we2.png]'))
    elif '三' in mes:
        await we.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/we3.png]'))
    elif '四' in mes:
        await we.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/we4.png]'))
    elif '五' in mes:
        await we.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/we5.png]'))
    elif '六' in mes:
        await we.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/we6.png]'))
    else:
        day = str(datetime.now().isoweekday())
        if day != '7':
            await we.finish(message=Message(f'[CQ:image,file=http://pic.xiaoxuan.xyz:88/image/we{day}.png]'))
        else:
            await we.finish('今天星期天所有副本都可以刷哦！')
