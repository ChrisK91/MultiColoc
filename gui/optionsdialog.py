"""
Represets the options for MultiColoc
"""

import sys
import PyQt5.QtWidgets as qw
from PyQt5.QtGui import QIntValidator
from PyQt5 import QtCore


class OptionsDialog(qw.QDialog):
    """
    The options GUI for MultiColoc
    """

    AVAILABLESETTINGS = {
        "area_px" : "Area in px",
        "area_overlap_px" : "Area in px that overlaps with other channels",
        "intensity_avg" : "Mean intensity",
        "intensity_max" : "Maximum and minimum intensity",
        "com" : "Center of mass position",
    }

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Configure output options')

        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

        self.setWindowFlags(
            self.windowFlags() |
            QtCore.Qt.CustomizeWindowHint
        )

        self.setWindowFlags(
            self.windowFlags() &
            ~QtCore.Qt.WindowCloseButtonHint
        )

        vlayout = qw.QVBoxLayout()

        vlayout.addWidget(self._buildstatisticsarea())
        vlayout.addWidget(self._buildsavemaskarea())
        vlayout.addWidget(self._builddetectionarea())

        vlayout.addStretch()

        buttons = qw.QDialogButtonBox(
            qw.QDialogButtonBox.Ok | qw.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        vlayout.addWidget(buttons)

        self.setLayout(vlayout)

    def _buildsavemaskarea(self):
        groupbox = qw.QGroupBox(
            "Mask output settings"
        )

        hbox = qw.QHBoxLayout()

        self._maskfoldercontrol = qw.QLineEdit()
        self._maskfoldercontrol.setPlaceholderText(
            "Specify a folder, to save masks"
        )

        browsebutton = qw.QPushButton("Browse...")
        browsebutton.clicked.connect(self._savemasks)

        hbox.addWidget(self._maskfoldercontrol)
        hbox.addWidget(browsebutton)

        groupbox.setLayout(hbox)

        return groupbox

    def _builddetectionarea(self):
        """
        Build the groupbox for detection settings

        Returns:
            QWidget -- The detections settings control
        """

        groupbox = qw.QGroupBox(
            "Object detection settings"
        )

        vbox = qw.QVBoxLayout()

        connectivityhelp = qw.QLabel(
            "By default, horizontally and vertically adjacent pixels are "
            "combined into on object/feature when checking for overlap.\n"
            "Use the option below, to also group pixels that are diagonally adjacent."
        )
        connectivityhelp.setWordWrap(True)

        self._diagonalconnectivity = qw.QCheckBox(
            "Use diagonal connectivity"
        )

        thresholdbox = qw.QHBoxLayout()
        thresholdbox.addWidget(qw.QLabel("Threshold (above):"))

        self._thresholdinput = qw.QLineEdit("0")

        validator = QIntValidator()
        self._thresholdinput.setValidator(validator)
        self._thresholdinput.setPlaceholderText("0")

        thresholdbox.addWidget(self._thresholdinput)

        groupbox.setLayout(vbox)
        vbox.addLayout(thresholdbox)
        vbox.addWidget(connectivityhelp)
        vbox.addWidget(self._diagonalconnectivity)

        return groupbox

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
            "Specify a folder, to calculacte statistics"
        )

        browsebutton = qw.QPushButton("Browse...")
        browsebutton.clicked.connect(self._savecsv)

        self._optioncontrols = {
            key: qw.QCheckBox(option)
            for key, option in self.AVAILABLESETTINGS.items()
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

        folder = qw.QFileDialog.getExistingDirectory(
            self,
            "Save statistics to...",
        )
        self._csvlocationbox.setText(folder)

    def _savemasks(self):
        """
        Display save dialog for folder
        """

        folder = str(qw.QFileDialog.getExistingDirectory(
            self, "Select Directory"))
        self._maskfoldercontrol.setText(folder)


if __name__ == '__main__':
    APP = qw.QApplication(sys.argv)
    MW = OptionsDialog()
    MW.show()
    sys.exit(APP.exec_())