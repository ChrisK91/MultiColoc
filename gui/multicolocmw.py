"""
Provides classes for the main window of the MultiColoc tool
"""
import PyQt5.QtWidgets as qw
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from gui.optionsdialog import OptionsDialog
from gui.workerdialog import WorkerDialog
from structures import Options, ChannelInfo

class ChannelInfoWidget(qw.QGroupBox):
    """
    QtWidget, that holds controls to set up a channel.
    """

    def __init__(self, channellist, parent=None):
        super().__init__(parent)

        self.setTitle("Channel info")
        self._layout = qw.QVBoxLayout()

        removebutton = qw.QPushButton("Remove this channel")
        removebutton.clicked.connect(self._onremove)

        self._filetextbox = qw.QLineEdit()
        browsefilebutton = qw.QPushButton("Browse...")
        browsefilebutton.clicked.connect(lambda x: self._onbrowse(self._filetextbox))

        self._datafilebox = qw.QLineEdit()
        self._datafilebox.setPlaceholderText("Leave empty to ignore")
        browsedatabutton = qw.QPushButton("Browse...")
        browsedatabutton.clicked.connect(lambda x: self._onbrowse(self._datafilebox))

        firstrow = qw.QHBoxLayout()
        secondrow = qw.QHBoxLayout()
        thirdrow = qw.QHBoxLayout()
        fourthrow = qw.QHBoxLayout()

        firstrow.addWidget(qw.QLabel("Folder:"))
        firstrow.addWidget(self._filetextbox)
        firstrow.addWidget(browsefilebutton)

        secondrow.addWidget(qw.QLabel("Channel identifier:"))

        thirdrow.addWidget(qw.QLabel("Data files:"))
        thirdrow.addWidget(self._datafilebox)
        thirdrow.addWidget(browsedatabutton)

        self._idtextbox = qw.QLineEdit()
        secondrow.addWidget(self._idtextbox)

        fourthrow.addStretch()
        fourthrow.addWidget(removebutton)

        self._layout.addLayout(firstrow)
        self._layout.addLayout(secondrow)
        self._layout.addLayout(thirdrow)
        self._layout.addLayout(fourthrow)

        self.setLayout(self._layout)
        channellist.append(self)
        self._channellist = channellist

    def _onremove(self):
        """
        Handle click of "Remove this channel" button
        """
        self._channellist.remove(self)
        self.deleteLater()

    def _onbrowse(self, textbox):
        """
        Handle click of "Browse..." button
        """

        folder = str(qw.QFileDialog.getExistingDirectory(
            self, "Select Directory"))
        textbox.setText(folder)

    def channelinfo(self):
        """Generate channel info for the input

        Returns:
            ChannelInfo -- a named touple with the user configuration
        """

        return ChannelInfo(
            self._filetextbox.text(),
            self._idtextbox.text(),
            self._datafilebox.text()
        )


class MultiColocMW(qw.QDialog):
    """
    Class for the main window
    """

    _options = None
    _channels = list()

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
            "a) \"Folder\" points to the place where your images are stored\n"
            "b) \"Channel identifier\" is the part of the name, that is unique for thath channel\n"
            "c) If you specify \"Data files\", intensity values from "
            "these images will be used to calculate statistics\n"
            "\n2. Set output options as needed\n"
            "\n3. Run the analysis\n"
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

        bottombox.addStretch()

        runbutton = qw.QPushButton("Run")
        runbutton.clicked.connect(self._run)
        bottombox.addWidget(runbutton)
        runbutton.setFixedWidth(75)

        return bottombox

    def _run(self):
        # net valid options to run
        if not self._options:
            mbox = qw.QMessageBox(self)
            mbox.setIcon(qw.QMessageBox.Information)
            mbox.setText("Please specify your options first")
            mbox.setWindowTitle("Information")
            mbox.setStandardButtons(qw.QMessageBox.Ok)
            mbox.exec_()

            self._onoptions()

            return -1

        channels = [item.channelinfo() for item in self._channels]

        # need at least two channels to run
        if len(channels) < 2:
            mbox = qw.QMessageBox(self)
            mbox.setIcon(qw.QMessageBox.Critical)
            mbox.setWindowTitle("Error")
            mbox.setText("Please specify at least two channels")
            mbox.setStandardButtons(qw.QMessageBox.Cancel)
            mbox.exec_()

            return -1
        else:
            # check for channels without folders
            for channel in channels:
                if not channel.folder:
                    mbox = qw.QMessageBox(self)
                    mbox.setIcon(qw.QMessageBox.Critical)
                    mbox.setWindowTitle("Error")
                    mbox.setText("At least one channel has no file location specified!")
                    mbox.setStandardButtons(qw.QMessageBox.Cancel)
                    mbox.show()
                    return -1

        # We have a valid configuration if we end up here
        # The workerdialog handles the rest

        wd = WorkerDialog(self)
        wd.show()
        wd.performwork(self._options, channels)


    def _storeoptions(self, dlg):
        self._options = Options(
            dlg._csvlocationbox.text(),
            [
                key for key, value in dlg._optioncontrols.items()
                if value.isChecked()
            ],
            dlg._maskfoldercontrol.text(),
            dlg._diagonalconnectivity.isChecked(),
            int(dlg._thresholdinput.text()) if dlg._thresholdinput.text() else 0,
            self._fileextensioninput.text()
        )

    def _onoptions(self):
        """
        Handles click of the options button
        """

        dlg = OptionsDialog(self)

        if dlg.exec_():
            self._storeoptions(dlg)

    def _onaddchannel(self):
        """
        Handles click of the "Add channel" button
        """

        self._fileinfolayout.insertWidget(
            self._fileinfolayout.count() - 1,
            ChannelInfoWidget(self._channels)
        )
