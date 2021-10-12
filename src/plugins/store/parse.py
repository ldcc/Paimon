import base64

from httpx import AsyncClient
from nonebot.adapters.cqhttp import Message, MessageSegment


async def get_data(msgs: Message) -> str:
    data = ''
    for seg in msgs:
        seg: MessageSegment
        if seg.type == 'image':
            url = seg.data['url']
            async with AsyncClient() as client:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
                }
                re = await client.get(url=url, headers=headers)
                pic = base64.b64encode(re.content).decode()
                seg = MessageSegment.image(f'base64://{pic}')
        data += str(seg).strip()
    return data
