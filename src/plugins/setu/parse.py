from typing import Union
from PicImageSearch.ascii2d import Ascii2DResponse
from PicImageSearch.saucenao import SauceNAOResponse
from PicImageSearch.tracemoe import TraceMoeResponse
from PicImageSearch.google import GoogleResponse
from nonebot.adapters.onebot.v11 import MessageSegment

def format_data(re: Union[Ascii2DResponse, SauceNAOResponse, TraceMoeResponse, GoogleResponse]) -> MessageSegment:
    re.raw
    pass
