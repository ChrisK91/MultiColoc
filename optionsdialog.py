"""
Represets the options for MultiColoc
"""

import sys
import PyQt5.QtWidgets as qw


class OptionsDialog(qw.QDialog):
    """
    The options GUI for MultiColoc
    """

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

        vlayout = qw.QVBoxLayout()

        vlayout.addWidget(self._buildstatisticsarea())

        vlayout.addStretch()

        self.setLayout(vlayout)

    def _buildstatisticsarea(self):
        """Create the statistics area, based on "AVAILABLESETTINGS"

        Returns:
            QWidget -- The statistics area
        """

        groupbox = qw.QGroupBox(
            "Statistics options - Select options to calculate"
        )

        vbox = qw.QVBoxLayout()

        self._csvlocationbox = qw.QLineEdit()
        self._csvlocationbox.setPlaceholderText(
            "Specify a location to save statistics!"
        )

        browsebutton = qw.QPushButton("Browse...")
        browsebutton.clicked.connect(self._savecsv)

        self._optioncontrols = {
            option: qw.QCheckBox(option)
            for option in self.AVAILABLESETTINGS
        }

        for widget in self._optioncontrols.values():
            widget.setChecked(True)
            vbox.addWidget(widget)

        hbox = qw.QHBoxLayout()

        hbox.addWidget(self._csvlocationbox)
        hbox.addWidget(browsebutton)

        vbox.addLayout(hbox)

        groupbox.setLayout(vbox)
        return groupbox

    def _savecsv(self):
        """
        Displays save dialog for the CSV
        """

        file, _ = qw.QFileDialog.getSaveFileName(
            self,
            "Save statistics to...",
            "",
            filter="*.csv"
        )
        self._csvlocationbox.setText(file)


if __name__ == '__main__':
    APP = qw.QApplication(sys.argv)
    MW = OptionsDialog()
    MW.show()
    sys.exit(APP.exec_())
