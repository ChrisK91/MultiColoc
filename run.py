"""
Main file to run the MultiColo application
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui.multicolocmw import MultiColocMW


def main():
    """
    Executes the application
    """

    APP = QApplication(sys.argv)
    MW = MultiColocMW()
    MW.show()
    sys.exit(APP.exec_())


if __name__ == '__main__':
    main()
