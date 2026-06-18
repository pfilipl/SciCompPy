"""
Main module for *SciCompPy project application*.

---
Copyright (C) 2026 Filip J. Baran
"""

# --- --- IMPORTS --- --- #

# --- libraries --- #
import sys
import json
import xraylib
from numpy import sqrt
from argparse import ArgumentParser
from PySide6 import QtWidgets

# --- own files --- #
import periodic_table
import manual


# --- --- CODE --- --- #


# --- classes --- #
class MainWindow(QtWidgets.QMainWindow):
    """
    Main window widget.
    """

    def __init__(self, args, /, parent=None):
        """
        Widget initialization with layout configuration.
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
        mainWidget.addTab(self.manualTab, "Manual")

        # mainWidget.addTab(self.xrfTab, "XRF lines")

    def exportJSON(self, fname):
        """
        Method for exporting JSON file with specified name.

        It creates JSON file with information about:
        excitation energy, detectors' properties, and defined ROIs.
        """

        Detectors = {}
        for detectorName, detector in self.Detectors.items():
            Detectors[detectorName] = json.loads(detector.getJSON())

        with open(fname, "w") as file:
            file.write(
                json.dumps(
                    {
                        "Excitation energy [eV]": self.energy * 1000,
                        "Detectors": Detectors,
                        "ROIsTable": json.loads(self.manualTab.table.getJSON()),
                    }
                )
            )


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
