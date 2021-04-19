from nonebot import on_command
from .translate import word_translation, phrase_translation

qqtrans = on_command("丘丘翻译")
qqdicts = on_command("丘丘词典")


@qqtrans.handle()
async def _(bot, event):
    txt = event.get_message().extract_plain_text().strip().lower()
    msg = word_translation(txt)
    await qqtrans.finish(msg)


@qqdicts.handle()
async def _(bot, event):
    txt = event.get_message().extract_plain_text().strip().lower()
    msg = phrase_translation(txt)
    await qqtrans.finish(msg)
