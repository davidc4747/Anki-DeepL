from typing import Callable
from dataclasses import dataclass
from aqt import mw

addon_name = mw.addonManager.addonFromModule(__name__)


@dataclass
class TransaltionConfig:
    name: str
    source_field: str
    target_field: str


@dataclass
class UserConfig:
    source_lang: str
    target_lang: str
    translations: list[TransaltionConfig]


def get_config() -> UserConfig:
    config = UserConfig(**mw.addonManager.getConfig(addon_name))
    config.translations = (
        [TransaltionConfig(**t) for t in config.translations]
        if config.translations
        else []
    )
    return config 


def restore_defaults() -> None:
    default_config = mw.addonManager.addonConfigDefaults(addon_name)
    mw.addonManager.writeConfig(addon_name, default_config if default_config else {})


def save(config: UserConfig) -> None:
    mw.addonManager.writeConfig(addon_name, config)


def set_config_action(func: Callable) -> None:
    mw.addonManager.setConfigAction(addon_name, func)
