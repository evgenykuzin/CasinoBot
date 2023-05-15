from typing import Optional

# from models import ContactRelationship

import requests

from backend import Response
from cache import *

base_url = "http://localhost:8081/users"


def register_user(
        telegram_id: int,
        username='',
        first_name='',
        last_name='',
        phone=''
):
    endpoint = f"{base_url}/registration"
    headers = {'Content-type': 'application/json'}
    data = {
        "telegramId": telegram_id,
        "username": username,
        "firstName": first_name,
        "secondName": last_name,
        "balance": 100,
        "credit": 0,
        "phone": phone
    }
    response = requests.post(url=endpoint, headers=headers, json=data)
    rs = Response(**response.json())
    if rs.status < 0:
        return None, rs.data
    return True, None


def get_user_by_id(bank_user_id) -> Optional[User]:
    try:
        endpoint = f"{base_url}/get-id?id={bank_user_id}"
        response = requests.get(url=endpoint)
        rs = Response(**response.json())
        if rs.status < 0:
            return None
        return User(**rs.data)
    except Exception as e:
        print(e)
        # return BankUser(bank_user_id=1, telegram_id=0, username='jekajops', phone='89523663611', balance=100, credit=0, deleted=False)
        return None


def get_user_by_username(username) -> Optional[User]:
    try:
        endpoint = f"{base_url}/get-username?username={username}"
        response = requests.get(url=endpoint)
        rs = Response(**response.json())
        if rs.status < 0:
            return None
        return User(**rs.data)
    except Exception as e:
        print(e)
        # return BankUser(bank_user_id=1, telegram_id=0, username='jekajops', phone='89523663611', balance=100, credit=0, deleted=False)
        return None


#@lru_cache
def get_user_by_telegram_id(telegram_id) -> Optional[User]:
    try:
        endpoint = f"{base_url}/get-tgid?telegramId={telegram_id}"
        response = requests.get(url=endpoint)
        print(response.json())
        rs = Response(**response.json())
        print(rs)
        if int(rs.status) < 0:
            print("status problem")
            print(rs.status)
            return None
        print("wtf")
        return User(**rs.data)
    except Exception as e:
        print("ex problem")
        print(e)
        # return BankUser(bank_user_id=1, telegram_id=0, username='jekajops', phone='89523663611', balance=100, credit=0, deleted=False)
        return None


def get_user_of_game(game_id):
    try:
        endpoint = f"{base_url}/game-participants?gameId={game_id}"
        response = requests.get(url=endpoint)
        rs = Response(**response.json())
        if rs.status < 0:
            return None
        users = []
        for user_json in rs.data:
            user = User(**user_json)
            users.append(user)
        return users
    except Exception as e:
        print(e)
        # return BankUser(bank_user_id=1, telegram_id=0, username='jekajops', phone='89523663611', balance=100, credit=0, deleted=False)
        return []

# def get_account_of_user(id: int) -> Account:
#     try:
#         return Account.get_by_id(id)
#     except Exception as e:
#         print(e)
#         return Account(bank_user=get_user_by_telegram_id(id), balance=100, credit=0, deleted=False)


def get_all_bank_users():
    endpoint = f"{base_url}/get-all"
    response = requests.get(url=endpoint)
    rs = Response(**response.json())
    if rs.status < 0:
        return None, str(rs.data)
    # print([f'Account(bank_user: {acc.bank_user}, balance: {acc.balance}, credit: {acc.credit})' for acc in Account.select()])
    users = []
    for user_json in rs.data:
        user = User(**user_json)
        users.append(user)
    return users, None


def get_money(telegram_id, amount):
    endpoint = f"{base_url}/update-balance/{telegram_id}/{amount}"
    response = requests.get(url=endpoint)
    rs = Response(**response.json())
    if rs.status < 0:
        return None, str(rs.data)
    return True, None
    # bu = get_user_by_telegram_id(telegram_id)
    # cbalance = int(bu.balance)
    # bu.balance = str(cbalance + int(amount))
    #
    # bu.save()

# def add_to_contacts(from_user: BankUser, to_user: BankUser):
#     ContactRelationship.create(from_user=from_user, to_user=to_user)
#
#
# def get_contacts_of_user(bank_user: BankUser):
#     return [contact.to_user
#             for contact in ContactRelationship.get(
#             ContactRelationship.from_user.bank_user_id == bank_user.bank_user_id
#         )]
