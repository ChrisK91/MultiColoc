"""
Provides classes for the main window of the MultiColoc tool
"""

import PyQt5.QtWidgets as qw
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from optionsdialog import OptionsDialog

class ChannelInfoWidget(qw.QGroupBox):
    """
    QtWidget, that holds controls to set up a channel.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Channel info")
        self._layout = qw.QVBoxLayout()

        removebutton = qw.QPushButton("Remove this channel")
        removebutton.clicked.connect(self._onremove)

        self._filetextbox = qw.QLineEdit()
        browsefilebutton = qw.QPushButton("Browse...")
        browsefilebutton.clicked.connect(self._onbrowse)

        firstrow = qw.QHBoxLayout()
        secondrow = qw.QHBoxLayout()
        thirdrow = qw.QHBoxLayout()

        firstrow.addWidget(qw.QLabel("Folder:"))
        firstrow.addWidget(self._filetextbox)
        firstrow.addWidget(browsefilebutton)

        secondrow.addWidget(qw.QLabel("Channel identifier:"))
        secondrow.addWidget(qw.QLineEdit())

        thirdrow.addStretch()
        thirdrow.addWidget(removebutton)

        self._layout.addLayout(firstrow)
        self._layout.addLayout(secondrow)
        self._layout.addLayout(thirdrow)

        self.setLayout(self._layout)


    def _onremove(self):
        """
        Handle click of "Remove this channel" button
        """
        self.deleteLater()

    def _onbrowse(self):
        """
        Handle click of "Browse..." button
        """
        folder = str(qw.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self._filetextbox.setText(folder)

class MultiColocMW(qw.QDialog):
    """
    Class for the main window
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('MultiColocalization Toolkit')
        self.setWindowIcon(QIcon('icon.ico'))

        self.setMinimumWidth(600)
        self.setMinimumHeight(600)

        self.setWindowFlags(
            self.windowFlags() |
            QtCore.Qt.WindowMinMaxButtonsHint
        )

        vbox = qw.QVBoxLayout()
        vbox.addWidget(self._buildtoparea())

        vbox.addWidget(self._buildcenterarea())

        vbox.addLayout(self._buildbottomarea())

        self.setLayout(vbox)

    def _buildtoparea(self):
        """
        Creates the top area containing:
            - Usage instructions

        Returns:
            QWidget -- A widget containing the top area
        """

        lbl = qw.QLabel(
            "1. Add a channel information for every channel you want to analyze\n"
            "2. Specify the channel unique names\n"
            "3. Set output options as needed"
        )
        lbl.setWordWrap(True)

        return lbl

    def _buildcenterarea(self):
        """
        Build the center area, containing:
            - A scroll area with a button to add channel infos

        Returns:
            QWidget -- A widget for the center area
        """
        filescrollarea = qw.QScrollArea()
        scrollablecontainer = qw.QWidget()

        self._fileinfolayout = qw.QVBoxLayout()
        self._fileinfolayout.addStretch()
        scrollablecontainer.setLayout(self._fileinfolayout)

        addchannelinfobutton = qw.QPushButton("Add channel info")
        addchannelinfobutton.clicked.connect(self._onaddchannel)
        self._fileinfolayout.insertWidget(0, addchannelinfobutton)

        filescrollarea.setWidgetResizable(True)
        filescrollarea.setWidget(scrollablecontainer)

        return filescrollarea

    def _buildbottomarea(self):
        """
        Build the bottom area, containing:
            - A input for the file extension
            - A options button
            - The run button

        Returns:
            QHBoxLayout -- A layout holding controls
        """

        bottombox = qw.QHBoxLayout()

        bottombox.addWidget(qw.QLabel("File extension"))

        self._fileextensioninput = qw.QLineEdit("tif")
        self._fileextensioninput.setFixedWidth(75)

        bottombox.addWidget(self._fileextensioninput)

        optionsbutton = qw.QPushButton("Options")
        optionsbutton.clicked.connect(self._onoptions)
        bottombox.addWidget(optionsbutton)

        #self._progressbar = QProgressBar()
        #bottombox.addWidget(self._progressbar)
        bottombox.addStretch()

        runbutton = qw.QPushButton("Run")
        bottombox.addWidget(runbutton)
        runbutton.setFixedWidth(75)

        return bottombox

    def _onoptions(self):
        """
        Handles click of the options button
        """
        dlg = OptionsDialog(self)

        dlg.exec_()

    def _onaddchannel(self):
        """
        Handles click of the "Add channel" button
        """
        self._fileinfolayout.insertWidget(
            self._fileinfolayout.count() - 1,
            ChannelInfoWidget()
            )
