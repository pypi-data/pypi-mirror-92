import argparse

from loguru import logger

from nebo_bot.core import BotCore


def run():
    parser = argparse.ArgumentParser(description='Nebo bot')
    parser.add_argument('login', type=str, action='store',
                        help='Login')
    parser.add_argument('password', type=str, action='store',
                        help='password')

    args = parser.parse_args()
    login = args.login
    password = args.password
    bot = BotCore()

    if bot.login(login, password):
        bot.city.work.run_invite()
    else:
        logger.error('Fail login')
