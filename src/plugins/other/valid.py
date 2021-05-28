default_switch_map = {'色图': True, '防撤回': True, '戳一戳': True, '偷闪照': True, 'r18': False}
group_switcher = dict()


async def set_switch(group_id, key, status) -> str:
    global group_switcher
    status_ret = '启动' if status else '关闭'
    try:
        switch_map = group_switcher[group_id]
    except:
        switch_map = default_switch_map
    try:
        if switch_map[key] == status:
            return f'{key}已经{status_ret}'
    except:
        return f'没有{key}这种功能'
    switch_map[key] = status
    group_switcher[group_id] = switch_map
    return f'{key}{status_ret}成功'


def check_switch(group_id, key) -> dict:
    global group_switcher
    try:
        switch_map = group_switcher[group_id]
    except:
        switch_map = default_switch_map
        group_switcher[group_id] = switch_map
    try:
        if switch_map[key]:
            return switch_map
    except:
        return dict()
    return dict()
