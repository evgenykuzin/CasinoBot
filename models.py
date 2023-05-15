import json
from enum import Enum


class GameType(Enum):
    ONE_WINNER = "ONE_WINNER"
    TOP3_WINNERS = "TOP3_WINNERS"
    RANDOM_WINNERS = "RANDOM_WINNERS"

    def russian(self):
        if self == GameType.ONE_WINNER:
            return "Царь горы"
        elif self == GameType.TOP3_WINNERS:
            return "Турнир"
        elif self == GameType.RANDOM_WINNERS:
            return "Хаос"

    @staticmethod
    def to_enum(russian_name):
        if russian_name == "Царь горы":
            return GameType.ONE_WINNER
        elif russian_name == "Турнир":
            return GameType.TOP3_WINNERS
        elif russian_name == "Хаос":
            return GameType.RANDOM_WINNERS

    def __str__(self):
        return self.value


class User:

    def __init__(self, id=None, telegramId=None, firstName=None, lastName=None, username=None, phone=None, balance=0, credit=0, deleted=False, timestamp=None):
        self.id = id
        self.telegramId = telegramId
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.phone = phone
        self.balance = balance
        self.credit = credit
        self.deleted = deleted
        self.timestamp = timestamp

    def __str__(self) -> str:
        return json.dumps({
            'id': self.id,
            'telegramId': self.telegramId,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'username': self.username,
            'phone': self.phone,
            'balance': self.balance,
            'credit': self.credit,
            'deleted': self.deleted,
            'timestamp': self.timestamp
        })


class Game:

    def __init__(self, id: int, name: str = None, adminId: str = None,
                 minPlayers: int = None, maxPlayers: int = None, minBet: int = None,
                 gameType: GameType = None, participants=None, startedAt=None, status: str=None):
        self.id = id
        self.name = name
        self.adminId = adminId
        self.minPlayers = minPlayers
        self.maxPlayers = maxPlayers
        self.minBet = minBet
        self.gameType = gameType
        self.participants = participants
        self.startedAt = startedAt
        self.status = status

    def to_json(self) -> str:
        game_dict = {
            'id': self.id,
            'name': self.name,
            'adminId': self.adminId if self.adminId else None,
            'minPlayers': self.minPlayers,
            'maxPlayers': self.maxPlayers,
            'minBet': self.minBet,
            'gameType': self.gameType.to_json(),
            'status': self.status
        }
        return json.dumps(game_dict)

    def __str__(self) -> str:
        import bank_users_service
        admin = bank_users_service.get_user_by_id(self.adminId)
        total_amount: float = 0.0
        usernames = ""
        for p in self.participants:
            bet_amount = p['betAmount']
            total_amount += bet_amount
            bu = bank_users_service.get_user_by_id(p["userId"])
            import utils
            usernames += f"\n\t\t{utils.tg_username_with_at(bu.username)}. Ставка: {bet_amount}"
        return f"Название: {self.name} \n" \
               f"Статус: {self.status} \n" \
               f"Админ: {admin.username if admin is not None else 'None'} \n" \
               f"Тип игры: {self.gameType} \n" \
               f"Мин. игроков: {self.minPlayers} \n" \
               f"Макс. игроков: {self.maxPlayers} \n" \
               f"Мин. ставка: {self.minBet} \n" \
               f"В банке: {total_amount} \n" \
               f"Игроки: {usernames}"


class GameResult:
    id: int = None,
    gameId = None,
    resultAmounts = []
    gameType: GameType = None,
    startedAt: str = None,
    finishedAt: str = None

    def __init__(self, id=None, gameId=None, resultAmounts=[], gameType=None, startedAt=None, finishedAt=None):
        self.id = id
        self.gameId = gameId
        self.resultAmounts = resultAmounts
        self.gameType = gameType
        self.startedAt = startedAt
        self.finishedAt = finishedAt

    def to_json(self):
        return json.dumps({
            'id': self.id,
            'gameId': self.gameId,
            'resultAmounts': self.resultAmounts,
            'gameType': str(self.gameType) if self.gameType else None,
            'startedAt': self.startedAt,
            'finishedAt': self.finishedAt,
        })

    def __str__(self) -> str:
        return self.to_json()