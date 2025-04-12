from typing import Callable
from aqt import mw
from aqt.qt import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QPushButton,
    QLabel,
    QComboBox,
    QFrame,
    QCursor,
    Qt,
)

source_language = ""
target_language = ""

# Full Documentation here https://developers.deepl.com/docs/api-reference/translate/openapi-spec-for-text-translation
SOURCE_LANGUAGES = [
    "BG",
    "CS",
    "DA",
    "DE",
    "EL",
    "EN",
    "ES",
    "ET",
    "FI",
    "FR",
    "HU",
    "ID",
    "IT",
    "JA",
    "KO",
    "LT",
    "LV",
    "NB",
    "NL",
    "PL",
    "PT",
    "RO",
    "RU",
    "SK",
    "SL",
    "SV",
    "TR",
    "UK",
    "ZH",
]
TARGET_LANGUAGES = [
    "AR",
    "BG",
    "CS",
    "DA",
    "DE",
    "EL",
    "EN-GB",
    "EN-US",
    "ES",
    "ET",
    "FI",
    "FR",
    "HU",
    "ID",
    "IT",
    "JA",
    "KO",
    "LT",
    "LV",
    "NB",
    "NL",
    "PL",
    "PT-BR",
    "PT-PT",
    "RO",
    "RU",
    "SK",
    "SL",
    "SV",
    "TR",
    "UK",
    "ZH",
    "ZH-HANS",
    "ZH-HANT",
]

state = {"source_lang": "EN", "target_lang": "ES", "translations": []}


def create_dialog(on_restore: Callable, on_save: Callable) -> QDialog:
    dialog = QDialog()
    dialog.setModal(True)
    dialog.setWindowTitle("Anki DeepL Configuration")

    group_layout = QVBoxLayout()

    # Language Dropdowns
    group_layout.addLayout(create_language_pickers())

    # Divider Line
    hline = QFrame()
    hline.setFrameShape(QFrame.Shape.HLine)
    hline.setFrameShadow(QFrame.Shadow.Sunken)
    group_layout.addWidget(hline)

    # Note Type Rows
    group_layout.addLayout(create_note_type_table())
    group_layout.addStretch()

    group_box = QGroupBox()
    group_box.setLayout(group_layout)

    dialog_layout = QVBoxLayout()
    dialog_layout.addWidget(group_box)
    dialog_layout.addLayout(create_submit_buttons(dialog, on_restore, on_save))
    dialog.setLayout(dialog_layout)
    return dialog


def create_language_pickers() -> QFormLayout:
    # Language Pickers
    form_layout = QFormLayout()
    form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)

    source_langs = QComboBox()
    source_langs.addItems(SOURCE_LANGUAGES)
    form_layout.addRow(QLabel("Source Language: "), source_langs)

    def handle_source_lang_changed(text):
        state["source_lang"] = text

    source_langs.currentTextChanged.connect(handle_source_lang_changed)
    source_langs.setCurrentText("ES")

    target_langs = QComboBox()
    target_langs.addItems(TARGET_LANGUAGES)
    form_layout.addRow(QLabel("Target Language: "), target_langs)

    def handle_target_lang_changed(text):
        state["target_lang"] = text

    target_langs.currentTextChanged.connect(handle_target_lang_changed)
    target_langs.setCurrentText("EN-US")

    return form_layout


def create_note_type_table() -> QVBoxLayout:
    table_layout = QGridLayout()
    table_layout.setColumnStretch(0, 1)
    table_layout.setColumnStretch(1, 1)
    table_layout.setColumnStretch(2, 1)
    table_layout.setColumnStretch(3, 0)
    table_layout.addWidget(QLabel(f"Note Type:"), 0, 0)
    table_layout.addWidget(QLabel(f"Source Field:"), 0, 1)
    table_layout.addWidget(QLabel(f"Target Field:"), 0, 2)

    # NoteType Rows
    for note_type in state["translations"]:
        render_note_type_row(table_layout, note_type)

    def new_note_type_row() -> None:
        all_models = mw.col.models.all()
        model = all_models[0]
        field_list = mw.col.models.field_names(model)

        new_note_type = {
            "id": 0,
            "name": model.get("name"),
            "source_field": field_list[0],
            "target_field": field_list[1],
        }
        new_note_type["id"] = id(new_note_type)
        state["translations"].append(new_note_type)
        render_note_type_row(table_layout, new_note_type)

    # Add Button
    addRowBtn = QPushButton(" + Add Note Type")
    addRowBtn.clicked.connect(new_note_type_row)
    table_layout.addWidget(addRowBtn, 4, 0)
    return table_layout


