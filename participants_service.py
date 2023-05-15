from typing import Optional, Any

# from models import ContactRelationship

import requests

from backend import Response
from cache import *

base_url = "http://localhost:8081/participants"


def get_participant_by_id(participant_id) -> Optional[Any]:
    try:
        endpoint = f"{base_url}/get-id?id={participant_id}"
        response = requests.get(url=endpoint)
        rs = Response(**response.json())
        if rs.status < 0:
            return None
        return rs.data.__dict__
    except Exception as e:
        print(e)
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
        user = User.from_json(user_json)
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
