from dotenv import dotenv_values
from bot_funcs import format_text

config = dotenv_values('bot.env')
main_channel = config['main_channel_name']
bot_name = config['bot_name']
reg = int(config['reg'])
ref = int(config['ref'])
drop_time = int(config['drop_time'])
drop = int(config['drop'])
ref_link = format_text(f"https://t.me/{bot_name}?start=")

start_text = '''AIRDROP BALABOL COIN👺

Условия участия ещё никогда не были настолько простыми
Абсолютно каждый участник получит токены $BLB👺

Чтобы участвовать, Вам необходимо:
1\. Пригласить как можно больше друзей
3\. Каждые 8 часов нажимать на кнопку ✈️ ️ДРОП✈️ в боте, получая дополнительные $BLB👺

За каждого приведённого друга вы получите 500 $BLB👺

Вы можете пригласить друзей по вашей персональной реферальной ссылке\. Просто нажмите на кнопку
🤑ЗАРАБОТАТЬ🤑'''

start_bonus_text = f'Начислено {reg} $BLB👺 за регистрацию'

error_handler_text = '''Произошла непредвиденная *_ошибка_*\! Действие *_сброшено_*

*_Повторите ввод_* команды'''

subscribe_text = f'Для использования функций бота необходимо *_быть подписанным_* на [наш канал]({format_text(main_channel)})'

new_subscribe_is_valid_text = 'Для получения приветственного бонуса нажмите на кнопку\n🤓УСЛОВИЯ🤓'

subscribe_is_valid_text = 'Команды снова доступны'

subscribe_is_not_valid_text = f'Пользователь не подписан на канал'

link_text = f'Ваша реферальная ссылка:\n\n`{ref_link}'

referrals_count_text = '\n\nКоличество рефералов: '

referrer_success_text = f'Начислено {ref} $BLB👺 за реферала'

drop_success_text = f'Вы получили вознаграждение в виде {drop} $BLB👺\n\nСледующая попытка через 8 ч\. 0 мин\.'

drop_fail_text = f'Не так быстро\! До следующего дропа осталось: '

wallet_info_text = 'Привяжите свой кошелек сети TON \(Tonkeeper, My TON wallet, Ton Hub\)\n\nПривязанный кошелёк: '

send_wallet_text = 'Укажите адрес кошелька в сети TON'

wallet_change_success_text = 'Кошелёк был успешно привязан'

wallet_change_fail_text = 'Ошибка привязки кошелька\! Введён некорректный адрес'
