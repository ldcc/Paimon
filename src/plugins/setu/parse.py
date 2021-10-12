from typing import Union
from PicImageSearch.Async.ascii2d import Ascii2DResponse
from PicImageSearch.Async.saucenao import SauceNAOResponse
from PicImageSearch.Async.tracemoe import TraceMoeResponse
from PicImageSearch.Async.google import GoogleResponse
from nonebot.adapters.cqhttp import MessageSegment

def format_data(re: Union[Ascii2DResponse, SauceNAOResponse, TraceMoeResponse, GoogleResponse]) -> MessageSegment:
    re.raw
    pass
