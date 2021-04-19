from nonebot import on_command
from nonebot.rule import to_me
from .qiu_qiu_translation import qiu_qiu_word_translation, qiu_qiu_phrase_translation

suffix = "\n※ 这个插件只能从丘丘语翻译为中文，不能反向翻译\n※ 发送词语时请注意空格位置是否正确，词语不区分大小写，不要加入任何标点符号\n※ 翻译数据来源于 米游社论坛 " \
         "https://bbs.mihoyo.com/ys/article/2286805 \n※ 如果你有更好的翻译欢迎来提出 issues "

qqtrans = on_command("丘丘一下", rule=to_me())
qqdicts = on_command("丘丘词典", rule=to_me())


@qqtrans.handle()
async def _(bot, event, state):
    txt = event.get_message().extract_plain_text().strip().lower()
    if txt:
        state["qq_sentence"] = txt


@qqtrans.got("qq_sentence")
async def _(bot, state):
    txt = state["qq_sentence"]
    msg = qiu_qiu_word_translation(txt)
    msg += suffix
    await qqtrans.finish(msg)


@qqdicts.handle()
async def _(bot, event, state):
    txt = event.get_message().extract_plain_text().strip().lower()
    if txt:
        state["qq_dictionary"] = txt


@qqdicts.got("qq_dictionary")
async def _(bot, state):
    txt = state["qq_dictionary"]
    msg = qiu_qiu_phrase_translation(txt)
    msg += suffix
    await qqtrans.finish(msg)
