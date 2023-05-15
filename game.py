import bank_users_service
import game_service
import models
import utils
from bot_utils import send_message
from cache import find_game_preparation, find_join_game, clear_game_preparation
from models import GameType
from registration import check_user_not_registered


def create_game(message):
    from bot_keyboards import prepare_game_creation_inline_keyboard
    from bot import bot
    bu = bank_users_service.get_user_by_telegram_id(message.from_user.id)
    if check_user_not_registered(message, bank_user_ext=bu):
        return
    find_game_preparation(message).admin = bu
    send_message(chat_id=message.from_user.id, text='Введите название игры',
                 reply_markup=prepare_game_creation_inline_keyboard.tg())
    bot.register_next_step_handler(message, create_game_name)


def create_game_name(message):
    from bot_keyboards import choose_game_type_keyboard
    from bot import bot
    find_game_preparation(message).name = message.text
    send_message(chat_id=message.from_user.id, text='Выберете тип игры из списка (откройте клавиатуру)',
                 reply_markup=choose_game_type_keyboard.tg())
    #bot.register_next_step_handler(message, create_game_game_type)


def create_game_game_type(message):
    from bot_keyboards import prepare_game_creation_inline_keyboard
    from bot import bot
    find_game_preparation(message).game_type = GameType.to_enum(message.text)
    send_message(chat_id=message.from_user.id, text='Введите минимальное число участников',
                 reply_markup=prepare_game_creation_inline_keyboard.tg())
    bot.register_next_step_handler(message, create_game_min_players)


def create_game_min_players(message):
    from bot_keyboards import prepare_game_creation_inline_keyboard
    from bot import bot
    gp = find_game_preparation(message)
    gp.min_users = message.text
    gp.max_users = 10
    send_message(chat_id=message.from_user.id, text='Введите минимальную сумму ставки',
                 reply_markup=prepare_game_creation_inline_keyboard.tg())
    bot.register_next_step_handler(message, create_game_min_bet)


def create_game_min_bet(message):
    from bot_keyboards import game_creation_inline
    from bot import bot
    gp = find_game_preparation(message)
    gp.min_bet = message.text
    send_message(chat_id=message.from_user.id, text='Теперь нажмите "Создать"',
                 reply_markup=game_creation_inline.tg())
    bot.clear_step_handler_by_chat_id(message.from_user.id)


def confirm_create_game(message):
    from bot_keyboards import my_game_inline_keyboard
    from bot import bot
    # if check_user_not_registered(message):
    #     return
    gp = find_game_preparation(message)
    response = game_service.create_game(gp)
    game_id = int(response.data)
    send_message(chat_id=message.chat.id, text='Игра создана!',
                 reply_markup=my_game_inline_keyboard(game_id).tg())
    bot.clear_step_handler_by_chat_id(message.chat.id)


def cancel_game_creation(message):
    from bot_keyboards import MAIN_KEYBOARD
    from bot import bot
    clear_game_preparation(find_game_preparation(message))
    bot.clear_step_handler_by_chat_id(message.chat.id)
    send_message(chat_id=message.chat.id, text='Отмена создания игры', reply_markup=MAIN_KEYBOARD.tg())


def default_game_creation(message):
    from bot_keyboards import my_game_inline_keyboard
    from bot import bot
    gp = find_game_preparation(message)
    gp.name = "Game"
    bu = bank_users_service.get_user_by_telegram_id(message.chat.id)
    print(f"bu = {bu}")
    gp.admin = bu
    gp.min_bet = 100
    gp.min_users = 1
    gp.max_users = 10
    gp.game_type = GameType.ONE_WINNER
    response = game_service.create_game(gp)
    game_id = int(response.data)
    send_message(chat_id=message.chat.id, text='Игра создана',
                 reply_markup=my_game_inline_keyboard(game_id).tg())
    bot.clear_step_handler_by_chat_id(message.chat.id)


# GAME


def my_games(message):
    from bot_keyboards import my_game_inline_keyboard
    games, error = game_service.get_my_games(bank_users_service.get_user_by_telegram_id(message.from_user.id).id)
    if error is not None:
        send_message(chat_id=message.from_user.id, text=error)
    if len(games) == 0:
        send_message(chat_id=message.from_user.id, text="Список ваших игр пока пуст")
    gm: models.Game
    for gm in games:
        rm = my_game_inline_keyboard(gm.id).tg() \
            if str(gm.status) == 'CREATED' else None
        send_message(chat_id=message.from_user.id, text=str(gm),
                     reply_markup=rm)


