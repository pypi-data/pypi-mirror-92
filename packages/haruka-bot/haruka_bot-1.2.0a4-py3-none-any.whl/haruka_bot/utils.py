import asyncio
import os
import traceback
from os import path

import nonebot
from nonebot import get_driver, require
from nonebot.adapters.cqhttp import Bot, Event, MessageEvent
from nonebot.log import logger
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.rule import Rule
from pydantic import BaseSettings

# 更换 Chromium 下载地址为非 https 淘宝源
os.environ['PYPPETEER_DOWNLOAD_HOST'] = 'http://npm.taobao.org/mirrors'
# os.environ['PYPPETEER_DOWNLOAD_HOST'] = 'http://storage.googleapis.com'
from pyppeteer import launch # 不能删，隔壁 dynamic.py 还要调用的
from pyppeteer.chromium_downloader import check_chromium, download_chromium

# 检查 Chromium 是否下载
if not check_chromium():
    download_chromium()


class Config(BaseSettings):

    haruka_dir: str = None
    haruka_to_me: bool = True

    class Config:
        extra = 'ignore'

global_config = get_driver().config
plugin_config = Config(**global_config.dict())


def get_path(name):
    """获取数据文件绝对路径"""
    if plugin_config.haruka_dir:
        dir_path = path.abspath(plugin_config.haruka_dir)
    else:
        src_path = path.dirname(path.abspath(__file__))
        dir_path = path.join(src_path, 'data')
    f_path = path.join(dir_path, name)
    return f_path


async def permission_check(bot: Bot, event: MessageEvent, state: dict):
    from .config import Config
    config = Config()
    if event.message_type == 'private':
        return True
    group_id = str(event.group_id)
    with Config() as config:
        if config.get_admin(group_id):
            return await (GROUP_ADMIN | GROUP_OWNER | SUPERUSER)(bot, event)
        return True

def to_me():
    if plugin_config.haruka_to_me:
        from nonebot.rule import to_me
        return to_me()
    async def _to_me(bot: Bot, event: Event, state: dict):
        return True
    return Rule(_to_me)


async def safe_send(bot: Bot, send_type, type_id, message):
    """发送出现错误时, 尝试重新发送, 并捕获异常且不会中断运行"""
    i = 0
    while True:
        try:
            i += 1
            return await send(bot, send_type, type_id, message)
        except:
            logger.error(traceback.format_exc())
            if i == 3:
                bot = await restart(bot)
                warning_msg = '检测到推送出现异常，已尝试自动重启，如仍有问题请向机器人管理员反馈'
                await send(bot, send_type, type_id, warning_msg)
                return await send(bot, send_type, type_id, message)
            await asyncio.sleep(0.1)

async def send(bot, send_type, type_id, message):
    return await bot.call_api('send_'+send_type+'_msg', **{
        'message': message,
        'user_id' if send_type == 'private' else 'group_id': type_id
        })

async def restart(bot: Bot):
    await bot.set_restart()
    await asyncio.sleep(1)
    while True:
        new_bot = nonebot.get_bots().get(bot.self_id, None)
        if new_bot:
            break
        await asyncio.sleep(0.1)
    return new_bot


scheduler = require('nonebot_plugin_apscheduler').scheduler


# bot 启动时检查 src\data\haruka_bot\ 目录是否存在
if not path.isdir(get_path('')):
    os.makedirs(get_path(''))
