"""
Main module for *SciCompPy project application*.

---
Copyright (C) 2026 Filip J. Baran
"""

# --- --- IMPORTS --- --- #

# --- libraries --- #
import sys
import xraylib
from PySide6 import QtWidgets, QtCore

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
        self.setFixedSize(1000, 600)

        mainWidget = QtWidgets.QTabWidget(
            tabPosition=QtWidgets.QTabWidget.TabPosition.West
        )
        xrfTab = periodic_table.PeriodicTables(
            {
                "Kα": {"line": xraylib.KA_LINE, "edge": xraylib.K_SHELL},
                "Kβ": {"line": xraylib.KB_LINE, "edge": xraylib.K_SHELL},
                "Lα": {"line": xraylib.LA_LINE, "edge": xraylib.L3_SHELL},
                "Lβ": {"line": xraylib.LB_LINE, "edge": xraylib.L2_SHELL},
                "Mα1": {"line": xraylib.MA1_LINE, "edge": xraylib.M5_SHELL},
            }
        )
        self.xrfTab = mainWidget.addTab(xrfTab, "XRF lines")
        self.manualTab = mainWidget.addTab(
            QtWidgets.QLabel(
                "Temporary widget", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
            ),
            "Manual",
        )

        self.setCentralWidget(mainWidget)


# --- --- EXECUTABLE --- --- #

# --- running the application --- #
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
