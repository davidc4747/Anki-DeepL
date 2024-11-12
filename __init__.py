from aqt import gui_hooks, mw
from .settings.dialog import create_dialog


def handle_defaults():
    default_config = mw.addonManager.addonConfigDefaults(__name__)
    mw.addonManager.writeConfig(__name__, default_config)


def handle_save():
    mw.addonManager.writeConfig(__name__, "{ 'configursation': '!!!!' }")


def open_config_window():
    global dialog
    dialog = create_dialog(handle_defaults, handle_save)
    dialog.show()
    dialog.activateWindow()


gui_hooks.main_window_did_init.append(open_config_window)
mw.addonManager.setConfigAction(__name__, open_config_window)
