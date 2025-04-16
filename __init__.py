from aqt import gui_hooks, mw
from aqt.qt import QAction
from aqt.operations import QueryOp
from aqt.operations.note import update_notes
from anki.notes import Note, NoteId
from .settings.settings_dialog import SettingDialog
from .config import get_config, restore_defaults, save, set_config_action, UserConfig
from .deepl import translate_phrases, deepl_usage
from .utils import get_field_indices


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
        source_index, target_index = get_field_indices(config, note)

        if source_index != -1:
            field_len = len(note.values()[source_index])
            if char_count + field_len < usage.character_limit:
                notes.append(note)
                char_count += field_len

    # Break it up into multiple translation requests for DeepL
    CHUNK_SIZE = 500
    for i in range(0, len(notes), CHUNK_SIZE):
        translate_notes(config, notes[i : i + CHUNK_SIZE])


def translate_notes(config: UserConfig, notes: list[Note]) -> None:
    phrases = []
    for note in notes:
        source_index, target_index = get_field_indices(config, note)
        if source_index != -1:
            phrases.append(note.values()[source_index])

    def on_success(english_translations):
        # Update the Note Fields
        for idx, note in enumerate(notes):
            source_index, target_index = get_field_indices(config, note)
            if target_index != -1:
                note.fields[target_index] = english_translations[idx]
        update_notes(parent=mw, notes=notes).run_in_background()

    # Send the field to DeepL for translation
    QueryOp(
        parent=mw,
        op=lambda col: translate_phrases(
            config.deepl_auth_key, config.source_lang, config.target_lang, phrases
        ),
        success=on_success,
    ).with_progress("Tranlating DeepL Fields...").run_in_background()
