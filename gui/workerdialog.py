"""
The workerdialog shows progress about the colocalization
analysis. This file contains a worker, which handles the
underlying work. This worker is run in a seperate thread
that is started from the main dialog
"""

import logging
import os
import sys
import PyQt5.QtWidgets as qw
from PyQt5 import QtCore
import colocalizer.colocalize as coloc


class Worker(QtCore.QObject):
    """
    The worker collectes files and hands them over to the
    colocalization functions

    Arguments:
        QtCore  -- parent
    """

    # Signals to write log messages
    info = QtCore.pyqtSignal(str)
    warning = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)
    critical = QtCore.pyqtSignal(str)

    # Signals to update/indicate progress
    progressMin = QtCore.pyqtSignal(int)
    progressMax = QtCore.pyqtSignal(int)
    progressUpdate = QtCore.pyqtSignal(int)

    # Signal emited when work is done or canceled
    done = QtCore.pyqtSignal()

    # Flag to indicate that work should be canceled
    __abort = False

    def __init__(self, id_: int, options, channels):
        """Constructor

        Arguments:
            id_ {int} -- the id of the worker
            options {sharedstructures.Options} -- user specified options
            channels {sharedstructures.Channels} -- the channels specified by the user
        """

        super().__init__()
        self.__id = id_

        self._options = options
        self._channels = channels

        coloc._callback = self.info.emit

    @QtCore.pyqtSlot()
    def abort(self):
        """
        Sets the abort flag
        """

        # self.info.emit("Abort flag set")
        self.__abort = True

    @QtCore.pyqtSlot()
    def work(self):
        """
        Performs colocalization analysis with the settings
        set when constructing
        """

        self.info.emit("Analysis started")
        self.info.emit("---------------")
        self.info.emit("Gathering files:")
        filelist = self._collectfiles()
        self.info.emit("---------------")
        self.info.emit(
            "Done scanning files. Found {0} matching images".format(len(filelist)))

        self.progressMin.emit(0)
        self.progressMax.emit(len(filelist))

        progress = 0
        coloc.new_run()

        for matchingfiles in filelist:
            qw.QApplication.instance().processEvents()
            if self.__abort:
                self.done.emit()
                self.progressUpdate.emit(len(filelist))
                self.warning.emit("Operation canceled by user")
                return -1

            progress += 1
            self.progressUpdate.emit(progress)
            self.info.emit("Processing {0} of {1}".format(
                progress, len(filelist)))

            coloc.spatial_colocalize(matchingfiles, self._options)

        self.done.emit()

    def _getdatafileornone(self, file, datafolder):
        if os.path.isfile(os.path.join(datafolder, file)):
            return file
        else:
            self.warning.emit("Datafile does not exist at '{0}', using original instead".format(
                os.path.join(datafolder, file)
            ))

        return None

    def _getchannelfolderornone(self, channelnumber, unique, file=None):
        if self._options.maskfolder:
            if unique:
                return os.path.join(self._options.maskfolder, unique, file)
            return os.path.join(self._options.maskfolder, "Channel_{0}".format(channelnumber), file)
        return None

    def _collectfiles(self):
        referencechannel, *otherchannels = self._channels

        filelist = list()  # final list, contains list with corresponding files

        for file in os.listdir(referencechannel.folder):
            qw.QApplication.instance().processEvents()
            if self.__abort:
                self.done.emit()
                self.warning.emit("Operation canceled by user")
                return -1

            if file.endswith(self._options.filetype):
                self.info.emit("Found file '{0}'".format(file))

                # get datafile, display warning if datafolder is set and file does not exist
                datafile = None
                if referencechannel.datafolder:
                    datafile = self._getdatafileornone(
                        file, referencechannel.datafolder)
                    if datafile:
                        self.info.emit("with data file")

                channelcounter = 1
                # keeps count to name output masks, if no unique parts are specified

                maskfolder = self._getchannelfolderornone(
                    channelcounter, referencechannel.unique, file)

                referencefile = (
                    os.path.join(referencechannel.folder, file),
                    datafile,
                    maskfolder,
                    referencechannel.unique if referencechannel.unique else "Channel {0}".format(
                        channelcounter)
                )

                otherfiles = list()  # todo: refactor in function
                for channel in otherchannels:
                    channelcounter += 1
                    inferredname = file.replace(
                        referencechannel.unique, channel.unique)
                    absolute = os.path.join(channel.folder, inferredname)

                    if not os.path.isfile(absolute):
                        self.critical.emit(
                            "The expected file called '{0}' does not exist."
                            "Aborting...".format(absolute))
                    else:
                        self.info.emit(
                            "Corresponding: '{0}'".format(inferredname))

                    datafile = None
                    if channel.datafolder:
                        datafile = self._getdatafileornone(
                            inferredname, channel.datafolder)
                        if datafile:
                            self.info.emit("with data file")

                    channelfolder = self._getchannelfolderornone(
                        channelcounter, channel.unique, inferredname)

                    otherfiles.append((
                        absolute,
                        datafile,
                        channelfolder,
                        channel.unique if channel.unique else "Channel {0}".format(
                            channelcounter)
                    ))

                filelist.append(
                    [
                        referencefile,
                        *otherfiles
                    ]
                )
                # End of processing matching files

        return filelist


