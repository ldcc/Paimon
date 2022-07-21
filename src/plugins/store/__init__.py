import base64
import os
from threading import Timer

from nonebot import on_command, on_message, get_bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, Event, ActionFailed
from nonebot.typing import T_State
from nonebot.rule import to_me
from .parse import get_data
import src.plugins as cfg

keys = on_command('圣经', rule=to_me())
save = on_command('记录')
drop = on_command('删除记录', aliases={'删除圣经'})
load = on_message(priority=10)
spec_sym = ';:{}[],./<>?~!@#$%^&*()_+|`-=\\，。、《》？；：‘’“”【】'
chat = True
cd = 1  # sec


@keys.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg_pairs = dict.fromkeys(cfg.ls)
    msg_list = cfg.format_group_message(msg_pairs)
    print(msg_list)
    await bot.send_group_forward_msg(group_id=event.group_id, messages=Message(msg_list))


@save.handle()
async def _(bot: Bot, event: Event, state: T_State):
    pair = state["_prefix"]["command_arg"]
    if len(pair) < 1:
        await save.finish(message=Message('错误的格式'))
    state['instruct'] = str(pair[0]).strip()
    if len(pair) > 1:
        state['content'] = pair[1:]


@save.got('content', prompt='请发送要记录的数据')
async def _(bot: Bot, event: Event, state: T_State):
    instruct = state['instruct']
    if len(instruct) < 3:
        await save.finish(message='关键词不能太短')
    if any(map(lambda c: c in spec_sym, instruct)):
        await save.finish(message='含有非法关键字')

    msgs = Message(state['content'])
    content = await get_data(msgs)
    if content == '':
        await save.finish(message='解析内容出错')
    file = os.path.join(cfg.STORE_PATH, instruct)
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = base64.b64decode(f.read()).decode() + content
    try:
        with open(file, 'w', encoding='utf-8') as f:
            data = base64.b64encode(content.encode()).decode()
            f.write(data)
    except:
        return
    await cfg.stash_ls(instruct)
    await save.finish(message=Message('👌'))


@drop.handle()
async def _(bot: Bot, event: Event, state: T_State):
    instructs = state["_prefix"]["command_arg"]
    if instructs:
        state['instructs'] = instructs


@drop.got('instructs', prompt='请发送要删除的圣经')
async def _(bot: Bot, event: Event, state: T_State):
    instructs = str(state['instructs']).strip().split(' ')
    if len(instructs) == 0:
        await drop.finish(message=Message('参数错误'))

    async def rm(instruct):
        file = os.path.join(cfg.STORE_PATH, instruct)
        if not os.path.exists(file):
            await drop.send(message=Message(f'没有{instruct}这条圣经'))
            return False
        os.remove(file)
        await cfg.drop_ls(instruct)
        return True

    if all([await rm(ins) for ins in instructs]):
        await drop.finish(message=Message('👌'))


@load.handle()
async def _(bot: Bot, event: Event, state: T_State):
    global chat
    if chat:
        msg = str(state["_prefix"]["command_arg"]).strip()
        for instruct in cfg.ls:
            file = os.path.join(cfg.STORE_PATH, instruct)
            if instruct in msg and os.path.exists(file):
                chat = False
                Timer(cd, allow_chat).start()
                with open(file, 'r', encoding='utf-8') as f:
                    data = base64.b64decode(f.read()).decode()
                try:
                    await load.finish(message=Message(data))
                except ActionFailed:
                    print(data)


def allow_chat():
    global chat
    chat = True
