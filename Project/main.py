"""
Main module for *SciCompPy project application*.

---
Copyright (C) 2026 Filip J. Baran
"""

# --- --- IMPORTS --- --- #

# --- standard libraries --- #
import sys
import json
from math import sqrt
from argparse import ArgumentParser

# --- 3rd party libraries --- #
import xraylib
from PySide6 import QtWidgets, QtCore, QtGui

# --- own files --- #
import periodic_table
import manual
import files


# --- --- CODE --- --- #


# --- classes --- #
class MainWindow(QtWidgets.QMainWindow):
    """
    Main window widget.
    """

    def __init__(self, args, /, parent=None):
        """
        Widget initialization with layout and toolbar configuration.
        """

        super().__init__(parent)

        # --- command line arguments --- #
        try:
            self.energy = float(args.energy) / 1000  # [eV] -> [keV] for xraylib
        except Exception:
            self.energy = None

        # --- variables --- #
        self.Detectors = {"SDD1": Detector(), "SDD2": Detector()}
        # self.Detectors = {
        #     "SDD1": Detector(),
        #     "SDD2": Detector(-100, 5, 300, 0.01),
        #     # "SDD3": Detector(200, 3, 500, 0.01),
        # }
        # self.Detectors = {}

        # --- --- layout --- --- #
        self.setWindowTitle("SciCompPy project app: XRF Spectra ROI Definer")
        self.setFixedSize(1000, 600)

        mainWidget = QtWidgets.QTabWidget(
            tabPosition=QtWidgets.QTabWidget.TabPosition.West
        )
        self.setCentralWidget(mainWidget)

        # --- XRF tab --- #
        self.xrfTab = periodic_table.PeriodicTables(
            {
                "Kα": {"line": xraylib.KA_LINE, "edge": xraylib.K_SHELL},
                "Kβ": {"line": xraylib.KB_LINE, "edge": xraylib.K_SHELL},
                "Lα": {"line": xraylib.LA_LINE, "edge": xraylib.L3_SHELL},
                "Lβ": {"line": xraylib.LB_LINE, "edge": xraylib.L2_SHELL},
                "Mα1": {"line": xraylib.MA1_LINE, "edge": xraylib.M5_SHELL},
            },
            self.energy,
        )
        self.xrfTab.elementToggled.connect(
            lambda checked, name, line: self.manualTab.toglleElementROI(
                checked, name, line
            )
        )
        mainWidget.addTab(self.xrfTab, "XRF lines")

        # --- manual tab --- #
        self.manualTab = manual.Manual(self.Detectors, parent=self)
        self.manualTab.checkElement.connect(
            lambda checked, name, tabName: self.xrfTab.checkElement(
                checked, name, tabName
            )
        )
        mainWidget.addTab(self.manualTab, "Manual")

        # --- --- toolbar --- --- #
        toolbar = QtWidgets.QToolBar(
            "Main toolbar",
            movable=False,
            floatable=False,
            iconSize=QtCore.QSize(24, 24),
            toolButtonStyle=QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon,
        )
        self.addToolBar(toolbar)

        # --- import --- #
        importAction = QtGui.QAction(
            QtGui.QIcon.fromTheme(QtGui.QIcon.ThemeIcon.DocumentOpen),
            "Import",
            self,
            enabled=False,
        )
        importAction.triggered.connect(self.importTriggered)
        toolbar.addAction(importAction)

        # --- export --- #
        exportAction = QtGui.QAction(
            QtGui.QIcon.fromTheme(QtGui.QIcon.ThemeIcon.DocumentSaveAs), "Export", self
        )
        exportAction.triggered.connect(self.exportTriggered)
        toolbar.addAction(exportAction)

        # --- separator --- #
        toolbar.addWidget(
            QtWidgets.QWidget(
                sizePolicy=QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Policy.Expanding,
                    QtWidgets.QSizePolicy.Policy.Preferred,
                )
            )
        )

        # --- reset --- #
        resetAction = QtGui.QAction(
            QtGui.QIcon.fromTheme(QtGui.QIcon.ThemeIcon.ViewRestore), "Reset", self
        )
        resetAction.triggered.connect(self.resetTriggered)
        toolbar.addAction(resetAction)

    def importTriggered(self):
        """
        Slot for toolbar's 'Import' action signal 'triggered'.

        It opens file dialog to take the file, and executes importing data.
        """

        pass

    def exportTriggered(self):
        """
        Slot for toolbar's 'Export' action signal 'triggered'.

        It opens file dialog to take filename, and executes exporting data.
        """

        fileName = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Export file",
            "./Project/ROIs.json",
            "JSON files (*.json);;Text files (*.txt *.csv)",
        )
        match fileName[0].split(".")[-1]:
            case "json":
                try:
                    files.exportJSON(
                        fileName[0], self.energy, self.Detectors, self.manualTab.table
                    )
                except Exception as e:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Export data",
                        f"An error occurred during exporting data:\n\n{e}",
                    )
                else:
                    QtWidgets.QMessageBox.information(
                        self,
                        "Export data",
                        f"Data was succesfully exported to file:\n\n{fileName[0]}",
                    )
            case "txt" | "csv":
                try:
                    pass
                except Exception as e:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Export data",
                        f"An error occurred during exporting data:\n\n{e}",
                    )
                else:
                    QtWidgets.QMessageBox.information(
                        self,
                        "Export data",
                        f"Data was succesfully exported to file:\n\n{fileName[0]}",
                    )
            case _:
                return

    def resetTriggered(self):
        """
        Slot for toolbar's 'Reset' action signal 'triggered'.

        It opens file dialog to confirm the action, and reseting whole applicataion.
        """

        if (
            QtWidgets.QMessageBox.question(
                self,
                "Reset",
                "Do you really want to reset the application?\nDefined ROIs will be lost.",
                defaultButton=QtWidgets.QMessageBox.StandardButton.No,
            )
            == QtWidgets.QMessageBox.StandardButton.Yes
        ):
            self.xrfTab.uncheckAll()
            numberOfRows = self.manualTab.table.rowCount()
            for row in range(numberOfRows + 1):
                self.manualTab.table.removeRow(numberOfRows - row)


