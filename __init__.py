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

dialog = QDialog()
dialog.setModal(True)
dialog.setWindowTitle("Anki DeepL Configuration")

noteTypes = []

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


def open_config_window():
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

    hline = QFrame()
    hline.setFrameShape(QFrame.Shape.HLine)
    hline.setFrameShadow(QFrame.Shadow.Sunken)

    # Note Type Rows
    notes_layout = QHBoxLayout()
    notes_layout.setContentsMargins(0, 8, 0, 32)
    notes_layout.addWidget(QLabel("Note Type:"))
    # notes_layout.addSpacing(32)
    notes_layout.addWidget(QLabel("Source Field:"))
    # notes_layout.addSpacing(32)
    notes_layout.addWidget(QLabel("Target Field:"))
    # notes_layout.addStretch()

    # TODO: Loop over this.
    # notes_layout.addWidget(QLabel("SP-Sentence (No Native Audio)"))
    # notes_layout.addWidget(QLabel("Spanish Answer"))
    # notes_layout.addWidget(QLabel("English Answer"))

    # Add Note Type button
    button_layout = QHBoxLayout()
    addRowBtn = QPushButton(" + Add Note Type")
    button_layout.addWidget(addRowBtn)
    button_layout.addStretch()

    # End -- GroupBox
    group_layout.addLayout(form_layout)
    group_layout.addWidget(hline)
    group_layout.addLayout(notes_layout)
    group_layout.addStretch()
    group_layout.addLayout(button_layout)
    group_box.setLayout(group_layout)
    main_layout.addWidget(group_box)

    # Row of Buttons
    button_box = QHBoxLayout()
    restoreBtn = QPushButton("Restore Default")
    button_box.addWidget(restoreBtn)
    button_box.addStretch()

    cancelBtn = QPushButton("Cancel")
    button_box.addWidget(cancelBtn)

    saveBtn = QPushButton("Save")
    button_box.addWidget(saveBtn)
    main_layout.addLayout(button_box)
    dialog.setLayout(main_layout)

    # Show time!
    dialog.show()
    dialog.activateWindow()


gui_hooks.main_window_did_init.append(open_config_window)
mw.addonManager.setConfigAction(__name__, open_config_window)
