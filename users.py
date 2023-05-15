import bank_users_service
import utils
from bot_utils import send_message


def get_all_users(message):
    bank_users = bank_users_service.get_all_bank_users()
    for bu in bank_users:
        msg = f'Имя: {bu.firstName} {bu.lastName};\n Никнейм: {utils.tg_username_with_at(bu.username)};'
        send_message(message.from_user.id, msg)