from aqt import gui_hooks, mw
from aqt.qt import (
    QWidget,
    QDialog,
    QAction,
    QLayout,
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QFrame,
    Qt,
)

dialog = None
source_language = ""
target_language = ""
# noteTypes = []
note_type_count = 2

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


def create_config_dialog(addon_name: str) -> QDialog:
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
    note_table = create_note_type_table()
    group_layout.addLayout(note_table)

    # Put it all together
    group_box = QGroupBox()
    group_box.setLayout(group_layout)

    dialog_layout = QVBoxLayout()
    dialog_layout.addWidget(group_box)
    dialog_layout.addLayout(create_submit_buttons(addon_name, dialog))
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
    table_layout = QVBoxLayout()

    # Header
    header_layout = QHBoxLayout()
    header_layout.setContentsMargins(0, 8, 0, 32)
    header_layout.addWidget(QLabel("Note Type:"))
    # header_layout.addSpacing(32)
    header_layout.addWidget(QLabel("Source Field:"))
    # header_layout.addSpacing(32)
    header_layout.addWidget(QLabel("Target Field:"))
    # header_layout.addStretch()
    table_layout.addLayout(header_layout)

    # NoteType Rows
    all_models = mw.col.models.all()
    for i in range(note_type_count):
        table_layout.addLayout(create_note_type_row(all_models, i))

    # Add Button
    button_layout = QHBoxLayout()
    addRowBtn = QPushButton(" + Add Note Type")
    button_layout.addWidget(addRowBtn)
    button_layout.addStretch()
    table_layout.addLayout(button_layout)

    # Spacer
    table_layout.addStretch()
    return table_layout


def create_note_type_row(all_models, index=0) -> QHBoxLayout:
    row_layout = QHBoxLayout()

    # Note Type Dropdown
    modelCmbo = QComboBox()
    modelCmbo.addItems([model.get("name") for model in all_models])
    modelCmbo.setCurrentIndex(index)
    row_layout.addWidget(modelCmbo)

    # Get Field List
    model = all_models[index]
    field_list = [field.get("name") for field in model.get("flds")]

    # Source
    source_field = QComboBox()
    source_field.addItems(field_list)
    row_layout.addWidget(source_field)

    # Target
    target_field = QComboBox()
    target_field.addItems(field_list)
    row_layout.addWidget(target_field)

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

    delete = QLabel(" X ")
    row_layout.addWidget(delete)
    return row_layout


def create_submit_buttons(addon_name: str, dialog: QDialog) -> QHBoxLayout:
    submit_button_layout = QHBoxLayout()

    def handle_defaults():
        default_config = mw.addonManager.addonConfigDefaults(addon_name)
        mw.addonManager.writeConfig(addon_name, default_config)

    restoreBtn = QPushButton("Restore Default")
    restoreBtn.clicked.connect(handle_defaults)
    submit_button_layout.addWidget(restoreBtn)
    submit_button_layout.addStretch()

    cancelBtn = QPushButton("Cancel")
    cancelBtn.clicked.connect(dialog.close)
    submit_button_layout.addWidget(cancelBtn)

    def handle_save():
        mw.addonManager.writeConfig(addon_name, "{ 'configursation': '!!!!' }")

    saveBtn = QPushButton("Save")
    saveBtn.setDefault(True)
    saveBtn.clicked.connect(handle_save)
    submit_button_layout.addWidget(saveBtn)
    return submit_button_layout


def open_config_window():
    global dialog
    dialog = create_config_dialog(__name__)
    dialog.show()
    dialog.activateWindow()


gui_hooks.main_window_did_init.append(open_config_window)
mw.addonManager.setConfigAction(__name__, open_config_window)
