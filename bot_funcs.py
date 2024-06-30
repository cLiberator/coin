from string import digits, ascii_uppercase, ascii_lowercase
from dotenv import dotenv_values
import datetime
from aiogram import Bot
from aiogram.types import ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner

config = dotenv_values('bot.env')
bot = Bot(token=config['api'])
base64 = digits + ascii_uppercase + ascii_lowercase


def format_text(text):
    s = ''
    for c in text:
        if c in ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']:
            s += f'\{c}'
        else:
            s += c
    return s


async def subscribe_check(user_id, channel):
    try:
        user = await bot.get_chat_member('@' + channel.split('/')[-1], user_id)
        if type(user) in [ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner]:
            return 1
        else:
            return 0
    except:
        return 0


def convert_seconds(seconds):
    r = str(datetime.timedelta(seconds=seconds))
    r = r[:-6] + 'ч' + r[-6:]
    r = r[:-3] + 'м' + r[-3:]
    r += 'с'
    return r


def wallet_check(wallet):
    if all(c in base64 for c in wallet):
        return True
    return False
