from aqt import mw


def get_field_by_model_name(model_name: str) -> list[dict]:
    model = mw.col.models.by_name(model_name)
    return mw.col.models.field_names(model) if model else []
