from aqt import gui_hooks, mw
from aqt.operations import QueryOp
from aqt.operations.note import update_notes
from .settings.settings_dialog import SettingDialog
from .config import get_config, restore_defaults, save, set_config_action
from .deepl import translate_multiple


dialog = None


@set_config_action
def open_settings_window():
    global dialog
    dialog = SettingDialog(get_config())

    dialog.default_restored.connect(restore_defaults)
    dialog.saved.connect(save)

    dialog.show()
    dialog.activateWindow()


@gui_hooks.main_window_did_init.append
def generate_missing_fields():
    # Read User config
    config = get_config()

    # Select notes based on config
    search = " or ".join(
        [
            f'(added:2 "note:{t.name}" "{t.source_field}:_*" "{t.target_field}:")'
            for t in config.translations
        ]
    )
    note_ids = [nid for nid in mw.col.find_notes(search)]
    notes = [mw.col.get_note(nid) for nid in note_ids]

    phrases = []
    for note in notes:
        model = note.note_type()
        field_list = mw.col.models.field_names(model)
        model_config = next(
            t for t in config.translations if t.name == model.get("name")
        )
        source_index = field_list.index(model_config.source_field)
        phrases.append(note.values()[source_index])

    def on_success(english_translations):
        # Update the Note Fields
        for idx, note in enumerate(notes):
            model = note.note_type()
            target_index = next(
                mw.col.models.field_names(model).index(t.target_field)
                for t in config.translations
                if t.name == model.get("name")
            )
            note.fields[target_index] = english_translations[idx]
        update_notes(parent=mw, notes=notes).run_in_background()

    # Send the field to DeepL for translation
    QueryOp(
        parent=mw,
        op=lambda col: translate_multiple(
            config.source_lang, config.target_lang, phrases
        ),
        success=on_success,
    ).run_in_background()
