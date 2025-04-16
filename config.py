from typing import Callable, Any
from dataclasses import dataclass, field, asdict
from aqt import mw

addon_name = mw.addonManager.addonFromModule(__name__)


@dataclass
class TranslationConfig:
    model_name: str
    source_field: str
    target_field: str


@dataclass
class UserConfig:
    deepl_auth_key: str
    source_lang: str
    target_lang: str
    translations: dict[str, TranslationConfig] = field(default_factory=dict)


def get_config() -> UserConfig:
    config = mw.addonManager.getConfig(addon_name)
    return UserConfig(
        deepl_auth_key=config.get("deepl_auth_key"),
        source_lang=config.get("source_lang"),
        target_lang=config.get("target_lang"),
        translations={
            key: TranslationConfig(**value)
            for key, value in config.get("translations").items()
        },
    )


def save(config: UserConfig) -> None:
    mw.addonManager.writeConfig(
        addon_name,
        {
            "deepl_auth_key": config.deepl_auth_key,
            "source_lang": config.source_lang,
            "target_lang": config.target_lang,
            "translations": {
                key: asdict(value) for key, value in config.translations.items()
            },
        },
    )


def restore_defaults() -> None:
    default_config = mw.addonManager.addonConfigDefaults(addon_name)
    mw.addonManager.writeConfig(addon_name, default_config if default_config else {})


def set_config_action(func: Callable) -> None:
    mw.addonManager.setConfigAction(addon_name, func)