class QPlainTextEditLogger(logging.Handler, QtCore.QObject):
    """
    Represents a control, that can display python logging messages
    """

    def __init__(self, parent):
        super().__init__()

        self.widget = qw.QTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)

    def write(self, m):
        """
        Not implemented
        """

        pass


class WorkerDialog(qw.QDialog):
    """
    QDialog to display information about the work that is
    currently done. Work is handled by a seperate thread
    """

    _thread = None
    _worker = None

    _running = True

    def __init__(self, parent=None):
        """
        Constructor. You propably want to call .performwork after
        showing this dialog to actually start work.
        """

        super().__init__(parent)
        self.setWindowTitle('Analysis running...')

        self.setWindowFlags(
            self.windowFlags() |
            QtCore.Qt.CustomizeWindowHint
        )

        self.setWindowFlags(
            self.windowFlags() &
            ~QtCore.Qt.WindowCloseButtonHint
        )

        self.setMinimumHeight(400)
        self.setMinimumWidth(800)

        layout = qw.QVBoxLayout()

        self._progressbar = qw.QProgressBar()
        # self._progressbar.setTextVisible(False)
        self._progressbar.setMaximum(0)
        self._progressbar.setValue(0)

        self._textlog = QPlainTextEditLogger(self)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s:\t %(message)s')
        self._textlog.setFormatter(formatter)

        logging.getLogger().addHandler(self._textlog)
        logging.getLogger().setLevel(logging.DEBUG)

        buttons = qw.QDialogButtonBox(
            qw.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.rejected.connect(self._canceloperations)

        self.closebutton = qw.QPushButton("Close")
        self.closebutton.clicked.connect(self.close)
        buttons.addButton(self.closebutton, qw.QDialogButtonBox.ActionRole)

        layout.addWidget(self._progressbar)
        layout.addWidget(self._textlog.widget)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def _canceloperations(self):
        if self._thread:
            self._worker.abort()
            logging.info(
                "Abort requested. Operations will stop after next files are done.")

    @QtCore.pyqtSlot(str)
    def loginfo(self, msg):
        """Display a information message

        Arguments:
            msg {str} -- the message
        """

        logging.info(msg)

    @QtCore.pyqtSlot(str)
    def logwarning(self, msg):
        """Display a warning

        Arguments:
            msg {str} -- the message
        """

        logging.warning(msg)

    @QtCore.pyqtSlot(str)
    def logerror(self, msg):
        """Display an error

        Arguments:
            msg {str} -- the message
        """

        logging.error(msg)

    @QtCore.pyqtSlot(str)
    def logcritical(self, msg):
        """Display a critical error

        Arguments:
            msg {str} -- the message
        """

        logging.critical(msg)

    @QtCore.pyqtSlot()
    def workdone(self):
        """
        Slot to handle a signal from the worker, that
        work has finished
        """

        if self._thread:
            self._thread.quit()
            self._thread.wait()

            self._thread = None
            self._worker = None
            self._running = False

            self.closebutton.setEnabled(True)

            logging.info("Work finished.")

    def performwork(self, options, channels):
        """Start work for the dialog

        Arguments:
            options {structures.Options} -- options
            channels {structures.Channels} -- the user specified channels
        """

        self._running = True
        self.closebutton.setEnabled(False)
        worker = Worker(1, options, channels)
        thread = QtCore.QThread()
        thread.setObjectName("worker_thread")

        self._thread = thread # Prevent GC
        self._worker = worker # Prevent GC

        worker.moveToThread(thread)

        worker.info.connect(self.loginfo)
        worker.error.connect(self.logerror)
        worker.critical.connect(self.logcritical)
        worker.warning.connect(self.logwarning)

        worker.progressMax.connect(self._progressbar.setMaximum)
        worker.progressMin.connect(self._progressbar.setMinimum)
        worker.progressUpdate.connect(self._progressbar.setValue)

        worker.done.connect(self.workdone)

        thread.started.connect(worker.work)
        thread.start()


if __name__ == '__main__':
    from multicolocmw import Options, ChannelInfo

    test_options = Options(
        "test.csv",
        ["area_px"],
        "",
        False,
        2,
        ".tif"
    )

    test_channels = [
        ChannelInfo("testfiles/ch1", "ch1", "data_ch1_nonexisting"),
        ChannelInfo("testfiles/ch2", "ch2", ""),
        ChannelInfo("testfiles/ch3_and_ch4", "ch3", "nonexisting"),
        ChannelInfo("testfiles/ch3_and_ch4", "ch4", "")
    ]

    APP = qw.QApplication(sys.argv)
    MW = WorkerDialog()
    MW.show()
    MW.performwork(test_options, test_channels)
    sys.exit(APP.exec_())
