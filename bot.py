import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter('cqhttp', CQHTTPBot)
nonebot.load_from_toml('pyproject.toml')

app = nonebot.get_asgi()

if __name__ == '__main__':
    nonebot.run()
