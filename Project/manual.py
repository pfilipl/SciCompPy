"""
Manual module for *SciCompPy project application*.

It defines form widget with necessary functionality.

---
Copyright (C) 2026 Filip J. Baran
"""

# --- --- IMPORTS --- --- #

# --- standard libraries --- #
import json
from statistics import fmean

# --- 3rd party libraries --- #
import xraylib
from PySide6 import QtWidgets, QtCore, QtGui

# --- own files --- #
import main
import periodic_table


# --- --- CODE --- --- #


# --- classes --- #
class Manual(QtWidgets.QWidget):
    """
    Manual tab widget for ROIs configuration,
    theirs parameters visualisation, importing, and exporting.
    """

    checkElement = QtCore.Signal(bool, str, str)

    def __init__(self, Detectors={}, /, parent=None):
        """
        Widget initialization with layout configuration.
        """

        super().__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)
        layout_form = QtWidgets.QGridLayout()
        layout.addLayout(layout_form)
        self.table = ROIsTable(Detectors, parent=self)
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

    def __init__(self, Detectors={}, /, parent=None):
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

        # --- 'Delete' key press detection --- #
        def eventFilterMethod():
            selectedRows = list(set([item.row() for item in self.selectedItems()]))
            for row in sorted(selectedRows, reverse=True):
                self.deleteROI(row, parent)

        self.installEventFilter(
            EventFilter(
                QtGui.QKeyEvent(
                    QtCore.QEvent.Type.KeyPress,
                    QtCore.Qt.Key.Key_Delete,
                    QtCore.Qt.KeyboardModifier.NoModifier,
                    "\u007f",
                ),
                eventFilterMethod,
                self,
            )
        )

    def addROI(self, ROIName, ROIData, importing=False, /, parent=None):
        """
        Method for adding manual ROI.

        It adds a row to ROIs table with ROIName, and ROIData
        including energy range, and channel range for specified detectors.
        """

        if importing:
            try:
                name, tabName = ROIName.split("_")
                if (
                    name in periodic_table.Elements.keys()
                    and tabName in ["Kα", "Kβ", "Lα", "Lβ", "Mα1"]
                    and parent is not None
                ):
                    parent.checkElement.emit(True, name, tabName)
                else:
                    self.insertRow(self.rowCount())
                    self.setItem(
                        self.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(ROIName)
                    )
                    for ikey, key in enumerate(ROIData.keys()):
                        self.setItem(
                            self.rowCount() - 1,
                            1 + ikey,
                            QtWidgets.QTableWidgetItem(ROIData[key]),
                        )
            except Exception:
                self.insertRow(self.rowCount())
                self.setItem(
                    self.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(ROIName)
                )
                for ikey, key in enumerate(ROIData.keys()):
                    self.setItem(
                        self.rowCount() - 1,
                        1 + ikey,
                        QtWidgets.QTableWidgetItem(ROIData[key]),
                    )
        else:
            # self.insertRow(self.rowCount())
            # self.setItem(self.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(ROIName))
            pass

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

    def deleteROI(self, row, /, parent=None):
        """
        Method for deleting manual ROI.

        It deletes a 'row' form ROIs table and uncheck element's button
        if corresponding ROI is standard element's line ROI.
        """

        ROI = self.item(row, 0)
        if ROI is not None:
            try:
                name, tabName = ROI.text().split("_")
                if (
                    name in periodic_table.Elements.keys()
                    and tabName in ["Kα", "Kβ", "Lα", "Lβ", "Mα1"]
                    and parent is not None
                ):
                    parent.checkElement.emit(False, name, tabName)
                else:
                    self.removeRow(row)
            except Exception:
                self.removeRow(row)
        else:
            self.removeRow(row)

    def getElementROIName(self, name, line):
        """
        Method for creating standard element's line ROI name.

        It returns string concatenation of element's symbol and characteristic line suffix.
        """

        match line:
            case xraylib.KA_LINE:
                return name + "_Kα"
            case xraylib.KB_LINE:
                return name + "_Kβ"
            case xraylib.LA_LINE:
                return name + "_Lα"
            case xraylib.LB_LINE:
                return name + "_Lβ"
            case xraylib.MA1_LINE:
                return name + "_Mα1"
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
            energy = xraylib.LineEnergy(Z, line) * 1000
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self, "ROI adding", f"An error occurred during adding a ROI:\n\n{e}"
            )
            return

        # --- --- creating ROI --- --- #
        # --- name --- #
        ROIName = self.getElementROIName(name, line)
        self.insertRow(self.rowCount())
        self.setItem(self.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(ROIName))

        # --- ROI's width in channels --- #
        if self.Detectors == {}:
            sigma = [100]
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

        # --- fmean ROI's widht in energy --- #
        self.setItem(
            self.rowCount() - 1,
            1,
            QtWidgets.QTableWidgetItem(f"{energy - fmean(sigma) * 2.355 / 2:.0f}"),
        )
        self.setItem(
            self.rowCount() - 1,
            2,
            QtWidgets.QTableWidgetItem(f"{energy + fmean(sigma) * 2.355 / 2:.0f}"),
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

    def getJSON(self):
        """
        Method for generating JSON structure from ROIsTable.

        It returnes JSON structure string form DataFrame
        which contains information about ROIs in ROIsTable.
        """

        ROIsTableHeaders = []
        for column in range(1, self.columnCount()):
            item = self.horizontalHeaderItem(column)
            ROIsTableHeaders.append(
                item.text().replace("\n", " ")
                if type(item) is QtWidgets.QTableWidgetItem
                else ""
            )

        ROIsTableNames = []
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            ROIsTableNames.append(
                item.text() if type(item) is QtWidgets.QTableWidgetItem else ""
            )

        ROIs = []
        for row in range(self.rowCount()):
            ROI = []
            for iheader, header in enumerate(ROIsTableHeaders):
                item = self.item(row, 1 + iheader)
                ROI.append(item.text() if item is not None else None)
            ROIs.append(dict(zip(ROIsTableHeaders, ROI)))

        return json.dumps(dict(zip(ROIsTableNames, ROIs)))


class EventFilter(QtCore.QObject):
    """
    Event filter object for filtering events
    and executing assigned to them methods.
    """

    def __init__(self, filter, method, /, parent=None):
        """
        Object initialization with specified filter and method.
        """

        super().__init__(parent)

        self.filter = filter
        self.method = method

    def eventFilter(self, widget, event):
        """
        Overwrited method for filtering events
        and executing assigned methods.
        """

        if event.__repr__() == self.filter.__repr__():
            self.method()
        return False


# --- --- EXECUTABLE --- --- #

# --- running the application --- #
if __name__ == "__main__":
    main.main()
