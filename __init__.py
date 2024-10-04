from aqt import gui_hooks, mw
from aqt.qt import (
    QWidget,
    QDialog,
    QAction,
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

    main_layout = QVBoxLayout()
    group_box = QGroupBox()
    group_layout = QVBoxLayout()

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
    group_layout.addLayout(form_layout)

    hline = QFrame()
    hline.setFrameShape(QFrame.Shape.HLine)
    hline.setFrameShadow(QFrame.Shadow.Sunken)
    group_layout.addWidget(hline)

    # Note Type Rows
    header_layout = QHBoxLayout()
    header_layout.setContentsMargins(0, 8, 0, 32)
    header_layout.addWidget(QLabel("Note Type:"))
    # header_layout.addSpacing(32)
    header_layout.addWidget(QLabel("Source Field:"))
    # header_layout.addSpacing(32)
    header_layout.addWidget(QLabel("Target Field:"))
    # header_layout.addStretch()
    group_layout.addLayout(header_layout)

    for i in range(note_type_count):
        type_layout = QHBoxLayout()

        modelCmbo = QComboBox()
        all_models = mw.col.models.all()
        modelCmbo.addItems([model.get("name") for model in all_models])
        modelCmbo.setCurrentIndex(0)
        type_layout.addWidget(modelCmbo)

        text = modelCmbo.currentText()
        # lbl = QLabel(modelCmbo.currentText)
        lbl = QLabel(text)
        # lbl = QLabel("1")
        type_layout.addWidget(lbl)

        source_field = QComboBox()
        type_layout.addWidget(source_field)

        target_field = QComboBox()
        type_layout.addWidget(target_field)

        delete = QLabel(" X ")
        type_layout.addWidget(delete)
        group_layout.addLayout(type_layout)

    # Add Note Type button
    button_layout = QHBoxLayout()
    addRowBtn = QPushButton(" + Add Note Type")
    button_layout.addWidget(addRowBtn)
    button_layout.addStretch()
    group_layout.addLayout(button_layout)
    group_layout.addStretch()

    # End -- GroupBox
    group_box.setLayout(group_layout)
    main_layout.addWidget(group_box)

    # Row of submit Buttons
    button_box = QHBoxLayout()

    def handle_defaults():
        default_config = mw.addonManager.addonConfigDefaults(addon_name)
        mw.addonManager.writeConfig(addon_name, default_config)

    restoreBtn = QPushButton("Restore Default")
    restoreBtn.clicked.connect(handle_defaults)
    button_box.addWidget(restoreBtn)
    button_box.addStretch()

    cancelBtn = QPushButton("Cancel")
    cancelBtn.clicked.connect(dialog.close)
    button_box.addWidget(cancelBtn)

    def handle_save():
        mw.addonManager.writeConfig(addon_name, "{ 'configursation': '!!!!' }")

    saveBtn = QPushButton("Save")
    saveBtn.setDefault(True)
    saveBtn.clicked.connect(handle_save)
    button_box.addWidget(saveBtn)

    main_layout.addLayout(button_box)
    dialog.setLayout(main_layout)
    return dialog


def open_config_window():
    global dialog
    dialog = create_config_dialog(__name__)
    dialog.show()
    dialog.activateWindow()


gui_hooks.main_window_did_init.append(open_config_window)
mw.addonManager.setConfigAction(__name__, open_config_window)
