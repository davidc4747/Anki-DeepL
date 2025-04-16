from aqt import mw
from anki.models import NotetypeDict


def get_field_by_model_name(model_name: str) -> list[dict]:
    model = mw.col.models.by_name(model_name)
    return mw.col.models.field_names(model) if model else []


def get_field_index(model: NotetypeDict, field_name: str) -> int:
    return mw.col.models.field_names(model).index(field_name)