def render_note_type_row(table_layout: QGridLayout, note_type) -> None:

    def get_index():
        return next(
            (
                index
                for index, translation in enumerate(state["translations"])
                if translation.get("id") == note_type.get("id")
            ),
            -1,
        )

    index = get_index()

    # Note Type Dropdown
    modelCmbo = QComboBox()
    modelCmbo.addItems([nameId.name for nameId in mw.col.models.all_names_and_ids()])
    modelCmbo.setCurrentText(note_type["name"])
    table_layout.addWidget(modelCmbo, index, 0)

    # Get Field List
    model = mw.col.models.by_name(note_type["name"])
    field_list = mw.col.models.field_names(model)

    # Source
    source_field = QComboBox()
    source_field.addItems(field_list)
    source_field.setCurrentText(note_type["source_field"])
    table_layout.addWidget(source_field, index, 1)

    def handle_source_field_changed(text):
        index = get_index()
        state["translations"][index]["source_field"] = text

    source_field.currentTextChanged.connect(handle_source_field_changed)

    # Target
    target_field = QComboBox()
    target_field.addItems(field_list)
    target_field.setCurrentText(note_type["target_field"])
    table_layout.addWidget(target_field, index, 2)

    def handle_target_field_changed(text):
        index = get_index()
        state["translations"][index]["target_field"] = text

    target_field.currentTextChanged.connect(handle_target_field_changed)

    def handle_update_fields(name: int):
        # Get New Fields
        model = mw.col.models.by_name(name)
        field_list = mw.col.models.field_names(model)

        # Update dropdowns
        source_field.clear()
        source_field.setCurrentIndex(0)
        source_field.addItems(field_list)

        target_field.clear()
        target_field.addItems(field_list)
        target_field.setCurrentIndex(1)

        # Update Data
        index = get_index()
        state["translations"][index]["name"] = name
        state["translations"][index]["source_field"] = source_field.currentText()
        state["translations"][index]["target_field"] = target_field.currentText()

    modelCmbo.currentTextChanged.connect(handle_update_fields)

    delete = QPushButton("❌")
    delete.setToolTip("Delete this Row")
    table_layout.addWidget(delete, index, 3)

    def handle_delete():
        index = get_index()
        del state["translations"][index]
        for i in range(table_layout.columnCount()):
            table_layout.itemAtPosition(index, i).widget().deleteLater()
        table_layout.removeWidget(source_field)
        table_layout.removeWidget(target_field)
        table_layout.removeWidget(delete)

    #
    delete.clicked.connect(handle_delete)


def create_submit_buttons(
    dialog: QDialog, on_restore: Callable, on_save: Callable
) -> QHBoxLayout:
    submit_button_layout = QHBoxLayout()

    restoreBtn = QPushButton("Restore Default")
    restoreBtn.clicked.connect(on_restore)
    submit_button_layout.addWidget(restoreBtn)
    submit_button_layout.addStretch()

    cancelBtn = QPushButton("Cancel")
    cancelBtn.clicked.connect(dialog.close)
    submit_button_layout.addWidget(cancelBtn)

    saveBtn = QPushButton("Save")
    saveBtn.setDefault(True)
    submit_button_layout.addWidget(saveBtn)

    def handle_save():
        on_save(state)
        dialog.close()

    saveBtn.clicked.connect(handle_save)
    return submit_button_layout
