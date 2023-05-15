class KeyboardsHolder:
    def __init__(self) -> None:
        super().__init__()
        from balance import get_balance, get_money, cashout, \
            cancel_get_money, cancel_cashout
        from bot_utils import menu
        from game import find_game, create_game, cancel_game_creation, \
            confirm_create_game, join_game, start_game, \
            default_game_creation, my_games, cancel_join, \
            my_active_games, leave_game
        from registration import cancel_reg

        self.keyboards = {
            "MAIN_KEYBOARD": create_keyboard({
                "Найти игру": lambda m: find_game(m),
                "Мои созданные игры": lambda m: my_games(m),
                "Мои активные игры": lambda m: my_active_games(m),
                "Создать игру": lambda m: create_game(m),
                "Баланс": lambda m: get_balance(m),
            }),
            "BALANCE_KEYBOARD": create_keyboard({
                "Пополнить баланс": lambda m: get_money(m),
                "Вывести бабки": lambda m: cashout(m),
                "Назад": lambda m: menu(m)
            }),
            "game_creation_inline": create_inline_keyboard({
                "Отмена:a": {"cancel_gp": (lambda m, d: cancel_game_creation(m))},
                "Создать": {"confirm_gp": lambda m, d: confirm_create_game(m)}
            }),
            "prepare_game_creation_inline_keyboard": create_inline_keyboard({
                "Отмена:b": {"cancel_gp": lambda m, d: cancel_game_creation(m)},
                "Дефолт": {"default_gp": lambda m, d: default_game_creation(m)}
            }),
            "cancel_registration_inline_keyboard": create_inline_keyboard({
                "Отмена:c": {"cancel_reg": lambda m, d: cancel_reg(m)},
            }),
            "cancel_get_money_inline_keyboard": create_inline_keyboard({
                "Отмена:d": {"cancel_get_money": lambda m, d: cancel_get_money(m)},
            }),
            "cancel_cashout_inline_keyboard": create_inline_keyboard({
                "Отмена:e": {"cancel_cashout": lambda m, d: cancel_cashout(m)},
            }),
            "cancel_join_game_inline_keyboard": create_inline_keyboard({
                "Отмена:f": {"cancel_join": lambda m, d: cancel_join(m)},
                "Пополнить баланс": {"update_balance": lambda m, d: get_money(m)}
            }),
            "join_game_inline_keyboard": create_inline_keyboard({
                "Присоединиться": {"join_game": lambda m, d: join_game(m, d)},
            }),
            "my_game_inline_keyboard": create_inline_keyboard({
                "Старт": {"start_game": lambda m, d: start_game(m, d)},
            }),
            "leave_game_inline_keyboard": create_inline_keyboard({
                "Покинуть": {"leave_game": lambda m, d: leave_game(m, d)},
            }),
            "choose_game_type_keyboard": create_choose_game_type_keyboard({
                "Отмена:g": lambda m: cancel_game_creation(m),
                "Назад": lambda m: menu(m)
            })
        }


from telebot import types
from telebot.types import JsonSerializable


class Keyboard:
    def __init__(self, buttons: [], inline: bool = False):
        self.buttons = buttons
        self.inline = inline

    def tg(self) -> JsonSerializable:
        keyboard: JsonSerializable
        if self.inline:
            keyboard = types.InlineKeyboardMarkup()
        else:
            keyboard = types.ReplyKeyboardMarkup()
        btn: Button
        for btn in self.buttons:
            if self.inline:
                tgbtn = types.InlineKeyboardButton(text=btn.name, callback_data=btn.callback)
            else:
                tgbtn = types.KeyboardButton(text=btn.name)
            keyboard.add(tgbtn)
        return keyboard

    def __str__(self) -> str:
        return f'Keyboard(buttons={self.buttons})'


class Button:
    def __init__(self, name: str, handle_message_func=None, callback: str = None):
        self.name = name
        self.handle_message_func = handle_message_func
        self.callback = callback

    def __str__(self) -> str:
        return f'Button(name={self.name})'


def create_keyboard(buttons: dict):
    btns = []
    k: str
    for k, f in buttons.items():
        btns.append(Button(k, handle_message_func=f))
    return Keyboard(btns)


def create_inline_keyboard(buttons: dict):
    btns = []
    k: str
    v: dict
    for k, v in buttons.items():
        cb = list(dict(v).keys())[0]
        f = list(dict(v).values())[0]
        btns.append(Button(k, callback=cb, handle_message_func=f))
    return Keyboard(btns, True)


def create_choose_game_type_keyboard(buttons: dict):
    from models import GameType
    game_type: GameType
    btns = []
    for game_type in GameType:
        from game import create_game_game_type
        btn = Button(name=game_type.russian(), handle_message_func=create_game_game_type)
        btns.append(btn)
    k: str
    for k, f in buttons.items():
        btns.append(Button(k, handle_message_func=f))
    return Keyboard(btns)


keyboards_holder = KeyboardsHolder()
keyboards = keyboards_holder.keyboards
MAIN_KEYBOARD = keyboards["MAIN_KEYBOARD"]
BALANCE_KEYBOARD = keyboards["BALANCE_KEYBOARD"]
game_creation_inline = keyboards["game_creation_inline"]
prepare_game_creation_inline_keyboard = keyboards["prepare_game_creation_inline_keyboard"]
cancel_registration_inline_keyboard = keyboards["cancel_registration_inline_keyboard"]
cancel_get_money_inline_keyboard = keyboards["cancel_get_money_inline_keyboard"]
cancel_cashout_inline_keyboard = keyboards["cancel_cashout_inline_keyboard"]
cancel_join_game_inline_keyboard = keyboards["cancel_join_game_inline_keyboard"]
choose_game_type_keyboard = keyboards["choose_game_type_keyboard"]


def join_game_inline_keyboard(game_id: int) -> Keyboard:
    return get_inline_keyboard_with_id(game_id, "join_game_inline_keyboard")


def my_game_inline_keyboard(game_id: int) -> Keyboard:
    return get_inline_keyboard_with_id(game_id, "my_game_inline_keyboard")


def leave_game_inline_keyboard(game_id: int) -> Keyboard:
    return get_inline_keyboard_with_id(game_id, "leave_game_inline_keyboard")


def get_inline_keyboard_with_id(id: int, keyboard_name: str) -> Keyboard:
    inline_keyboard: Keyboard = Keyboard(**keyboards[keyboard_name].__dict__)
    buttons = [*inline_keyboard.buttons]
    btn: Button = Button(**buttons[0].__dict__)
    btn.callback = f"{btn.callback}:{id}"
    buttons[0] = btn
    inline_keyboard.buttons = buttons
    return inline_keyboard
