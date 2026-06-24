"""
Manual module for *SciCompPy project application*.

It defines form widget with necessary functionality.

---
Copyright (C) 2026 Filip J. Baran
"""

# --- --- IMPORTS --- --- #

# --- standard libraries --- #
import json
from math import ceil
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

        # --- --- layout --- --- #
        layout = QtWidgets.QVBoxLayout(self)
        layout_form = QtWidgets.QGridLayout()
        layout.addLayout(layout_form)

        # --- manual form --- #
        # radio buttons groups #
        self.manualDefiningType = QtWidgets.QButtonGroup(self, exclusive=True)
        self.manualWidthType = QtWidgets.QButtonGroup(self, exclusive=True)

        # name #
        self.manualName = QtWidgets.QLineEdit(
            placeholderText="Name...", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.manualName.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.manualName.setFont(
            QtGui.QFont(self.font().family(), ceil(self.font().pointSize() * 1.5))
        )

        # line and width radio #
        self.manualLineRadio = QtWidgets.QRadioButton("Line and width")
        self.manualLineRadio.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.manualLineRadio.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred
        )
        self.manualLineRadio.setChecked(True)
        self.manualDefiningType.addButton(self.manualLineRadio)

        # line #
        self.manualLine = QtWidgets.QSpinBox(
            prefix="E = ", suffix=" eV", minimum=0, maximum=100000
        )
        self.manualLine.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.manualLine.returnPressed.connect(self.manualLineRadio.toggle)

        # width by sigma radio #
        self.manualWidthSigmaRadio = QtWidgets.QRadioButton()
        self.manualWidthSigmaRadio.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred
        )
        self.manualWidthType.addButton(self.manualWidthSigmaRadio)
        if Detectors == {}:
            self.manualWidthSigmaRadio.setEnabled(False)
        else:
            self.manualWidthSigmaRadio.setChecked(True)

        # width by sigma #
        self.manualWidthSigma = QtWidgets.QDoubleSpinBox(
            prefix="± ", suffix=" σ", minimum=0.0, value=0.5, maximum=5, singleStep=0.01
        )
        self.manualWidthSigma.returnPressed.connect(self.manualLineRadio.toggle)
        self.manualWidthSigma.returnPressed.connect(self.manualWidthSigmaRadio.toggle)
        if Detectors == {}:
            self.manualWidthSigma.setEnabled(False)

        # width by energy radio #
        self.manualWidthEnergyRadio = QtWidgets.QRadioButton()
        self.manualWidthEnergyRadio.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred
        )
        self.manualWidthType.addButton(self.manualWidthEnergyRadio)
        if Detectors == {}:
            self.manualWidthEnergyRadio.setChecked(True)

        # width by energy #
        self.manualWidthEnergy = QtWidgets.QSpinBox(
            prefix="± ", suffix=" eV", minimum=0, value=50, maximum=50000
        )
        self.manualWidthEnergy.returnPressed.connect(self.manualLineRadio.toggle)
        self.manualWidthEnergy.returnPressed.connect(self.manualWidthEnergyRadio.toggle)

        # energy range radio #
        self.manualEnergyRangeRadio = QtWidgets.QRadioButton("Energy range")
        self.manualEnergyRangeRadio.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft
        )
        self.manualEnergyRangeRadio.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred
        )
        self.manualDefiningType.addButton(self.manualEnergyRangeRadio)

        # energy range minimum #
        self.manualEnergyRangeMin = QtWidgets.QSpinBox(
            prefix="Emin = ", suffix=" eV", minimum=0, maximum=100000
        )
        self.manualEnergyRangeMin.returnPressed.connect(
            self.manualEnergyRangeRadio.toggle
        )

        # energy range maximum #
        self.manualEnergyRangeMax = QtWidgets.QSpinBox(
            prefix="Emax = ", suffix=" eV", minimum=0, maximum=100000
        )
        self.manualEnergyRangeMax.returnPressed.connect(
            self.manualEnergyRangeRadio.toggle
        )

        # add ROI button #
        self.manualAddROI = QtWidgets.QPushButton("Add\nROI")
        self.manualAddROI.setFont(
            QtGui.QFont(self.font().family(), ceil(self.font().pointSize() * 1.5))
        )
        self.manualAddROI.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.manualAddROI.pressed.connect(self.pressManualAddROI)

        # placing widgets in layout grid #
        layout_form.addWidget(self.manualName, 1, 0, 3, 2)
        layout_form.addWidget(self.manualLineRadio, 1, 3, 2, 1)
        layout_form.addWidget(self.manualLine, 1, 4, 2, 1)
        layout_form.addWidget(self.manualWidthSigma, 1, 5, 1, 1)
        layout_form.addWidget(self.manualWidthSigmaRadio, 1, 6, 1, 1)
        layout_form.addWidget(self.manualWidthEnergy, 2, 5, 1, 1)
        layout_form.addWidget(self.manualWidthEnergyRadio, 2, 6, 1, 1)
        layout_form.addWidget(self.manualEnergyRangeRadio, 3, 3, 1, 1)
        layout_form.addWidget(self.manualEnergyRangeMin, 3, 4, 1, 1)
        layout_form.addWidget(self.manualEnergyRangeMax, 3, 5, 1, 1)
        layout_form.addWidget(self.manualAddROI, 1, 7, 3, 1)

        # --- ROIs table --- #
        self.table = ROIsTable(Detectors, parent=self)
        self.table.cellChanged.connect(lambda row, column: self.ROIChanged(row, column))
        self.table.horizontalHeader().sectionDoubleClicked.connect(
            lambda column: self.table.sortByColumn(
                column, QtCore.Qt.SortOrder.AscendingOrder
            )
        )
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

    def ROIChanged(self, row, column):
        """
        Slot for ROIs table signal 'cellChanged'.

        It adds '_edited' to ROI's name if ROI's parametres was changed.
        """

        if column > 0:
            changedIitem = self.table.item(row, column)
            nameItem = self.table.item(row, 0)
            if changedIitem in self.table.selectedItems() and nameItem is not None:
                if nameItem.text().split("_")[-1] != "edited":
                    nameItem.setText(nameItem.text() + "_edited")

    def pressManualAddROI(self):
        """
        Slot for manual Add ROI button signal 'pressed'.

        It adds manually defined ROI to ROIs table.
        """

        ROIName = self.manualName.text()
        ROIData = {
            "DefiningType": "line" if self.manualLineRadio.isChecked() else "range",
            "WidthType": "sigma"
            if self.manualWidthSigmaRadio.isChecked()
            else "energy",
            "Line": self.manualLine.value(),
            "WidthSigma": self.manualWidthSigma.value(),
            "WidthEnergy": self.manualWidthEnergy.value(),
            "EnergyRangeMin": self.manualEnergyRangeMin.value(),
            "EnergyRangeMax": self.manualEnergyRangeMax.value(),
        }

        try:
            self.table.addROI(ROIName, ROIData, parent=self)
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self, "ROI adding", f"An error occurred during adding a ROI:\n\n{e}"
            )


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

        # --- --- importing --- --- #
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
                        tempItem = QtWidgets.QTableWidgetItem()
                        tempItem.setData(
                            QtCore.Qt.ItemDataRole.DisplayRole, int(ROIData[key])
                        )
                        self.setItem(self.rowCount() - 1, 1 + ikey, tempItem)
            except Exception:
                self.insertRow(self.rowCount())
                self.setItem(
                    self.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(ROIName)
                )
                for ikey, key in enumerate(ROIData.keys()):
                    tempItem = QtWidgets.QTableWidgetItem()
                    tempItem.setData(
                        QtCore.Qt.ItemDataRole.DisplayRole, int(ROIData[key])
                    )
                    self.setItem(self.rowCount() - 1, 1 + ikey, tempItem)
        
        # --- --- manual adding --- --- #
        else:
            # --- ROI's name --- #
            if ROIName == "":
                ROIName = "ROI"

            try:
                name, tabName = ROIName.split("_")
                if name in periodic_table.Elements.keys() and tabName in [
                    "Kα",
                    "Kβ",
                    "Lα",
                    "Lβ",
                    "Mα1",
                ]:
                    ROIName += "_manual"
            except Exception:
                pass

            ROINameRegex = QtCore.QRegularExpression(
                f"^{QtCore.QRegularExpression.escape(ROIName)}(?:_\\d+)?$"
            )
            sameNameROIsNumber = len(
                self.findItems(
                    ROINameRegex.pattern(), QtCore.Qt.MatchFlag.MatchRegularExpression
                )
            )
            if sameNameROIsNumber:
                ROIName += f"_{sameNameROIsNumber}"

            self.insertRow(self.rowCount())
            self.setItem(self.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(ROIName))

            # --- adding by energy line --- #
            if ROIData["DefiningType"] == "line":
                energy = ROIData["Line"]

                # ROI's width in channels #
                if self.Detectors == {} or ROIData["WidthType"] == "energy":
                    sigma = [ROIData["WidthEnergy"]]
                elif self.Detectors != {} and ROIData["WidthType"] == "sigma":
                    sigma = []
                    for idetector, detector in enumerate(self.Detectors.values()):
                        sigma.append(detector.getSigma(energy))
                        tempItemMinus = QtWidgets.QTableWidgetItem()
                        tempItemMinus.setData(
                            QtCore.Qt.ItemDataRole.DisplayRole,
                            int(
                                detector.getChannel(
                                    energy - sigma[-1] * 2.355 * ROIData["WidthSigma"]
                                )
                            ),
                        )
                        self.setItem(
                            self.rowCount() - 1, 3 + idetector * 2, tempItemMinus
                        )
                        tempItemPlus = QtWidgets.QTableWidgetItem()
                        tempItemPlus.setData(
                            QtCore.Qt.ItemDataRole.DisplayRole,
                            int(
                                detector.getChannel(
                                    energy + sigma[-1] * 2.355 * ROIData["WidthSigma"]
                                )
                            ),
                        )
                        self.setItem(
                            self.rowCount() - 1, 3 + idetector * 2 + 1, tempItemPlus
                        )
                else:
                    raise ValueError(
                        f"Undefined WidthType while manual adding ROI: {ROIData['WidthType']!r}."
                    )

                # fmean ROI's width in energy #
                tempItemMinus = QtWidgets.QTableWidgetItem()
                tempItemMinus.setData(
                    QtCore.Qt.ItemDataRole.DisplayRole,
                    int(energy - fmean(sigma) * 2.355 * ROIData["WidthSigma"]),
                )
                self.setItem(self.rowCount() - 1, 1, tempItemMinus)
                tempItemPlus = QtWidgets.QTableWidgetItem()
                tempItemPlus.setData(
                    QtCore.Qt.ItemDataRole.DisplayRole,
                    int(energy + fmean(sigma) * 2.355 * ROIData["WidthSigma"]),
                )
                self.setItem(self.rowCount() - 1, 2, tempItemPlus)

            # --- by energy range --- #
            elif ROIData["DefiningType"] == "range":
                energyMin = min(ROIData["EnergyRangeMin"], ROIData["EnergyRangeMax"])
                energyMax = max(ROIData["EnergyRangeMin"], ROIData["EnergyRangeMax"])

                # ROI's width in channels #
                if self.Detectors != {}:
                    for idetector, detector in enumerate(self.Detectors.values()):
                        tempItemMinus = QtWidgets.QTableWidgetItem()
                        tempItemMinus.setData(
                            QtCore.Qt.ItemDataRole.DisplayRole,
                            int(detector.getChannel(energyMin)),
                        )
                        self.setItem(
                            self.rowCount() - 1, 3 + idetector * 2, tempItemMinus
                        )
                        tempItemPlus = QtWidgets.QTableWidgetItem()
                        tempItemPlus.setData(
                            QtCore.Qt.ItemDataRole.DisplayRole,
                            int(detector.getChannel(energyMax)),
                        )
                        self.setItem(
                            self.rowCount() - 1, 3 + idetector * 2 + 1, tempItemPlus
                        )

                # ROI's width in energy #
                tempItemMinus = QtWidgets.QTableWidgetItem()
                tempItemMinus.setData(
                    QtCore.Qt.ItemDataRole.DisplayRole, int(energyMin)
                )
                self.setItem(self.rowCount() - 1, 1, tempItemMinus)
                tempItemPlus = QtWidgets.QTableWidgetItem()
                tempItemPlus.setData(QtCore.Qt.ItemDataRole.DisplayRole, int(energyMax))
                self.setItem(self.rowCount() - 1, 2, tempItemPlus)

            else:
                raise ValueError(
                    f"Undefined DefiningType while manual adding ROI: {ROIData['DefiningType']!r}."
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
                tempItemMinus = QtWidgets.QTableWidgetItem()
                tempItemMinus.setData(
                    QtCore.Qt.ItemDataRole.DisplayRole,
                    int(detector.getChannel(energy - sigma[-1] * 2.355 / 2)),
                )
                self.setItem(self.rowCount() - 1, 3 + idetector * 2, tempItemMinus)
                tempItemPlus = QtWidgets.QTableWidgetItem()
                tempItemPlus.setData(
                    QtCore.Qt.ItemDataRole.DisplayRole,
                    int(detector.getChannel(energy + sigma[-1] * 2.355 / 2)),
                )
                self.setItem(self.rowCount() - 1, 3 + idetector * 2 + 1, tempItemPlus)

        # --- fmean ROI's width in energy --- #
        tempItemMinus = QtWidgets.QTableWidgetItem()
        tempItemMinus.setData(
            QtCore.Qt.ItemDataRole.DisplayRole, int(energy - fmean(sigma) * 2.355 / 2)
        )
        self.setItem(self.rowCount() - 1, 1, tempItemMinus)
        tempItemPlus = QtWidgets.QTableWidgetItem()
        tempItemPlus.setData(
            QtCore.Qt.ItemDataRole.DisplayRole, int(energy + fmean(sigma) * 2.355 / 2)
        )
        self.setItem(self.rowCount() - 1, 2, tempItemPlus)

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
