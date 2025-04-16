from aqt import gui_hooks, mw
from aqt.operations import QueryOp
from aqt.operations.note import update_notes
from anki.notes import Note, NoteId
from .settings.settings_dialog import SettingDialog
from .config import get_config, restore_defaults, save, set_config_action, UserConfig
from .deepl import translate_phrases, deepl_usage
from .utils import get_field_index


dialog = None


@set_config_action
def open_settings_window():
    global dialog
    dialog = SettingDialog(get_config())

    dialog.default_restored.connect(restore_defaults)
    dialog.saved.connect(save)

    dialog.show()
    dialog.activateWindow()


@gui_hooks.sync_will_start.append
def generate_missing_fields():
    # Check that you haven't reached the DeepL Limit
    res = deepl_usage()
    if res.character_count / res.character_limit >= 0.9:
        print("Reached DeepL Limit")
        return

    # Read User config
    config = get_config()

    # Select notes based on config
    search = " or ".join(
        [
            f'("note:{t.model_name}" "{t.source_field}:_*" "{t.target_field}:")'
            for model_name, t in config.translations.items()
        ]
    )
    notes: list[Note] = [mw.col.get_note(nid) for nid in mw.col.find_notes(search)]

    CHUNK_SIZE = 1000
    for i in range(0, len(notes), CHUNK_SIZE):
        translate_notes(config, notes[i : i + CHUNK_SIZE])


def translate_notes(config: UserConfig, notes: list[Note]) -> None:
    phrases = []
    for note in notes:
        model = note.note_type()
        translation_config = config.translations.get(model.get("name"))
        if translation_config:
            source_index: int = get_field_index(model, translation_config.source_field)
            phrases.append(note.values()[source_index])

    def on_success(english_translations):
        # Update the Note Fields
        for idx, note in enumerate(notes):
            model = note.note_type()
            translation_config = config.translations.get(model.get("name"))
            if translation_config:
                target_index: int = get_field_index(
                    model, translation_config.target_field
                )
                note.fields[target_index] = english_translations[idx]
        update_notes(parent=mw, notes=notes).run_in_background()

    # Send the field to DeepL for translation
    QueryOp(
        parent=mw,
        op=lambda col: translate_phrases(
            config.source_lang, config.target_lang, phrases
        ),
        success=on_success,
    ).with_progress("Tranlating cards...").run_in_background()
