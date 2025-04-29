from aqt import gui_hooks, mw
from aqt.qt import QAction
from aqt.operations import QueryOp
from aqt.operations.note import update_notes
from anki.notes import Note
from .settings.settings_dialog import SettingDialog
from .config import get_config, restore_defaults, save, set_config_action, UserConfig
from .deepl import translate_phrases, deepl_usage


# Settings Window
#########################################################################
dialog = None
action = QAction("AnkiDeepL Options...", mw)


@set_config_action
@action.triggered.connect
def open_settings_window() -> None:
    global dialog
    dialog = SettingDialog(get_config())

    dialog.default_restored.connect(restore_defaults)
    dialog.saved.connect(save)

    dialog.show()
    dialog.activateWindow()


mw.form.menuTools.addAction(action)


# Translate on Sync
#########################################################################


@gui_hooks.sync_will_start.append
def generate_missing_fields() -> None:
    # Read User config
    config = get_config()

    # Select notes based on config
    search = " or ".join(
        [
            f'("note:{t.model_name}" "{t.source_field}:_*" "{t.target_field}:")'
            for model_name, t in config.translations.items()
        ]
    )

    # Check if the DeepL Limit has been reached
    usage = deepl_usage(config.deepl_auth_key)
    char_count = usage.character_count
    notes: list[Note] = []
    for nid in mw.col.find_notes(search):
        note = mw.col.get_note(nid)

        translation_config = config.translations.get(note.note_type().get("name"))
        if translation_config:
            field_len = len(note[translation_config.source_field])
            if char_count + field_len < usage.character_limit:
                notes.append(note)
                char_count += field_len

    # Break it up into multiple translation requests for DeepL
    print(len(notes), char_count)
    CHUNK_SIZE = 500
    for i in range(0, len(notes), CHUNK_SIZE):
        translate_notes(config, notes[i : i + CHUNK_SIZE])


def translate_notes(config: UserConfig, notes: list[Note]) -> None:
    phrases = []
    for note in notes:
        translation_config = config.translations.get(note.note_type().get("name"))
        if translation_config:
            phrases.append(note[translation_config.source_field])

    def on_success(english_translations):
        # Update the Note Fields
        for i, note in enumerate(notes):
            translation_config = config.translations.get(note.note_type().get("name"))
            if translation_config:
                note[translation_config.target_field] = english_translations[i]
        update_notes(parent=mw, notes=notes).run_in_background()

    # Send the field to DeepL for translation
    QueryOp(
        parent=mw,
        op=lambda col: translate_phrases(
            config.deepl_auth_key, config.source_lang, config.target_lang, phrases
        ),
        success=on_success,
    ).with_progress("Tranlating fields with DeepL...").run_in_background()
