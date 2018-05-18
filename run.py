"""
Main file to run the MultiColo application
"""

import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
import PyQt5.QtCore as qc


def main():
    """
    Executes the application
    """

    APP = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap('files/splash.png'))
    splash.show()

    from gui.multicolocmw import MultiColocMW
    MW = MultiColocMW()
    MW.show()
    splash.hide()
    sys.exit(APP.exec_())


if __name__ == '__main__':
    main()
