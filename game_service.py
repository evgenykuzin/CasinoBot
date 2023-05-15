from typing import Union

import requests
import typing

from backend import Response
from cache import *
from models import Game, GameResult

base_url = "http://localhost:8081/games"


def create_game(game: GamePreparation):
    endpoint = f"{base_url}/create-game"
    headers = {'Content-type': 'application/json'}
    data = {
        "name": game.name,
        "adminId": game.admin.id,
        "minPlayers": game.min_users,
        "maxPlayers": game.max_users,
        "minBet": game.min_bet,
        "gameType": str(game.game_type)
    }
    print(data)
    response = requests.post(url=endpoint, headers=headers, json=data)
    return Response(**response.json())


def get_all_games() -> Union[typing.Any, str]:
    endpoint = f"{base_url}/get-all"
    response = requests.get(url=endpoint)
    rs = Response(**response.json())
    if rs.status < 0:
        return None, str(rs.data)
    games = []
    for game_json in rs.data:
        print(game_json)
        game = Game(**game_json)
        games.append(game)
    return games, None


def get_my_games(user_id) -> Union[typing.Any, str]:
    endpoint = f"{base_url}/get-my?userId={user_id}"
    response = requests.get(url=endpoint)
    rs = Response(**response.json())
    if rs.status < 0:
        return None, str(rs.data)
    games = []
    for game_json in rs.data:
        print(game_json)
        game = Game(**game_json)
        games.append(game)
    return games, None


def get_active_games(user_id) -> Union[typing.Any, str]:
    endpoint = f"{base_url}/get-active?userId={user_id}"
    response = requests.get(url=endpoint)
    rs = Response(**response.json())
    if rs.status < 0:
        return None, str(rs.data)
    games = []
    for game_json in rs.data:
        print(game_json)
        game = Game(**game_json)
        games.append(game)
    return games, None


def get(game_id: int) -> typing.Any:
    endpoint = f"{base_url}/get?gameId={game_id}"
    response = requests.get(url=endpoint)
    rs = Response(**response.json())
    if rs.status < 0:
        return None
    return Game(**rs.data)


def join_game(game_id: int, bet_amount: int, user_id: int) -> Union[typing.Any, str]:
    endpoint = f"{base_url}/join-game"
    headers = {'Content-type': 'application/json'}
    data = {"gameId": game_id, "betAmount": bet_amount, "userId": user_id}
    response = requests.post(url=endpoint, headers=headers, json=data)
    rs = Response(**response.json())
    if rs.status < 0:
        return None, str(rs.data)
    return True, None


def leave_game(game_id: int, user_id: int) -> Union[typing.Any, str]:
    endpoint = f"{base_url}/leave-game?gameId={game_id}&userId={user_id}"
    response = requests.get(url=endpoint)
    rs = Response(**response.json())
    if rs.status < 0:
        return None, str(rs.data)
    return True, None


def start_game(game_id: int, telegram_id: int) -> Union[typing.Any, str]:
    endpoint = f"{base_url}/start-game?gameId={game_id}"
    response = requests.get(url=endpoint)
    rs = Response(**response.json())
    if rs.status < 0:
        return None, str(rs.data)
    endpoint = f"{base_url}/results?gameId={game_id}"
    response = requests.get(url=endpoint)
    rs = Response(**response.json())
    if rs.status < 0:
        return None, str(rs.data)
    print(response)
    game_result: GameResult = GameResult(**rs.data)
    print(game_result)
    return game_result, None


def __make_dictionary__(keys, values):
    """
    Функция принимает два списка: keys и values.
    Создает словарь, где каждому элементу списка keys соответствует элемент из списка values.
    Возвращает полученный словарь.
    """
    dictionary = {}
    for i in range(len(keys)):
        dictionary[keys[i]] = values[i]
    return dictionary
