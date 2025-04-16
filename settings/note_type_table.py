from aqt import mw
from aqt.qt import QGridLayout, QLabel, QPushButton, QComboBox
from ..utils import get_field_by_model_name
from ..config import UserConfig, TransaltionConfig


class NoteTypeTable(QGridLayout):
    def __init__(self, config: UserConfig):
        super().__init__()
        self.setColumnStretch(0, 1)
        self.setColumnStretch(1, 1)
        self.setColumnStretch(2, 1)
        self.setColumnStretch(3, 0)

        # Headers
        self.addWidget(QLabel(f"Note Type:"), 0, 0)
        self.addWidget(QLabel(f"Source Field:"), 0, 1)
        self.addWidget(QLabel(f"Target Field:"), 0, 2)

        # NoteType Rows
        if config and config.translations:
            for index, note_type in enumerate(config.translations):
                # index+1 cuz the first row has Qlabels in it
                self.insert_row(note_type, index + 1)

        # Add Button
        addRowBtn = QPushButton(" + Add Note Type")
        addRowBtn.clicked.connect(self.append_row)
        self.addWidget(addRowBtn, 4, 0)

    def insert_row(self, note_type: TransaltionConfig, row: int) -> None:
        # Note Type Dropdown
        modelCmbo = QComboBox()
        modelCmbo.addItems(
            [nameId.name for nameId in mw.col.models.all_names_and_ids()]
        )
        modelCmbo.setCurrentText(note_type.name)
        modelCmbo.currentTextChanged.connect(self.handle_update_row)

        # Get Field List
        field_list = get_field_by_model_name(modelCmbo.currentText())

        # Source
        source_field = QComboBox()
        source_field.addItems(field_list if len(field_list) > 0 else [""])
        source_field.setCurrentText(note_type.source_field)

        # Target
        target_field = QComboBox()
        target_field.addItems(field_list if len(field_list) > 0 else [""])
        target_field.setCurrentText(note_type.target_field)

        # Delete
        delete = QPushButton("❌")
        delete.setToolTip("Delete this Row")
        delete.clicked.connect(self.handle_delete_row)

        # Make space for the new row in the table
        new_row = [modelCmbo, source_field, target_field, delete]
        for r in range(row, self.rowCount() + 1):
            for col in range(self.columnCount()):
                # Swap the Widget in the Grid with the one I have in Memeory
                temp = self.itemAtPosition(r, col)
                temp = temp.widget() if temp else None
                if temp:
                    self.removeWidget(temp)
                if new_row[col]:
                    self.addWidget(new_row[col], r, col)
                new_row[col] = temp

    def append_row(self) -> None:
        # Add the new Row
        model = mw.col.models.all()[0]
        field_list = mw.col.models.field_names(model)
        self.insert_row(
            TransaltionConfig(
                **{
                    "name": model.get("name"),
                    "source_field": field_list[0] or "",
                    "target_field": field_list[1] or "",
                }
            ),
            self.rowCount() - 1,  # Move it 1 above the " + Add Note Type"
        )

    def handle_update_row(self, name: int) -> None:
        # Get New Fields
        field_list = get_field_by_model_name(name)
        row, col, rowspan, colspan = self.getItemPosition(self.indexOf(self.sender()))

        source_field = self.itemAtPosition(row, 1)
        if source_field:
            source_field = source_field.widget()
            source_field.clear()
            source_field.addItems(field_list)
            source_field.setCurrentIndex(0)

        target_field = self.itemAtPosition(row, 2)
        if target_field:
            target_field = target_field.widget()
            target_field.clear()
            target_field.addItems(field_list)
            target_field.setCurrentIndex(1)

    def handle_delete_row(self) -> None:
        row, col, rowspan, colspan = self.getItemPosition(self.indexOf(self.sender()))

        # Delete the whole row
        for i in range(self.columnCount()):
            widget = self.itemAtPosition(row, i)
            if widget:
                widget.widget().deleteLater()

    def get_translations(self) -> dict:
        translations = []
        for row in range(1, self.rowCount() - 1):

            modelCmbo = self.itemAtPosition(row, 0)
            source_field = self.itemAtPosition(row, 1)
            target_field = self.itemAtPosition(row, 2)

            if modelCmbo and source_field and target_field:
                translations.append(
                    {
                        "name": modelCmbo.widget().currentText(),
                        "source_field": source_field.widget().currentText(),
                        "target_field": target_field.widget().currentText(),
                    }
                )

        return translations
