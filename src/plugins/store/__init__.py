import base64
import os
from threading import Timer

from nonebot import on_command, on_message
from nonebot.adapters.cqhttp import GroupMessageEvent, Bot, Message, Event
from nonebot.typing import T_State
import src.plugins as cfg

keys = on_command('圣经')
save = on_command('记录')
drop = on_command('删除圣经', aliases={'圣经删除'})
load = on_message(priority=10)
spec_sym = ';:{}[],./<>?~!@#$%^&*()_+|`-=\\，。、《》？；：‘’“”【】'
chat = True
cd = 1  # sec


@keys.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    mes_list = cfg.format_group_message(cfg.ls)
    await bot.send_group_forward_msg(group_id=event.group_id, messages=Message(mes_list))


@save.handle()
async def _(bot: Bot, event: Event, state: T_State):
    pair = str(event.get_message()).strip().split(' ', 1)
    if len(pair) < 2:
        pair = str(event.get_message()).strip().split('\n', 1)
    if len(pair) < 1:
        await save.finish(message=Message('错误的格式'))
    state['instruct'] = pair[0].strip()
    if len(pair) == 2:
        state['content'] = pair[1]


@save.got('content', prompt='请发送要记录的数据')
async def _(bot: Bot, event: Event, state: T_State):
    instruct = state['instruct']
    content = str(state['content']).strip()
    if len(instruct) < 2:
        await save.finish(message='关键词不能太短')
    if any(map(lambda c: c in spec_sym, instruct)):
        await save.finish(message='含有非法关键字')

    file = os.path.join(r'./src/data/store', instruct)
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content += base64.b64decode(f.read()).decode()
    try:
        with open(file, 'w', encoding='utf-8') as f:
            data = base64.b64encode(content.encode()).decode()
            f.write(data)
    except:
        return
    await cfg.append_ls(instruct)
    await save.finish(message=Message('👌'))


@drop.handle()
async def _(bot: Bot, event: Event, state: T_State):
    instructs = event.get_message()
    if instructs:
        state['instructs'] = instructs


@drop.got('instructs', prompt='请发送要删除的圣经')
async def _(bot: Bot, event: Event, state: T_State):
    instructs = str(state['instructs']).strip().split(' ')
    if len(instructs) == 0:
        await drop.finish(message=Message('参数错误'))

    async def rm(instruct):
        file = os.path.join(r'./src/data/store', instruct)
        if not os.path.exists(file):
            await drop.send(message=Message(f'没有{instruct}这条圣经'))
            return False
        os.remove(file)
        return True

    if all([await rm(ins) for ins in instructs]):
        await drop.finish(message=Message('👌'))


@load.handle()
async def _(bot: Bot, event: Event):
    global chat
    if chat:
        msg = str(event.get_message()).strip()
        for instruct in cfg.ls:
            file = os.path.join(r'./src/data/store', instruct)
            if instruct in msg and os.path.exists(file):
                chat = False
                Timer(cd, allow_chat).start()
                with open(file, 'r', encoding='utf-8') as f:
                    data = base64.b64decode(f.read()).decode()
                await load.finish(message=Message(data))


def allow_chat():
    global chat
    chat = True
