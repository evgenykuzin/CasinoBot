import bank_users_service
import cashout_service
from bot_utils import send_message
from registration import check_user_not_registered


def get_balance(message):
    from bot_keyboards import cancel_cashout_inline_keyboard
    from bot_keyboards import cancel_get_money_inline_keyboard
    from bot_keyboards import BALANCE_KEYBOARD
    bank_user = bank_users_service.get_user_by_telegram_id(message.from_user.id)
    if check_user_not_registered(message, bank_user_ext=bank_user):
        return
    # account: Account = bank_users_service.get_account_of_user(bank_user.bank_user_id)
    send_message(message.from_user.id, f"Ваш текущий баланс: {bank_user.balance}. Кредит: {bank_user.credit}",
                 reply_markup=BALANCE_KEYBOARD.tg())


def get_money(message):
    from bot_keyboards import cancel_cashout_inline_keyboard
    from bot_keyboards import cancel_get_money_inline_keyboard
    from bot_keyboards import BALANCE_KEYBOARD
    if check_user_not_registered(message):
        return
    send_message(message.chat.id, "Введите сумму пополнения",
                 reply_markup=cancel_get_money_inline_keyboard.tg())
    from bot import bot
    bot.register_next_step_handler(message, get_money_amount)


def get_money_amount(message):
    from bot_keyboards import cancel_cashout_inline_keyboard
    from bot_keyboards import cancel_get_money_inline_keyboard
    from bot_keyboards import BALANCE_KEYBOARD
    amountstr: str = message.text
    if not amountstr.isnumeric() or int(amountstr) <= 0:
        send_message(message.from_user.id, "Сумма некорректна. Отправьте сумму еще раз.",
                     reply_markup=cancel_get_money_inline_keyboard.tg())
        from bot import bot
        bot.register_next_step_handler(message, get_money_amount)
        return
    amount = int(amountstr)
    bank_users_service.get_money(message.from_user.id, amount)
    send_message(message.from_user.id, f"Баланс пополнен на {amount} руб.")
    get_balance(message)


def cashout(message):
    from bot_keyboards import cancel_cashout_inline_keyboard
    from bot_keyboards import cancel_get_money_inline_keyboard
    from bot_keyboards import BALANCE_KEYBOARD
    bu = bank_users_service.get_user_by_telegram_id(message.from_user.id)
    if check_user_not_registered(message, bank_user_ext=bu):
        return
    send_message(message.from_user.id, "Введите сумму вывода средств",
                 reply_markup=cancel_cashout_inline_keyboard.tg())


def cashout_amount(message):
    from bot_keyboards import cancel_cashout_inline_keyboard
    from bot_keyboards import cancel_get_money_inline_keyboard
    from bot_keyboards import BALANCE_KEYBOARD
    amountstr: str = message.text
    if not amountstr.isnumeric() or int(amountstr) <= 0:
        send_message(message.from_user.id, "Сумма некорректна. Отправьте сумму еще раз.",
                     reply_markup=cancel_cashout_inline_keyboard.tg())
        from bot import bot
        bot.register_next_step_handler(message, cashout_amount)
        return
    amount = int(amountstr)
    bu = bank_users_service.get_user_by_telegram_id(message.from_user.id)
    cashout_service.cashout(bu, amount)
    get_balance(message)


def cancel_get_money(message):
    send_message(message.chat.id, "Отмена пополнения")
    from bot import bot
    bot.clear_step_handler_by_chat_id(message.chat.id)


def cancel_cashout(message):
    send_message(message.chat.id, "Отмена вывода средств")
    from bot import bot
    bot.clear_step_handler_by_chat_id(message.chat.id)

