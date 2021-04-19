from nonebot import on_command
from .qiu_qiu_translation import qiu_qiu_word_translation, qiu_qiu_phrase_translation

qqtrans = on_command("丘丘翻译")
qqdicts = on_command("丘丘词典")


@qqtrans.handle()
async def _(bot, event, state):
    txt = event.get_message().extract_plain_text().strip().lower()
    msg = qiu_qiu_word_translation(txt)
    await qqtrans.finish(msg)


@qqdicts.handle()
async def _(bot, event, state):
    txt = event.get_message().extract_plain_text().strip().lower()
    msg = qiu_qiu_phrase_translation(txt)
    await qqtrans.finish(msg)
