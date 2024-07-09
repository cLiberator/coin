from time import time
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ErrorEvent, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards import *
from phrases import *
from database_requests import *
from bot_funcs import *

user_router = Router()


class User(StatesGroup):
    referrer_id = State()
    wallet = State()


@user_router.message(CommandStart())
@user_router.message(F.text == '🤓УСЛОВИЯ🤓')
@user_router.message(F.text == 'ГЛАВНОЕ МЕНЮ')
async def cmd_start(message: Message, state: FSMContext):
    if message.chat.type == 'private':
        if await is_new_user(message.from_user.id):
            referrer_id = None
            if len(message.text) > 7:
                referrer_id = int(message.text[7:])
            await state.update_data(referrer_id=referrer_id)
            await add_user(message.from_user.id)
        if await subscribe_check(message.from_user.id, main_channel):
            try:
                referrer_id = await state.get_data()
                referrer_id = referrer_id['referrer_id']
                if referrer_id is not None and referrer_id != message.from_user.id:
                    await increment_referrers_count(referrer_id)
                    await increment_token_balance(referrer_id, ref)
                    try:
                        await bot.send_message(referrer_id, referrer_success_text)
                    except:
                        pass
                    await state.update_data(referrer_id=None)
            except:
                await state.update_data(referrer_id=None)
            await message.answer_photo(FSInputFile('images/terms.jpg'), start_text, parse_mode="MarkdownV2",
                                       reply_markup=default_reply_keyboard)
            if await get_token_balance(message.from_user.id) == 0:
                await increment_token_balance(message.from_user.id, reg)
                await message.answer(new_subscribe_is_valid_text, parse_mode="MarkdownV2",
                                     reply_markup=default_reply_keyboard)
        else:
            await message.answer(subscribe_text, parse_mode="MarkdownV2", reply_markup=check_subscribe_keyboard)


@user_router.callback_query(F.data == 'check_subscribe')
async def check_subscribe(callback: CallbackQuery, state: FSMContext):
    if await subscribe_check(callback.from_user.id, main_channel):
        try:
            referrer_id = await state.get_data()
            referrer_id = referrer_id['referrer_id']
            if referrer_id is not None and referrer_id != callback.from_user.id:
                await increment_referrers_count(referrer_id)
                await increment_token_balance(referrer_id, ref)
                try:
                    await bot.send_message(referrer_id, referrer_success_text)
                except:
                    pass
                await state.update_data(referrer_id=None)
        except:
            await state.update_data(referrer_id=None)
        await callback.message.delete()
        if await get_token_balance(callback.from_user.id) == 0:
            await increment_token_balance(callback.from_user.id, reg)
            await callback.message.answer(new_subscribe_is_valid_text, parse_mode="MarkdownV2",
                                          reply_markup=default_reply_keyboard)
        else:
            await callback.message.answer(subscribe_is_valid_text, parse_mode="MarkdownV2",
                                          reply_markup=default_reply_keyboard)
    else:
        await callback.answer(subscribe_is_not_valid_text, parse_mode="MarkdownV2")


@user_router.message(F.text == '🤑ЗАРАБОТАТЬ🤑')
@user_router.message(Command('link'))
async def get_referral_link(message: Message):
    if message.chat.type == 'private':
        if await subscribe_check(message.from_user.id, main_channel):
            text = link_text + str(message.from_user.id) + '`' + referrals_count_text + \
                   str(await get_referrers_count(message.from_user.id))
            await message.answer_photo(FSInputFile('images/referral_link.jpg'), text, parse_mode="MarkdownV2",
                                       reply_markup=default_reply_keyboard)
        else:
            await message.answer(subscribe_text, parse_mode="MarkdownV2", reply_markup=check_subscribe_keyboard)


@user_router.message(F.text == '💰БАЛАНС💰')
@user_router.message(Command('balance'))
async def get_balance(message: Message):
    if message.chat.type == 'private':
        if await subscribe_check(message.from_user.id, main_channel):
            await message.answer_photo(FSInputFile('images/balance.jpg'),
                                       f'Баланс: {await get_token_balance(message.from_user.id)} '
                                       f'$BLB\n\n1 реферал \= 500 $BLB',
                                       parse_mode="MarkdownV2", reply_markup=default_reply_keyboard)
        else:
            await message.answer(subscribe_text, parse_mode="MarkdownV2", reply_markup=check_subscribe_keyboard)


@user_router.message(F.text == '✈️ДРОП✈️')
@user_router.message(Command('balabol'))
async def get_drop(message: Message):
    if message.chat.type == 'private':
        if await subscribe_check(message.from_user.id, main_channel):
            if int(time()) >= await get_last_drop_date(message.from_user.id) + drop_time:
                await increment_token_balance(message.from_user.id, drop)
                await set_last_drop_date(message.from_user.id, int(time()))
                await message.answer_photo(FSInputFile('images/drop.jpg'), drop_success_text, parse_mode="MarkdownV2",
                                           reply_markup=default_reply_keyboard)
            else:
                d = await get_last_drop_date(message.from_user.id) + drop_time - int(time())
                d = convert_seconds(d)
                await message.answer(drop_fail_text+d, parse_mode="MarkdownV2", reply_markup=default_reply_keyboard)
        else:
            await message.answer(subscribe_text, parse_mode="MarkdownV2", reply_markup=check_subscribe_keyboard)


@user_router.message(F.text == '👛КОШЕЛЁК👛')
@user_router.message(Command('wallet'))
async def get_wallet_cmd(message: Message):
    if message.chat.type == 'private':
        if await subscribe_check(message.from_user.id, main_channel):
            await message.answer_photo(FSInputFile('images/wallet.jpg'),
                                       wallet_info_text + '`' + format_text(await get_wallet(message.from_user.id)) +
                                       '`', parse_mode="MarkdownV2", reply_markup=wallet_reply_keyboard)
        else:
            await message.answer(subscribe_text, parse_mode="MarkdownV2", reply_markup=check_subscribe_keyboard)


@user_router.message(F.text == 'ПРИВЯЗАТЬ НОВЫЙ КОШЕЛЁК')
async def cmd_change_wallet(message: Message, state: FSMContext):
    if message.chat.type == 'private':
        if await subscribe_check(message.from_user.id, main_channel):
            await state.set_state(User.wallet)
            await message.answer(send_wallet_text, parse_mode="MarkdownV2", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(subscribe_text, parse_mode="MarkdownV2", reply_markup=check_subscribe_keyboard)


@user_router.message(User.wallet)
async def cmd_set_wallet(message: Message, state: FSMContext):
    if message.chat.type == 'private':
        if await subscribe_check(message.from_user.id, main_channel):
            await state.update_data(wallet=message.text)
            data = await state.get_data()
            if wallet_check(data['wallet']):
                await set_wallet(message.from_user.id, data['wallet'])
                await message.answer(wallet_change_success_text, parse_mode="MarkdownV2",
                                     reply_markup=default_reply_keyboard)
            else:
                await message.answer(wallet_change_fail_text, parse_mode="MarkdownV2",
                                     reply_markup=default_reply_keyboard)
        else:
            await message.answer(subscribe_text, parse_mode="MarkdownV2", reply_markup=check_subscribe_keyboard)


@user_router.error(F.update.message.as_("message"))
async def exception_handler(event: ErrorEvent, message: Message, state: FSMContext):
    if message.chat.type == 'private':
        print(event.exception)
        await state.update_data(referrer_id=None)
        await message.answer(error_handler_text, parse_mode="MarkdownV2", reply_markup=default_reply_keyboard)
