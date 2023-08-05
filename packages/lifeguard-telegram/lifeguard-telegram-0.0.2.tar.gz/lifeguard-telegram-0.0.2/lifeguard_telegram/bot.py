import os
import sys
from functools import wraps

from lifeguard.logger import lifeguard_logger as logger
from lifeguard.settings import LIFEGUARD_DIRECTORY
from telegram.ext import CommandHandler, Updater

from lifeguard_telegram.settings import LIFEGUARD_TELEGRAM_BOT_TOKEN

CONTEXT = {"updater": None}


def init_updater():
    CONTEXT["updater"] = Updater(LIFEGUARD_TELEGRAM_BOT_TOKEN, use_context=True)

    load_bot_handlers()
    CONTEXT["updater"].start_polling()
    CONTEXT["updater"].idle()


def load_bot_handlers():
    """
    Load bot handlers from application path
    """
    sys.path.append(LIFEGUARD_DIRECTORY)

    if not os.path.exists(os.path.join(LIFEGUARD_DIRECTORY, "bot_handlers")):
        return

    for bot_handler_file in os.listdir(
        os.path.join(LIFEGUARD_DIRECTORY, "bot_handlers")
    ):
        if bot_handler_file.endswith("_bot_handler.py"):
            bot_handler_module_name = bot_handler_file.replace(".py", "")
            logger.info("loading bot handler %s", bot_handler_module_name)

            module = "bot_handlers.%s" % (bot_handler_module_name)
            if module not in sys.modules:
                __import__(module)


def bot_handler(command):
    """
    Decorator to configure a bot handler
    """

    def function_reference(decorated):
        @wraps(decorated)
        def wrapped(*args, **kwargs):
            return decorated(*args, **kwargs)

        CONTEXT["updater"].dispatcher.add_handler(CommandHandler(command, decorated))
        return wrapped

    return function_reference
