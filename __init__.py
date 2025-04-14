from aqt import gui_hooks
from .settings.settings_dialog import SettingDialog
from .config import get_config, restore_defaults, save

dialog = None


def open_config_window():
    global dialog
    dialog = SettingDialog(get_config())

    dialog.default_restored.connect(restore_defaults)
    dialog.saved.connect(save)

    dialog.show()
    dialog.activateWindow()


gui_hooks.main_window_did_init.append(open_config_window)
