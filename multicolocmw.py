from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

class ChannelInfoWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Channel info")
        self._layout = QVBoxLayout()

        removebutton = QPushButton("Remove this channel")
        removebutton.clicked.connect(self.onremove)

        self._filetextbox = QLineEdit()
        browsefilebutton = QPushButton("Browse...")
        browsefilebutton.clicked.connect(self.onbrowse)

        #
        #  Folder : ------ : Browse
        #  Distinct part: ---- : Remove channel
        #

        firstrow = QHBoxLayout()
        secondrow = QHBoxLayout()
        thirdrow = QHBoxLayout()

        firstrow.addWidget(QLabel("Folder:"))
        firstrow.addWidget(self._filetextbox)
        firstrow.addWidget(browsefilebutton)

        secondrow.addWidget(QLabel("Channel identifier:"))
        secondrow.addWidget(QLineEdit())

        thirdrow.addStretch()
        thirdrow.addWidget(removebutton)

        self._layout.addLayout(firstrow)
        self._layout.addLayout(secondrow)
        self._layout.addLayout(thirdrow)

        self.setLayout(self._layout)

    def onremove(self):
        self.deleteLater()

    def onbrowse(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self._filetextbox.setText(folder)

class MultiColocMW(QDialog):
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

        vbox = QVBoxLayout()
        vbox.addWidget(self.buildtoparea())

        vbox.addWidget(self.buildcenterarea())

        vbox.addLayout(self.buildbottomarea())

        self.setLayout(vbox)

    def buildtoparea(self):
        lbl = QLabel(
            "1. Add a channel information for every channel you want to analyze\n"
            "2. Specify the channel unique names\n"
            "3. Set output options as needed"
        )
        lbl.setWordWrap(True)

        return lbl

    def buildcenterarea(self):    
        filescrollarea = QScrollArea()
        scrollablecontainer = QWidget()

        self._fileinfolayout = QVBoxLayout()
        self._fileinfolayout.addStretch()
        scrollablecontainer.setLayout(self._fileinfolayout)

        addchannelinfobutton = QPushButton("Add channel info")
        addchannelinfobutton.clicked.connect(self.onaddchannel)
        self._fileinfolayout.insertWidget(0, addchannelinfobutton)

        filescrollarea.setWidgetResizable(True)
        filescrollarea.setWidget(scrollablecontainer)

        return filescrollarea

    def buildbottomarea(self):
        bottombox = QHBoxLayout()
        
        self._progressbar = QProgressBar()
        bottombox.addWidget(self._progressbar)
        
        self._runbutton = QPushButton("Run")
        bottombox.addWidget(self._runbutton)
        self._runbutton.setFixedWidth(250)

        return bottombox

    def onaddchannel(self):
        self._fileinfolayout.insertWidget(
            self._fileinfolayout.count() - 1,
            ChannelInfoWidget()
            )

    def onremovechild(self, widget):
        self._fileinfolayout.removeWidget(widget)