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
# noteTypes = []

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
    source_langs.setCurrentText("ES")
    form_layout.addRow(QLabel("Source Language: "), source_langs)

    target_langs = QComboBox()
    target_langs.addItems(TARGET_LANGUAGES)
    target_langs.setCurrentText("EN-US")
    form_layout.addRow(QLabel("Target Language: "), target_langs)

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
    all_models = mw.col.models.all()
    # TODO: loop over the date structure instead of just some set number of times
    for i in range(1, 3):
        create_note_type_row(table_layout, all_models, i)
        # table_layout.addLayout(create_note_type_row(all_models, i))

    # Add Button
    # button_layout = QHBoxLayout()
    addRowBtn = QPushButton(" + Add Note Type")
    # button_layout.addWidget(addRowBtn)
    # button_layout.addStretch()
    # table_layout.addLayout(button_layout)
    table_layout.addWidget(addRowBtn, 4, 0)
    return table_layout


def create_note_type_row(table_layout: QGridLayout, all_models, index=0) -> QHBoxLayout:
    # row_layout = QHBoxLayout()

    # Note Type Dropdown
    modelCmbo = QComboBox()
    modelCmbo.addItems([model.get("name") for model in all_models])
    modelCmbo.setCurrentIndex(index)
    table_layout.addWidget(modelCmbo, index, 0)

    # Get Field List
    model = all_models[index]
    field_list = [field.get("name") for field in model.get("flds")]

    # Source
    source_field = QComboBox()
    source_field.addItems(field_list)
    table_layout.addWidget(source_field, index, 1)

    # Target
    target_field = QComboBox()
    target_field.addItems(field_list)
    table_layout.addWidget(target_field, index, 2)

    def update_fields(index: int):
        # Get New Fields
        model = all_models[index]
        field_list = [field.get("name") for field in model.get("flds")]

        # Clear
        source_field.clear()
        target_field.clear()
        # Update dropdowns
        source_field.addItems(field_list)
        target_field.addItems(field_list)

    modelCmbo.currentIndexChanged.connect(update_fields)

    delete = QLabel("❌")
    delete.setToolTip("Delete this Row")
    delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    table_layout.addWidget(delete, index, 3)


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
    saveBtn.clicked.connect(on_save)
    submit_button_layout.addWidget(saveBtn)
    return submit_button_layout
