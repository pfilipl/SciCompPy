"""
Main module for *SciCompPy project application*.

---
Copyright (C) 2026 Filip J. Baran
"""

# --- --- IMPORTS --- --- #

# --- libraries --- #
import sys
import xraylib
from PySide6 import QtWidgets

# --- own files --- #
import periodic_table


# --- --- CODE --- --- #

# --- classes --- #
class MainWindow(QtWidgets.QMainWindow):
    """
    Main window widget.
    """

    def __init__(self, *args, **kwargs):
        """
        Widget initialization with layout configuration.
        """

        super().__init__(*args, **kwargs)

        self.setWindowTitle("SciCompPy project app: XRF spectra ROI definer")
        # self.setCentralWidget(periodic_table.PeriodicTable(line=xraylib.KA_LINE, edge=xraylib.K_SHELL, energy=10))
        # self.setCentralWidget(periodic_table.PeriodicTable(line=xraylib.MA1_LINE))
        self.setCentralWidget(periodic_table.PeriodicTable())
        self.setFixedSize(1000, 600)


# --- --- EXECUTABLE --- --- #

# --- running the application --- #
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
