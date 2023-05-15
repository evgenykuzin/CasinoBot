from abc import ABC

from telebot.types import JsonSerializable


class Response(JsonSerializable, ABC):

    def __init__(self, status, data) -> None:
        super().__init__()
        self.status: int = status
        self.data: dict = data

    def __str__(self):
        return f"{{\"status\": \"{self.status}\", \"data\": {self.data}}}"






