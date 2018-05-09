import sys
from PyQt5.QtWidgets import QApplication
from multicolocmw import MultiColocMW

APP = QApplication(sys.argv)
MW = MultiColocMW()
MW.show()
sys.exit(APP.exec_())
