import base64

import nonebot
from httpx import AsyncClient


async def ghs_pic3(keyword='') -> str:
    apikey = nonebot.get_driver().config.apikey
    proxy = 'disable'
    if nonebot.get_driver().config.setuproxy:
        proxy = 'i.pixiv.cat'
    async with AsyncClient() as client:
        req_url = "https://api.lolicon.app/setu/"
        params = {
            "apikey": apikey,
            "r18": 0,
            "size1200": 'true',
            'keyword': keyword,
            'proxy': proxy
        }
        res = await client.get(req_url, params=params)
        try:
            setu_title = res.json()['data'][0]['title']
            setu_url = res.json()['data'][0]['url']
            setu_pid = res.json()['data'][0]['pid']
            setu_author = res.json()['data'][0]['author']
            msg = "给大佬递图\n" + "Title: " + setu_title + "\nPid: " + str(setu_pid) + "\n画师:" + setu_author + "\nUrl:"
            msg += "\n" "[CQ:image,file=base64://" + await down_pic(setu_url) + "]"
            return msg
        except Exception as e:
            print(res.text)
            print(e)
            if '额度限制' not in res.text:
                return f"图库中没有搜到关于{keyword}的图。今日额度还剩下{res.json()['quota']}次。"
            else:
                return 'api调用已到达上限'


async def down_pic(url) -> str:
    async with AsyncClient() as client:
        headers = {
            'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        re = await client.get(url=url, headers=headers)
        return base64.b64encode(re.content).decode()


if __name__ == '__main__':
    down_pic(ghs_pic3())
