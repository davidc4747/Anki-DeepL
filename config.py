from typing import Callable
from aqt import mw

addon_name = mw.addonManager.addonFromModule(__name__)


def get_config() -> dict:
    return mw.addonManager.getConfig(addon_name)


def restore_defaults() -> None:
    default_config = mw.addonManager.addonConfigDefaults(addon_name)
    mw.addonManager.writeConfig(addon_name, default_config if default_config else {})


def save(config: dict) -> None:
    mw.addonManager.writeConfig(addon_name, config)


def set_config_action(func: Callable) -> None:
    mw.addonManager.setConfigAction(addon_name, func)