class Detector:
    """
    Detector object for energetic callibration properties storage.
    """

    def __init__(
        self, zero=-647.684, gain=6.953, noise=140.0, fano=0.006, epsilon=3.85, N=4096
    ):
        """
        Object initialization with default callibration values.

        It sets callibration parameters:
        'zero' [eV], 'gain' [eV/channel], 'noise' [eV], and 'fano' [-];
        and detector parameters:
        'epsilon' [eV], and 'N' (number of channels) [-].
        """

        self.calibrate(zero, gain, noise, fano)
        self.epsilon = epsilon  # [eV]
        self.N = N  # [-]

    def calibrate(self, zero, gain, noise, fano):
        """
        Method for setting callibration.

        It sets callibration parameters:
        'zero' [eV], 'gain' [eV/channel], 'noise' [eV], and 'fano' [-].
        """

        self.zero = zero  # [eV]
        self.gain = gain  # [eV/ch]
        self.noise = noise  # [eV]
        self.fano = fano  # [-]

    def getEnergy(self, channel):
        """
        Method for getting energy.

        It returns energy [eV] for specified detector's channel.
        """

        return channel * self.gain + self.zero

    def getSigma(self, energy=None, *, channel=None):
        """
        Method for getting standard deviation.

        It returns standard deviation (sigma) [eV] for specified energy [eV], or channel.
        """

        if (energy is None) and (channel is not None):
            energy = channel * self.gain + self.zero
        return (
            sqrt(
                self.noise * self.noise
                + 2.355 * 2.355 * self.epsilon * self.fano * energy
            )
            / 2.335
        )

    def getChannel(self, energy):
        """
        Method for getting detector's channel.

        It returns detector's channel for specified energy [eV].
        """

        return round((energy - self.zero) / self.gain)

    def getJSON(self):
        """
        Method for generating JSON structure form detector's properties.

        It returnes JSON structure string with detector's properties.
        """

        return json.dumps(
            {
                "Zero [eV]": self.zero,
                "Gain [eV/channel]": self.gain,
                "Noise [eV]": self.noise,
                "Fano [-]": self.fano,
                "Epsilon [eV]": self.epsilon,
                "N [-]": self.N,
            }
        )


# --- --- EXECUTABLE --- --- #


# --- running the application --- #
def main():
    """
    Function for executing an application with additional command-line parameters.
    """

    parser = ArgumentParser(
        prog="XRF Spectra ROI Definer",
        description="""
        SciCompPy project application for defining energetic regions of interest (ROIs) 
        for X-ray Fluorescence spectra analysis.
        """,
    )
    parser.add_argument("-e", "--energy", required=False, help="excitation energy [eV]")
    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(args)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
