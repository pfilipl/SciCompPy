"""
Manual module for *SciCompPy project application*.

It defines form widget with necessary functionality.

---
Copyright (C) 2026 Filip J. Baran
"""

# --- --- IMPORTS --- --- #

# --- libraries --- #
import xraylib
from numpy import mean
from PySide6 import QtWidgets, QtCore

# --- own files --- #
import main


# --- --- CODE --- --- #


# --- classes --- #
class Manual(QtWidgets.QWidget):
    """
    Manual tab widget for ROIs configuration,
    theirs parameters visualisation, importing, and exporting.
    """

    def __init__(self, Detectors={}, parent=None):
        """
        Widget initialization with layout configuration.
        """

        super().__init__(parent)

        self.table = ROIsTable(Detectors)

        layout = QtWidgets.QVBoxLayout(self)
        layout_form = QtWidgets.QGridLayout()
        layout.addLayout(layout_form)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def toglleElementROI(self, checked, name, line):
        """
        Slot for element's button signal 'toggled'.

        It adds standard element's line ROI to ROIs table, or deletes it.
        """

        if checked:
            self.table.addElementROI(name, line)
        else:
            self.table.deleteElementROI(name, line)


class ROIsTable(QtWidgets.QTableWidget):
    """
    ROIs table widget for theirs parameters visualisation.
    """

    def __init__(self, Detectors={}, parent=None):
        """
        Widget initialization with specified detectors.
        """

        self.Detectors = Detectors

        super().__init__(0, 3 + 2 * len(self.Detectors), parent)

        self.setHorizontalHeaderLabels(
            ["ROI name", "Min energy [eV]", "Max energy [eV]"]
        )
        if self.Detectors is not None:
            for iname, name in enumerate(self.Detectors.keys()):
                self.setHorizontalHeaderItem(
                    3 + 2 * iname, QtWidgets.QTableWidgetItem(f"{name}\nMin channel")
                )
                self.setHorizontalHeaderItem(
                    3 + 2 * iname + 1,
                    QtWidgets.QTableWidgetItem(f"{name}\nMax channel"),
                )
        # self.setHorizontalHeaderItem(3 + 2 * len(self.Detectors), QtWidgets.QTableWidgetItem(""))
        # self.horizontalHeader().setStretchLastSection(True)

    def getElementROIName(self, name, line):
        """
        Method for creating standard element's line ROI name.

        It returns string concatenation of element's symbol and characteristic line suffix.
        """

        match line:
            case xraylib.KA_LINE:
                return name + "_Ka"
            case xraylib.KB_LINE:
                return name + "_Kb"
            case xraylib.LA_LINE:
                return name + "_La"
            case xraylib.LB_LINE:
                return name + "_Lb"
            case xraylib.MA1_LINE:
                return name + "_Ma1"
            case _:
                return name

    def addElementROI(self, name, line):
        """
        Method for adding standard element's line ROI.

        It adds a row to ROIs table with name, energy range,
        and channel range for specified detectors.
        """

        # --- characteristic energy --- #
        try:
            Z = xraylib.SymbolToAtomicNumber(name)
            energy = xraylib.LineEnergy(Z - 10, line) * 1000
        except Exception as e:
            QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Icon.Warning,
                "ROI adding",
                f"An error occurred during adding a ROI:\n\n{e}",
                buttons=QtWidgets.QMessageBox.StandardButton.Ok,
            ).exec()
            return

        # --- --- creating ROI --- --- #
        # --- name --- #
        ROIName = self.getElementROIName(name, line)
        self.insertRow(self.rowCount())
        self.setItem(self.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(ROIName))

        # --- ROI's width in channels --- #
        if self.Detectors == {}:
            sigma = 100
        else:
            sigma = []
            for idetector, detector in enumerate(self.Detectors.values()):
                sigma.append(detector.getSigma(energy))
                self.setItem(
                    self.rowCount() - 1,
                    3 + idetector * 2,
                    QtWidgets.QTableWidgetItem(
                        f"{detector.getChannel(energy - sigma[-1] * 2.355 / 2):d}"
                    ),
                )
                self.setItem(
                    self.rowCount() - 1,
                    3 + idetector * 2 + 1,
                    QtWidgets.QTableWidgetItem(
                        f"{detector.getChannel(energy + sigma[-1] * 2.355 / 2):d}"
                    ),
                )

        # --- mean ROI's widht in energy --- #
        self.setItem(
            self.rowCount() - 1,
            1,
            QtWidgets.QTableWidgetItem(f"{energy - mean(sigma) * 2.355 / 2:.0f}"),
        )
        self.setItem(
            self.rowCount() - 1,
            2,
            QtWidgets.QTableWidgetItem(f"{energy + mean(sigma) * 2.355 / 2:.0f}"),
        )

        # --- text alignment --- #
        # for item in (
        #     self.item(self.rowCount() - 1, column)
        #     for column in range(self.columnCount() - 1)
        # ):
        for item in (
            self.item(self.rowCount() - 1, column)
            for column in range(self.columnCount())
        ):
            if item is not None:
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def deleteElementROI(self, name, line):
        """
        Method for deleting standard element's line ROI.

        It deletes a row form ROIs table which ROI's name match exactly
        to specified element and its characteristic line.
        """

        ROIName = self.getElementROIName(name, line)

        for item in self.findItems(ROIName, QtCore.Qt.MatchFlag.MatchExactly):
            self.removeRow(item.row())


# --- --- EXECUTABLE --- --- #

# --- running the application --- #
if __name__ == "__main__":
    main.main()
