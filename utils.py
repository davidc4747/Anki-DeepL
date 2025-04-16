from aqt import mw
from anki.models import NotetypeDict
from anki.notes import Note, NoteId
from .config import UserConfig


def get_field_by_model_name(model_name: str) -> list[dict]:
    model = mw.col.models.by_name(model_name)
    return mw.col.models.field_names(model) if model else []


def get_field_index(model: NotetypeDict, field_name: str) -> int:
    return mw.col.models.field_names(model).index(field_name)


def get_field_indices(config: UserConfig, note: Note) -> tuple[int, int]:
    model = note.note_type()
    translation_config = config.translations.get(model.get("name"))
    if translation_config:
        source_index: int = get_field_index(model, translation_config.source_field)
        target_index: int = get_field_index(model, translation_config.target_field)
        return (source_index, target_index)
    else:
        return (-1, -1)