def my_active_games(message):
    from bot_keyboards import leave_game_inline_keyboard
    games, error = game_service.get_active_games(bank_users_service.get_user_by_telegram_id(message.from_user.id).id)
    if error is not None:
        send_message(chat_id=message.from_user.id, text=error)
    if len(games) == 0:
        send_message(chat_id=message.from_user.id, text="Список активных игр пока пуст")
    gm: models.Game
    for gm in games:
        send_message(chat_id=message.from_user.id, text=str(gm),
                     reply_markup=leave_game_inline_keyboard(gm.id).tg())


def find_game(message):
    from bot_keyboards import join_game_inline_keyboard
    games, error = game_service.get_all_games()
    if error is not None:
        send_message(chat_id=message.from_user.id, text=error)
    if len(games) == 0:
        send_message(chat_id=message.from_user.id, text="Список игр пока пуст")
    gm: models.Game
    for gm in games:
        send_message(chat_id=message.from_user.id, text=str(gm),
                     reply_markup=join_game_inline_keyboard(gm.id).tg())


def join_game(message, data: str):
    from bot import bot
    game_id = int(utils.callback_param(data))
    jg = find_join_game(message)
    jg.game_id = game_id
    bu = bank_users_service.get_user_by_telegram_id(message.chat.id)
    if check_user_not_registered(message, bank_user_ext=bu):
        return
    jg.user_id = bu.id
    game: models.Game = game_service.get(game_id)
    for p in game.participants:
        if bu.id == p["userId"]:
            send_message(message.chat.id, f"Вы уже в игре!")
            return
    send_message(message.chat.id, f"Укажите свою ставку. Минимальная ставка {game.minBet}")
    bot.register_next_step_handler(message, join_game_amount)


def join_game_amount(message):
    from bot_keyboards import cancel_join_game_inline_keyboard
    from bot import bot
    amountstr: str = message.text
    amount: int = int(amountstr)
    if not amountstr.isnumeric() \
            or amount <= 0 \
            or amount > bank_users_service.get_user_by_telegram_id(message.from_user.id).balance:
        send_message(message.from_user.id, "Сумма некорректна или недостаточно средств. Отправьте сумму еще раз.",
                     reply_markup=cancel_join_game_inline_keyboard.tg())
        bot.register_next_step_handler(message, join_game_amount)
        return
    jg = find_join_game(message)
    response, error = game_service.join_game(jg.game_id, amount, jg.user_id)
    if error is not None:
        send_message(chat_id=message.from_user.id, text=error)
        return
    send_message(message.from_user.id, "Вы присоединились к игре")
    game = game_service.get(jg.game_id)
    print(game)
    admin = bank_users_service.get_user_by_id(game.adminId)
    participant = bank_users_service.get_user_by_telegram_id(message.from_user.id)
    send_message(chat_id=admin.telegramId, text=f"{participant.username} присоединился к вашей игре")


def leave_game(message, data: str):
    from bot_keyboards import cancel_cashout_inline_keyboard
    from bot import bot
    game_id = int(utils.callback_param(data))
    bu = bank_users_service.get_user_by_telegram_id(message.chat.id)
    response, error = game_service.leave_game(game_id, bu.id)
    if error is not None:
        send_message(chat_id=message.chat.id, text=error)
        return
    print(response)
    send_message(message.chat.id, "Вы покинули игру")


def start_game(message, data: str):
    send_message(message.chat.id, f"Игра началась!")
    game_result: models.GameResult
    game_result, error = game_service.start_game(int(utils.callback_param(data)), message.from_user.id)
    if error is not None:
        send_message(chat_id=message.chat.id, text=error)
        return
    from views import GameResultView
    game: models.Game = game_service.get(game_result.gameId)
    game_result_view = GameResultView(
        game.name,
        game_result.resultAmounts,
        game_result.gameType,
        game_result.startedAt,
        game_result.finishedAt
    )
    send_message(message.chat.id, f"Результаты игры:\n\n{str(game_result_view)}")
    participants = bank_users_service.get_user_of_game(game.id)
    for bu in participants:
        if bu.telegramId == message.chat.id:
            continue
        send_message(chat_id=bu.telegramId, text=f"Результаты игры:\n\n{str(game_result_view)}")


def cancel_join(message):
    send_message(message.chat.id, "Отмена входа в игру")
    from bot import bot
    bot.clear_step_handler_by_chat_id(message.chat.id)
