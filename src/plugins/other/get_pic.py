import base64
import io
import random

import nonebot
from PIL import Image, ImageDraw
from httpx import AsyncClient


async def setu_pic3(keyword='', r18=False) -> str:
    apikey = nonebot.get_driver().config.apikey
    r18 = 1 if r18 else 0
    proxy = 'disable'
    if nonebot.get_driver().config.setu_proxy:
        proxy = 'i.pixiv.cat'
    async with AsyncClient() as client:
        req_url = "https://api.lolicon.app/setu/"
        params = {
            "apikey": apikey,
            "r18": r18,
            "size1200": 'true',
            'keyword': keyword,
            'proxy': proxy
        }
        res = await client.get(req_url, params=params)
        try:
            data = res.json()['data'][0]
            title = data['title']
            url = data['url']
            pid = data['pid']
            author = data['author']
            pic = f'[CQ:image,file=base64://{await down_pic(url, pid)}]'
            msg = f"给大佬递图\nPid: {str(pid)}\nTitle: {title}\n画师: {author}\nUrl: {url}\n{pic}"
            return msg
        except Exception as err:
            print(res.text)
            print(err)
            if '额度限制' not in res.text:
                return f"图库中没有搜到关于{keyword}的图。今日额度还剩下{res.json()['quota']}次。"
            else:
                return 'api调用已到达上限'


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


def anti_harmonious(pic):
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
