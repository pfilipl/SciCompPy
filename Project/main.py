"""
Main module for *SciCompPy project application*.

---
Copyright (C) 2026 Filip J. Baran
"""

# --- --- IMPORTS --- --- #

# --- libraries --- #
import sys
import xraylib
from numpy import sqrt
from argparse import ArgumentParser
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

        # --- command line arguments --- #
        try:
            energy = float(args.energy) / 1000  # [eV] -> [keV] for xraylib
        except Exception:
            energy = None

        # --- variables --- #
        self.Detectors = {"SDD1": Detector(), "SDD2": Detector()}

        # --- --- layout --- --- #
        self.setWindowTitle("SciCompPy project app: XRF Spectra ROI Definer")
        self.setFixedSize(1000, 600)

        # --- central widget --- #
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
            energy,
        )
        mainWidget.addTab(self.xrfTab, "XRF lines")

        # --- manual tab --- #
        mainWidget.addTab(
            QtWidgets.QLabel(
                "Temporary widget", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
            ),
            "Manual",
        )


class Detector:
    """
    Detector object for energetic callibration properties storage.
    """

    def __init__(
        self, zero=-647.684, gain=6.953, noise=140, fano=0.006, epsilon=3.85, N=4096
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
            sqrt(self.noise ^ 2 + 2.355 ^ 2 * self.epsilon * self.fano * energy) / 2.335
        )

    def getChannel(self, energy):
        """
        Method for getting detector's channel.

        It returns detector's channel for specified energy [eV].
        """

        return round((energy - self.zero) / self.gain)


# --- --- EXECUTABLE --- --- #


# --- running the application --- #
def main():
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
