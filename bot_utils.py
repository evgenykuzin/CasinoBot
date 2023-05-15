def send_message(chat_id=None, text=None, reply_markup=None):
    if reply_markup is None:
        from bot_keyboards import MAIN_KEYBOARD
        reply_markup = MAIN_KEYBOARD.tg()
    print(f"Bot send to {chat_id} '{text}' \n keyboard: {reply_markup.to_json()}")
    from bot import bot
    return bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


def menu(message):
    from bot_keyboards import MAIN_KEYBOARD
    send_message(
        message.from_user.id,
        text='Главное меню',
        reply_markup=MAIN_KEYBOARD.tg()
    )
