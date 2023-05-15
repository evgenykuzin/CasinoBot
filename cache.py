from functools import lru_cache

from models import User, GameType


class UserSession:
    session_id: int

    def __init__(self, session_id):
        self.session_id = session_id


class Registration(UserSession):
    first_name = None
    last_name = None
    phone = None
    username = None

    def __str__(self):
        return f"Registration(session=" \
               f"{self.session_id}, " \
               f"{self.first_name}, " \
               f"{self.last_name}, " \
               f"{self.phone}, " \
               f"{self.username})"


class GamePreparation(UserSession):
    name: str = None
    admin: User = None
    min_users: int = None
    max_users: int = None
    min_bet: int = None
    game_type: GameType = None

    def __str__(self):
        return f"GamePreparation(session=" \
               f"{self.session_id}, " \
               f"{self.name}, " \
               f"{self.admin}, " \
               f"{self.min_users}, " \
               f"{self.max_users}, " \
               f"{self.min_bet}," \
               f"{self.game_type})"


class JoinGameCache(UserSession):
    game_id: int = None,
    user_id: int = None,
    bet_amount: int = None

    def __str__(self):
        return f"KeyboardCache(session=" \
               f"{self.session_id}, " \
               f"{self.game_id}, " \
               f"{self.user_id}, " \
               f"{self.bet_amount}, )"


def find_registration(message) -> Registration:
    c = find_registration_cache(message.from_user.id)
    print("cache reg: " + str(c))
    return c


def find_game_preparation(message) -> GamePreparation:
    c = find_game_preparation_cache(message.chat.id)
    print("cache game: " + str(c))
    return c


def find_join_game(message) -> JoinGameCache:
    c = find_join_game_cache(message.chat.id)
    print("cache join game: " + str(c))
    return c


def clear_registration(reg: Registration):
    reg.first_name = None
    reg.last_name = None
    reg.username = None
    reg.phone = None
    reg.session_id = None


def clear_game_preparation(gp: GamePreparation):
    gp.admin = None
    gp.min_users = None
    gp.max_users = None
    gp.min_bet = None
    gp.game_type = None
    gp.session_id = None


@lru_cache
def find_registration_cache(from_user_id) -> Registration:
    return Registration(from_user_id)


@lru_cache
def find_game_preparation_cache(from_user_id) -> GamePreparation:
    return GamePreparation(from_user_id)


@lru_cache
def find_join_game_cache(from_user_id) -> JoinGameCache:
    return JoinGameCache(from_user_id)