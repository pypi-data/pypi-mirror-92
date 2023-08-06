from loguru import logger

from nebo_bot.core import BotCore


def run(login, password):
    bot = BotCore()
    if bot.login(login, password):
        bot.run_works()
    else:
        logger.error('Fail login')
