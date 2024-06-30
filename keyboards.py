from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

default_reply_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🤓УСЛОВИЯ🤓'),
                                                        KeyboardButton(text='💰БАЛАНС💰')],
                                                       [KeyboardButton(text='🤑ЗАРАБОТАТЬ🤑'),
                                                        KeyboardButton(text='✈️ДРОП✈️')],
                                                       [KeyboardButton(text='👛КОШЕЛЁК👛')]],
                                             resize_keyboard=True,
                                             input_field_placeholder='Нажмите на кнопку или введите команду...')

wallet_reply_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='ПРИВЯЗАТЬ НОВЫЙ КОШЕЛЁК')],
                                                       [KeyboardButton(text='ГЛАВНОЕ МЕНЮ')]],
                                            resize_keyboard=True,
                                            input_field_placeholder='Нажмите на кнопку или введите команду...')

check_subscribe_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='ПРОВЕРИТЬ ПОДПИСКУ',
                                                                  callback_data='check_subscribe')]])