import telebot

import bank_users_service
import botenv
from bot_utils import send_message, menu
from registration import registration, fast_registration

bot = telebot.TeleBot(token=botenv.get_token())
print("Start bot...")


def run():
    bot.infinity_polling()


@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text == '/start':
        send_message(message.from_user.id, "Добро пожаловать! Зарегистрируйся /reg "
                                           "или зарегистрируйся быстро /fast_reg")
        registration(message)
    else:
        bu = bank_users_service.get_user_by_telegram_id(message.from_user.id)
        if bu is not None:
            print(f"Пишет ("
                  f"id:{bu.id}; "
                  f"name:{bu.firstName} {bu.lastName}; "
                  f"tg_username:{bu.username}; "
                  f"tg_id:{bu.telegramId}; "
                  f"balance:{bu.balance})")
        else:
            print("from_id: " + str(message.from_user.id))
        print(message.text)
        if message.text == '/reg':
            registration(message)
        elif message.text == '/fast_reg':
            fast_registration(message)
        elif message.text == '/menu':
            menu(message)
        else:
            from bot_keyboards import keyboards
            for keyboard in keyboards.values():
                for btn in keyboard.buttons:
                    if btn.name == message.text:
                        handle_func = btn.handle_message_func
                        if handle_func is not None:
                            handle_func(message)
                            return
            send_message(chat_id=message.from_user.id, text="Откройте клавиатуру или напишите /menu")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    from bot_keyboards import keyboards
    for keyboard in keyboards.values():
        for btn in keyboard.buttons:
            if btn.callback == call.data or call.data.__contains__(str(btn.callback).split(":")[0]):
                handle_func = btn.handle_message_func
                if handle_func is not None:
                    handle_func(call.message, call.data)
                    return
