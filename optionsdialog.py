from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import sys

class OptionsDialog(QDialog):
    AVAILABLESETTINGS = [
        "Area in px",
        "Area in px that overlaps with other channels",
        "Average intensity",
        "Maximum intensity",
        "Center of mass position",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Configure output options')

        self.setMinimumWidth(400)
        self.setMinimumHeight(400)

        self.resize(400, 400)

        vlayout = QVBoxLayout()

        vlayout.addWidget(self.buildstatisticsarea())

        vlayout.addStretch()

        self.setLayout(vlayout)

    def buildstatisticsarea(self):
        groupbox = QGroupBox("Statistics options - Select options to calculate")

        vbox = QVBoxLayout()

        self._csvlocationbox = QLineEdit()
        self._csvlocationbox.setPlaceholderText("Specify a location to save statistics!")
        browsebutton = QPushButton("Browse...")
        browsebutton.clicked.connect(self._savecsv)

        self._optioncontrols = {
            option : QCheckBox(option)
            for option in self.AVAILABLESETTINGS
        }

        for w in self._optioncontrols.values():
            w.setChecked(True)
            vbox.addWidget(w)

        hbox = QHBoxLayout()

        hbox.addWidget(self._csvlocationbox)
        hbox.addWidget(browsebutton)

        vbox.addLayout(hbox)

        groupbox.setLayout(vbox)
        return groupbox

    def _savecsv(self):
        file, filter = QFileDialog.getSaveFileName(
            self,
            "Save statistics to...",
            "",
            filter = "*.csv"
        )
        self._csvlocationbox.setText(file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = OptionsDialog()
    mw.show()
    sys.exit(app.exec_())