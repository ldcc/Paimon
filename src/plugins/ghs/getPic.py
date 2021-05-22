import nonebot
from httpx import AsyncClient


async def ghs_pic3(keyword='') -> str:
    apikey = nonebot.get_driver().config.apikey
    proxy = 'disable'
    if nonebot.get_driver().config.setu_proxy:
        proxy = 'i.pixiv.cat'
    async with AsyncClient() as client:
        req_url = "https://api.lolicon.app/setu/"
        params = {
            "apikey": apikey,
            "r18": nonebot.get_driver().config.r18,
            "size1200": 'true',
            'keyword': keyword,
            'proxy': proxy
        }
        res = await client.get(req_url, params=params)
        try:
            data = res.json()['data'][0]
            title = data['title']
            url = str(data['url']).replace("\\", "")
            pid = data['pid']
            author = data['author']
            msg = f"给大佬递图\nTitle: {title}\nPid: {str(pid)}\n画师: {author}\nUrl: {url}\n[CQ:image,file={url}]"
            return msg
        except Exception as err:
            print(res.text)
            print(err)
            if '额度限制' not in res.text:
                return f"图库中没有搜到关于{keyword}的图。今日额度还剩下{res.json()['quota']}次。"
            else:
                return 'api调用已到达上限'
