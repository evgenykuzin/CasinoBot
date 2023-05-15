import utils
from models import GameType
import bank_users_service


class GameResultView:
    def __init__(self, gameName=None, resultAmounts=[], gameType=None, startedAt=None, finishedAt=None):
        self.gameName = gameName
        self.resultAmounts = resultAmounts
        self.gameType = gameType
        self.startedAt = startedAt
        self.finishedAt = finishedAt

    def __str__(self) -> str:
        results: str = ""
        import bank_users_service
        for ra in self.resultAmounts:
            userId = ra['participant']['userId']
            bu = bank_users_service.get_user_by_id(userId)
            results += f"\n\t\t{utils.tg_username_with_at(bu.username)}: {str(ra['amount'])} руб."
        return f"Игра: {self.gameName}\n" \
               f"Тип игры: {str(self.gameType)}\n" \
               f"Начато: {self.startedAt}\n" \
               f"Завершено: {self.finishedAt}\n" \
               f"Таблица результатов: {results}"


class GameView:

    def __init__(self, id: int, name: str = None, adminId: str = None,
                 minPlayers: int = None, maxPlayers: int = None, minBet: int = None,
                 gameType: GameType = None, participants=None, startedAt=None, status=None):
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

    def __str__(self) -> str:
        admin = bank_users_service.get_user_by_id(self.adminId)
        usernames = ""
        for p in self.participants:
            bu = bank_users_service.get_user_by_id(p["userId"])
            usernames += f"\n\t\t{utils.tg_username_with_at(bu.username)}. Ставка: {p['betAmount']}"
        return f"Название: {self.name} \n" \
               f"Админ: {admin if admin is not None else 'None'} \n" \
               f"Тип игры: {self.gameType} \n" \
               f"Мин. игроков: {self.minPlayers} \n" \
               f"Макс. игроков: {self.maxPlayers} \n" \
               f"Мин. ставка: {self.minBet} \n" \
               f"Игроки: {usernames}"
