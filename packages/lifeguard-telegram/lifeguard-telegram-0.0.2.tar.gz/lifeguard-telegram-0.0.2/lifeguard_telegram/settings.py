"""
Lifeguard Telegram Settings
"""
from lifeguard.settings import SettingsManager

SETTINGS_MANAGER = SettingsManager(
    {
        "LIFEGUARD_TELEGRAM_BOT_TOKEN": {
            "default": "",
            "description": "Telegram bot token",
        },
    }
)

LIFEGUARD_TELEGRAM_BOT_TOKEN = SETTINGS_MANAGER.read_value("LIFEGUARD_TELEGRAM_BOT_TOKEN")
