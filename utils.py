from typing import Optional


def is_blank(s: str):
    return s is None or s == '' or s.isspace()


def tg_username_with_at(username: str):
    return username if username.startswith('@') else '@' + username


def tg_username_without_at(username: str):
    return username.replace('@', '') if username.startswith('@') else username


def callback_param(data: str) -> Optional[str]:
    try:
        return data.split(":")[1]
    except Exception as e:
        print(e)
        return None
