import bank_users_service
import utils
from bot_utils import send_message, menu
from cache import find_registration, clear_registration


def registration(message):
    from bot_keyboards import cancel_registration_inline_keyboard
    from bot import bot
    user = message.from_user
    existed_user = bank_users_service.get_user_by_telegram_id(user.id)
    if existed_user is not None:
        send_message(message.from_user.id, "Вы уже зарегистрированы!")
        return
    reg = bank_users_service.find_registration(message)
    if reg.username is None and user.username is None:
        print(f"input username")
        send_message(message.from_user.id, "Введите ваш никнейм",
                     reply_markup=cancel_registration_inline_keyboard.tg())
        bot.register_next_step_handler(message, get_username)
        return
    elif reg.username is None:
        print(f"set default username {user.username}")
        # username = utils.tg_username_formatter(user.username)
        reg.username = utils.tg_username_without_at(user.username)
    if reg.first_name is None and user.firstName is None:
        print(f"input first_name")
        send_message(message.from_user.id, "Введите ваше имя, либо /skip",
                     reply_markup=cancel_registration_inline_keyboard.tg())
        bot.register_next_step_handler(message, get_first_name)
        return
    elif reg.first_name is None:
        print(f"set default first_name {user.first_name}")
        reg.first_name = user.first_name
    if reg.last_name is None and user.last_name is None:
        print(f"input last_name")
        send_message(message.from_user.id, "Введите вашу фамилию, либо /skip",
                     reply_markup=cancel_registration_inline_keyboard.tg())
        bot.register_next_step_handler(message, get_last_name)
        return
    elif reg.last_name is None:
        print(f"set default last_name {user.last_name}")
        reg.last_name = user.lastName
    if reg.phone is None:
        send_message(message.from_user.id, "Введите ваш номер телефона, либо /skip",
                     reply_markup=cancel_registration_inline_keyboard.tg())
        bot.register_next_step_handler(message, get_phone)
        return
    print("user creating...")
    result, error = bank_users_service.register_user(
        telegram_id=message.from_user.id,
        username=reg.username,
        first_name=reg.first_name,
        last_name=reg.last_name,
        phone=reg.phone
    )
    if error is not None:
        send_message(chat_id=message.from_user.id, text=error)
        return
    else:
        send_message(message.from_user.id, 'Вы зарегистрированы!')
        menu(message)


def fast_registration(message):
    user = message.from_user
    existed_user = bank_users_service.get_user_by_telegram_id(user.id)
    if existed_user is not None:
        send_message(message.from_user.id, "Вы уже зарегистрированы!")
        return
    reg = bank_users_service.find_registration(message)
    if reg.username is None:
        print(f"set default username {user.username}")
        # username = utils.tg_username_formatter(user.username)
        reg.username = utils.tg_username_without_at(user.username)
    if reg.first_name is None:
        print(f"set default first_name {user.first_name}")
        reg.first_name = user.first_name
    if reg.last_name is None:
        print(f"set default last_name {user.last_name}")
        reg.last_name = user.last_name
    print("user creating...")
    result, error = bank_users_service.register_user(
        telegram_id=message.from_user.id,
        username=reg.username,
        first_name=reg.first_name,
        last_name=reg.last_name,
        phone=reg.phone
    )
    if error is not None:
        send_message(chat_id=message.from_user.id, text=error)
        return
    else:
        send_message(message.from_user.id, 'Вы зарегистрированы!')
        menu(message)


def get_username(message):
    find_registration(message).username = message.text
    registration(message)


def get_first_name(message):
    if message.text != '/skip':
        find_registration(message).first_name = message.text
    else:
        find_registration(message).first_name = ''
        send_message(message.from_user.id, 'Ок, без имени(((')
    registration(message)


def get_last_name(message):
    if message.text != '/skip':
        find_registration(message).last_name = message.text
    else:
        find_registration(message).last_name = ''
        send_message(message.from_user.id, 'Ок, без фамилии(((')
    registration(message)


def get_phone(message):
    if message.text != '/skip':
        find_registration(message).phone = message.text
    else:
        find_registration(message).phone = ''
        send_message(message.from_user.id, 'Ок, без телефона(((')
    registration(message)


def cancel_reg(message):
    from bot import bot
    print("cancel pay")
    reg = find_registration(message)
    clear_registration(reg)
    bot.clear_step_handler_by_chat_id(message.chat.id)
    send_message(message.chat.id, 'Отменена регистрации(((')


def check_user_not_registered(message, bank_user_ext=None) -> bool:
    if message is not None and bank_user_ext is None:
        bank_user = bank_users_service.get_user_by_telegram_id(message.chat.id)
    elif bank_user_ext is not None:
        bank_user = bank_user_ext
    else:
        bank_user = None
    if bank_user is None:
        send_message(message.chat.id, "Вы еще не зарегистрированы! Нажмите /reg или /fast_reg")
        return True
    return False
