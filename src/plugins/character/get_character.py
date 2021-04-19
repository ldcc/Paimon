import difflib
import json
import re

import bs4
import requests
from xpinyin import Pinyin


def nic2name(name):
    with open(r"./src/data/character/nickname.json", 'r', encoding='utf-8') as f:
        all = json.load(f)
        f.close()
    for i in all:
        for x in i.values():
            if name in x:
                return x[0]
    return name


def get_json(name: str) -> dict:
    name = nic2name(name)
    res = requests.get(f'https://genshin.minigg.cn/?data={name}')
    soup = bs4.BeautifulSoup(res.text, "lxml").body
    character_json = json.loads(soup.text)
    return character_json


def get_icon(data: dict) -> str:
    url = data['avatar'].split('?')[0]
    png_name = url.split('/')[-1]
    return f'[CQ:image,file={png_name},url={url}]'


def get_character(name: str) -> str:
    nick_name = nic2name(name)
    try:
        data0 = get_json(nick_name)
        data = data0['角色信息']
        if nick_name == '旅行者':
            data["简介"] = '无'
    except:
        correct_result = auto_correct(nick_name)
        if correct_result is None:
            return f"派蒙这里没找到{name}，可能是派蒙的错，可能是你输入的名字不正确哦。"
        else:
            if len(correct_result) > 1:
                return f"派蒙这里没找到{name}，你是要搜索如下的角色吗?\n{montage_result(correct_result)}"
            elif len(correct_result) < 1:
                return f"派蒙这里没找到{name}，可能是派蒙的错，可能是你输入的名字不正确哦。"
            else:
                return f"派蒙这里没找到{name}，你是要搜索{correct_result[0]}吗"

    result = nick_name + '\n' + get_icon(data0) + '\n'
    result += '称号：' + str(data['称号']) + '\n'
    result += '简介：' + str(data['简介'])
    result += '生日：' + str(data['生日']) + '\n'
    result += '所属：' + str(data['所属']) + '\n'
    result += '武器类型：' + str(data['武器类型']) + '\n'
    result += '命之座：' + str(data['命之座']) + '\n'
    try:
        result += '神之心：' + str(data['神之心']) + '\n'
    except:
        result += '神之眼：' + str(data['神之眼']) + '\n'
    return result


async def get_mz(name_mz: str) -> str:
    name = nic2name(name_mz.replace(" ", ""))
    try:
        data0 = get_json(name)
        data = data0['命之座']
    except:
        return f"派蒙这没有{name}，可能是官方资料没有该资料，可能是你输入的名字不正确哦。"
    result = ''
    n = 1
    for key, value in data.items():
        result += str(n) + ' 命：' + key + ' - ' + str(value['introduction']) + '\n'
        n += 1
    return '\n' + result


def auto_correct(name: str) -> list:
    with open(r"./src/data/character/character_index.json", "r", encoding="utf-8") as f:
        character_index = json.loads(f.read())
    input_pin_yin_list = Pinyin().get_pinyin(name).split("-")
    result_cache = []
    result = []
    for index_name in character_index:
        true_name = list(index_name.keys())[0]
        for input_pin_yin in input_pin_yin_list:
            for true_pin_yin in index_name[true_name]:
                if difflib.SequenceMatcher(None, true_pin_yin, input_pin_yin).quick_ratio() >= 1:
                    result_cache.append(true_name)
        if difflib.SequenceMatcher(None, true_name, name).quick_ratio() >= 0.3:
            result_cache.append(true_name)
    for result_repeat in result_cache:
        if result_cache.count(result_repeat) > 1 and not result_repeat in result:
            result.append(result_repeat)
    return result


def montage_result(correct_result: list) -> str:
    cause = correct_result[0]
    for i in range(1, len(correct_result)):
        cause = cause + "\n" + correct_result[i]
    return cause
