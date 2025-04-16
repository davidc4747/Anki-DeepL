from PyQt6.QtCore import pyqtSignal
from aqt.qt import (
    QVBoxLayout,
    QFrame,
    QGroupBox,
    QDialog,
    QFormLayout,
    QComboBox,
    QLabel,
    QPushButton,
    QHBoxLayout,
)
from ..deepl import SOURCE_LANGUAGES, TARGET_LANGUAGES
from .note_type_table import NoteTypeTable
from ..config import UserConfig


class SettingDialog(QDialog):
    saved = pyqtSignal(UserConfig)
    default_restored = pyqtSignal()

    def __init__(self, config: UserConfig):
        super().__init__()
        self.setModal(True)
        self.setWindowTitle("Anki DeepL Configuration")

        group_layout = QVBoxLayout()

        # Language Dropdowns
        group_layout.addLayout(self.create_language_pickers(config))

        # Divider Line
        hline = QFrame()
        hline.setFrameShape(QFrame.Shape.HLine)
        hline.setFrameShadow(QFrame.Shadow.Sunken)
        group_layout.addWidget(hline)

        # Note Type Rows
        self.note_table = NoteTypeTable(config)
        group_layout.addLayout(self.note_table)
        group_layout.addStretch()

        group_box = QGroupBox()
        group_box.setLayout(group_layout)

        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(group_box)
        dialog_layout.addLayout(self.create_submit_buttons())
        self.setLayout(dialog_layout)

    def create_language_pickers(self, config: UserConfig) -> QFormLayout:
        # Language Pickers
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint
        )

        self.source_langs = QComboBox()
        self.source_langs.addItems(SOURCE_LANGUAGES)
        form_layout.addRow(QLabel("Source Language: "), self.source_langs)

        self.target_langs = QComboBox()
        self.target_langs.addItems(TARGET_LANGUAGES)
        form_layout.addRow(QLabel("Target Language: "), self.target_langs)
        self.target_langs.setCurrentText("EN-US")

        if config:
            self.source_langs.setCurrentText(config.source_lang)
            self.target_langs.setCurrentText(config.target_lang)

        return form_layout

    def create_submit_buttons(self) -> QHBoxLayout:
        submit_button_layout = QHBoxLayout()

        restoreBtn = QPushButton("Restore Default")
        restoreBtn.clicked.connect(self.handle_restore_default)
        submit_button_layout.addWidget(restoreBtn)
        submit_button_layout.addStretch()

        cancelBtn = QPushButton("Cancel")
        cancelBtn.clicked.connect(self.close)
        submit_button_layout.addWidget(cancelBtn)

        saveBtn = QPushButton("Save")
        saveBtn.setDefault(True)
        submit_button_layout.addWidget(saveBtn)

        def handle_save(self):
            self.close()

        saveBtn.clicked.connect(self.handle_save)
        return submit_button_layout

    def handle_save(self) -> None:
        self.saved.emit(
            UserConfig(
                source_lang=self.source_langs.currentText(),
                target_lang=self.target_langs.currentText(),
                translations=self.note_table.get_translations(),
            )
        )
        self.close()

    def handle_restore_default(self) -> None:
        self.default_restored.emit()
        self.close()
