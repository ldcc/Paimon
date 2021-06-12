import base64
import io
import os
import random

from PIL import Image, ImageDraw
from httpx import AsyncClient
from nonebot.adapters.cqhttp.message import MessageSegment
import src.plugins as cfg


async def setu_pic(keyword='', r18=False, is_proxy=False) -> MessageSegment:
    pic = ''
    while len(cfg.apikeys) > 0:
        apikey = cfg.apikeys.pop(0)
        pic = await setu_pic3(keyword, r18, apikey, is_proxy)
        if pic != 'api调用已到达上限':
            cfg.apikeys.append(apikey)
            return pic
    await cfg.reset_apikeys_default()
    return pic


async def setu_pic3(keyword='', r18=False, apikey='', is_proxy=False) -> MessageSegment:
    r18 = 1 if r18 else 0
    proxy = 'i.pximg.net'
    if is_proxy:
        proxy = 'i.pixiv.cat'
    async with AsyncClient() as client:
        req_url = 'https://api.lolicon.app/setu/'
        params = {
            'apikey': apikey,
            'r18': r18,
            'size1200': 'true',
            'keyword': keyword,
            'proxy': proxy
        }
        try:
            res = await client.get(req_url, params=params)
        except:
            return MessageSegment.text('网络错误，请稍后重试')
        try:
            data = res.json()['data'][0]
        except:
            print(res.text)
            if '额度限制' in res.text:
                return MessageSegment.text('api调用已到达上限')
            else:
                return MessageSegment.text(f'图库中没有搜到关于{keyword}的图。')

        author = data['author']
        title = data['title']
        url = data['url']
        pid = data['pid']
        try:
            return MessageSegment.image(f'base64://{await down_pic(url, pid)}')
        except Exception as err:
            return MessageSegment.text(f'获取图片失败\n画师: {author}\nTitle: {title}\nUrl: {url}\nErr: {err}')


async def down_pic(url, pid) -> str:
    async with AsyncClient() as client:
        headers = {
            'Referer': f'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={pid}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        re = await client.get(url=url, headers=headers)
        pic = anti_harmonious(re.content)
        return base64.b64encode(pic).decode()


def anti_harmonious(pic: bytes) -> bytes:
    im = Image.open(io.BytesIO(pic))
    if im.mode != 'RGB':
        im = im.convert('RGB')
    width, height = im.size
    draw = ImageDraw.Draw(im)
    draw.point((random.randint(1, width), random.randint(1, height)), fill=(random.randint(0, 255),
                                                                            random.randint(0, 255),
                                                                            random.randint(0, 255)))
    pic = io.BytesIO()
    im.save(pic, format='JPEG')
    return pic.getvalue()
