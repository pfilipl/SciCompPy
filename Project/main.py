"""
Main module for *SciCompPy project application*.

---
Copyright (C) 2026 Filip J. Baran
"""

# --- --- IMPORTS --- --- #

# --- libraries --- #
import sys
import argparse
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

    def __init__(self, args, parent=None):
        """
        Widget initialization with layout configuration.
        """

        super().__init__(parent)

        try:
            energy = float(args.energy)
        except Exception:
            energy = None

        self.setWindowTitle("SciCompPy project app: XRF Spectra ROI Definer")
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
            },
            energy,
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
def main():
    parser = argparse.ArgumentParser(
        prog="XRF Spectra ROI Definer",
        description="""
        SciCompPy project application for defining energetic regions of interest (ROIs) 
        for X-ray Fluorescence spectra analysis.
        """,
    )
    parser.add_argument(
        "-e", "--energy", required=False, help="excitation energy [keV]"
    )
    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(args)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
