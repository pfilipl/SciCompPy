"""
Periodic table module for *SciCompPy project application*.

It defines periodic table widget with necessary functionality.

---
Copyright (C) 2026 Filip J. Baran
"""

# --- --- IMPORTS --- --- #

# --- libraries --- #
import xraylib
from math import ceil
from PySide6 import QtWidgets, QtCore, QtGui

# --- own files --- #
import main


# --- --- CODE --- --- #

# --- Elements' symbols and names --- #
Elements = {
    "H": "Hydrogen",
    "He": "Helium",
    "Li": "Lithium",
    "Be": "Beryllium",
    "B": "Boron",
    "C": "Carbon",
    "N": "Nitrogen",
    "O": "Oxygen",
    "F": "Fluorine",
    "Ne": "Neon",
    "Na": "Sodium",
    "Mg": "Magnesium",
    "Al": "Aluminium",
    "Si": "Silicon",
    "P": "Phosphorus",
    "S": "Sulfur",
    "Cl": "Chlorine",
    "Ar": "Argon",
    "K": "Potassium",
    "Ca": "Calcium",
    "Sc": "Scandium",
    "Ti": "Titanium",
    "V": "Vanadium",
    "Cr": "Chromium",
    "Mn": "Manganese",
    "Fe": "Iron",
    "Co": "Cobalt",
    "Ni": "Nickel",
    "Cu": "Copper",
    "Zn": "Zinc",
    "Ga": "Gallium",
    "Ge": "Germanium",
    "As": "Arsenic",
    "Se": "Selenium",
    "Br": "Bromine",
    "Kr": "Krypton",
    "Rb": "Rubidium",
    "Sr": "Strontium",
    "Y": "Yttrium",
    "Zr": "Zirconium",
    "Nb": "Niobium",
    "Mo": "Molybdenum",
    "Tc": "Technetium",
    "Ru": "Ruthenium",
    "Rh": "Rhodium",
    "Pd": "Palladium",
    "Ag": "Silver",
    "Cd": "Cadmium",
    "In": "Indium",
    "Sn": "Tin",
    "Sb": "Antimony",
    "Te": "Tellurium",
    "I": "Iodine",
    "Xe": "Xenon",
    "Cs": "Caesium",
    "Ba": "Barium",
    "La": "Lanthanum",
    "Ce": "Cerium",
    "Pr": "Praseodymium",
    "Nd": "Neodymium",
    "Pm": "Promethium",
    "Sm": "Samarium",
    "Eu": "Europium",
    "Gd": "Gadolinium",
    "Tb": "Terbium",
    "Dy": "Dysprosium",
    "Ho": "Holmium",
    "Er": "Erbium",
    "Tm": "Thulium",
    "Yb": "Ytterbium",
    "Lu": "Lutetium",
    "Hf": "Hafnium",
    "Ta": "Tantalum",
    "W": "Tungsten",
    "Re": "Rhenium",
    "Os": "Osmium",
    "Ir": "Iridium",
    "Pt": "Platinum",
    "Au": "Gold",
    "Hg": "Mercury",
    "Tl": "Thallium",
    "Pb": "Lead",
    "Bi": "Bismuth",
    "Po": "Polonium",
    "At": "Astatine",
    "Rn": "Radon",
    "Fr": "Francium",
    "Ra": "Radium",
    "Ac": "Actinium",
    "Th": "Thorium",
    "Pa": "Protactinium",
    "U": "Uranium",
    "Np": "Neptunium",
    "Pu": "Plutonium",
    "Am": "Americium",
    "Cm": "Curium",
    "Bk": "Berkelium",
    "Cf": "Californium",
    "Es": "Einsteinium",
    "Fm": "Fermium",
    "Md": "Mendelevium",
    "No": "Nobelium",
    "Lr": "Lawrencium",
    "Rf": "Rutherfordium",
    "Db": "Dubnium",
    "Sg": "Seaborgium",
    "Bh": "Bohrium",
    "Hs": "Hassium",
    "Mt": "Meitnerium",
    "Ds": "Darmstadtium",
    "Rg": "Roentgenium",
    "Cn": "Copernicium",
    "Nh": "Nihonium",
    "Fl": "Flerovium",
    "Mc": "Moscovium",
    "Lv": "Livermorium",
    "Ts": "Tennessine",
    "Og": "Oganesson",
}


# --- classes --- #
class PeriodicTables(QtWidgets.QTabWidget):
    """
    Periodic tables tab widget for specified characteristic lines.
    """

    elementToggled = QtCore.Signal(bool, str, int)

    def __init__(self, linesAndEdges, energy=None, /, parent=None):
        """
        Widget initialization with specified characteristic lines and edges.
        """

        super().__init__(parent)

        self.Tabs = dict()

        for name in linesAndEdges.keys():
            self.Tabs[name] = PeriodicTable(
                energy,
                self,
                line=linesAndEdges[name]["line"],
                edge=linesAndEdges[name]["edge"],
            )
            self.addTab(self.Tabs[name], name)

    def changeEnergy(self, energy=None):
        """
        Method for changing excitation energy.

        It enables buttons in every defined periodic table widget
        which element's energies are defined, and its absorption energy 
        is not greater than specified 'energy' [eV].
        """

        if energy is not None:
            energy /= 1000 # [eV] -> [keV] for xraylib
        for periodicTable in self.Tabs.values():
            periodicTable.elementButtonsEnabling(energy)


class PeriodicTable(QtWidgets.QWidget):
    """
    Periodic table widget with checkable elements' buttons,
    element's symbol and name panel, and X-ray Fluorescence information panel.
    """

    def __init__(self, energy=None, /, parent=None, *, line=None, edge=None):
        """
        Widget initialization with layout configuration.
        """

        super().__init__(parent)

        # --- variables --- #
        self.line = line
        self.edge = edge

        # --- --- layout  --- --- #
        # --- groups and periods labels --- #
        layout = QtWidgets.QGridLayout(self)
        for group in range(1, 19):
            layout.addWidget(
                QtWidgets.QLabel(
                    f"{group}", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
                ),
                0,
                group,
            )
        for period in range(1, 8):
            layout.addWidget(
                QtWidgets.QLabel(
                    f"{period}", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
                ),
                period,
                0,
            )
        layout.addWidget(
            QtWidgets.QLabel("", alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 8, 0
        )
        layout.addWidget(
            QtWidgets.QLabel("6", alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 9, 0
        )
        layout.addWidget(
            QtWidgets.QLabel("7", alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 10, 0
        )

        # --- elements' buttons --- #
        period = 1
        group = 1
        self.elementButtons = dict()
        for element in Elements.keys():
            self.elementButtons[element] = Element(element)
            self.elementButtons[element].hover.connect(self.elementButtonHover)
            if parent is not None:
                self.elementButtons[element].toggled.connect(lambda checked, name=element: parent.elementToggled.emit(checked, name, self.line))
            layout.addWidget(self.elementButtons[element], period, group)
            match element:
                case "H":
                    group += 17
                case "Be" | "Mg":
                    group += 11
                case "Ba" | "Ra":
                    group += 2
                    period += 3
                case "Lu" | "Lr":
                    group -= 14
                    period -= 3
                case "He" | "Ne" | "Ar" | "Kr" | "Xe" | "Rn":
                    group = 1
                    period += 1
                case _:
                    group += 1
        self.elementButtonsEnabling(energy)

        # --- element's symbol and name panel --- #
        layout_element = QtWidgets.QVBoxLayout()
        layout.addLayout(layout_element, 1, 3, 3, 4)
        self.element_symbol = QtWidgets.QLabel(
            "", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.element_name = QtWidgets.QLabel(
            "", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.element_symbol.setFont(
            QtGui.QFont(self.font().family(), self.font().pointSize() * 8)
        )
        self.element_name.setFont(
            QtGui.QFont(self.font().family(), self.font().pointSize() * 2)
        )
        layout_element.addWidget(self.element_symbol)
        layout_element.addWidget(self.element_name)
        layout_element.addWidget(QtWidgets.QLabel())

        # --- X-ray Fluorescence information panel --- #
        layout_labels = QtWidgets.QGridLayout()
        layout.addLayout(layout_labels, 1, 7, 3, 6)
        self.labels_KshellInfo = XRFinfo(
            {"K": xraylib.K_SHELL},
            {"Kα": xraylib.KA_LINE, "Kβ": xraylib.KB_LINE},
            currentEdge=self.edge,
            currentLine=self.line,
        )
        self.labels_LshellInfo = XRFinfo(
            {"L3": xraylib.L3_SHELL, "L2": xraylib.L2_SHELL},
            {"Lα": xraylib.LA_LINE, "Lβ": xraylib.LB_LINE},
            currentEdge=self.edge,
            currentLine=self.line,
        )
        self.labels_MshellInfo = XRFinfo(
            {"M5": xraylib.M5_SHELL},
            {"Mα1": xraylib.MA1_LINE},
            currentEdge=self.edge,
            currentLine=self.line,
        )
        layout_labels.addWidget(self.labels_KshellInfo)
        layout_labels.addWidget(self.labels_LshellInfo)
        layout_labels.addWidget(self.labels_MshellInfo)

        self.setLayout(layout)

    def elementButtonsEnabling(self, energy=None):
        """
        Method for enabling elements' buttons.

        It enables buttons which element's energies are defined,
        and its absorption energy is not greater than 'energy' [keV].
        """

        for element in self.elementButtons.keys():
            try:
                Z = xraylib.SymbolToAtomicNumber(element)
                if (
                    (self.line is not None) and (xraylib.LineEnergy(Z, self.line) == 0)
                ) or (
                    (self.edge is not None)
                    and (energy is not None)
                    and (xraylib.EdgeEnergy(Z, self.edge) > energy)
                ):
                    self.elementButtons[element].setEnabled(False)
                else:
                    self.elementButtons[element].setEnabled(True)
            except Exception:
                self.elementButtons[element].setEnabled(False)

    def elementButtonHover(self, state, text=None):
        """
        Slot for element's button signal 'hover'.

        It changes values in element's symbol and name panel,
        and XRF information panel.
        """

        if state and text:
            self.element_symbol.setText(text)
            self.element_name.setText(Elements[text])
            try:
                Z = xraylib.SymbolToAtomicNumber(text)
            except Exception:
                Z = -1
            self.labels_KshellInfo.setLabels(Z)
            self.labels_LshellInfo.setLabels(Z)
            self.labels_MshellInfo.setLabels(Z)
        else:
            self.element_symbol.setText("")
            self.element_name.setText("")
            self.labels_KshellInfo.setLabels()
            self.labels_LshellInfo.setLabels()
            self.labels_MshellInfo.setLabels()


class Element(QtWidgets.QPushButton):
    """
    Element's button widget with mouse hovering signal emmiting.
    """

    hover = QtCore.Signal(bool, str)

    def __init__(self, text, /, parent=None):
        """
        Widget initialization with default properties and layout configuration.
        """

        super().__init__(text, parent)

        self.setCheckable(True)
        self.setFont(
            QtGui.QFont(self.font().family(), ceil(self.font().pointSize() * 1.5))
        )

        self.setMinimumHeight(50)
        self.setMinimumWidth(50)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )

    def enterEvent(self, event):
        """
        Slot for mouse entering signal.

        It emits 'hover' signal with state 'True' and its text (element's symbol).
        """

        self.hover.emit(True, self.text())
        super().enterEvent(event)

    def leaveEvent(self, event):
        """
        Slot for mouse leaving signal.

        It emits 'hover' signal with state 'False'.
        """

        self.hover.emit(False, None)
        super().leaveEvent(event)


class XRFinfo(QtWidgets.QWidget):
    """
    X-ray Fluorescence information panel widget
    with absorption edges' and characteristic lines' energies.
    """

    def __init__(
        self, Edges, Lines, /, parent=None, *, currentLine=None, currentEdge=None
    ):
        """
        Widget initialization with edges and characteristic lines specification,
        and layout configuration.
        """

        super().__init__(parent)

        self.Edges = Edges
        self.Lines = Lines

        # --- --- layout --- --- #
        self.edgeLabels = dict()
        self.lineLabels = dict()
        layout = QtWidgets.QGridLayout(self)

        # --- edges --- #
        for iedge, edge in enumerate(self.Edges.keys()):
            self.edgeLabels[edge] = {
                "label": QtWidgets.QLabel(
                    f"{edge} edge:",
                    alignment=QtCore.Qt.AlignmentFlag.AlignVCenter
                    | QtCore.Qt.AlignmentFlag.AlignRight,
                ),
                "energy": QtWidgets.QLabel(
                    "", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
                ),
                "unit": QtWidgets.QLabel(
                    "keV",
                    alignment=QtCore.Qt.AlignmentFlag.AlignVCenter
                    | QtCore.Qt.AlignmentFlag.AlignLeft,
                ),
            }
            self.edgeLabels[edge]["label"].setMinimumWidth(50)
            self.edgeLabels[edge]["energy"].setMinimumWidth(50)
            self.edgeLabels[edge]["unit"].setMinimumWidth(30)
            if (currentEdge is not None) and (currentEdge != self.Edges[edge]):
                self.edgeLabels[edge]["label"].setEnabled(False)
                self.edgeLabels[edge]["energy"].setEnabled(False)
                self.edgeLabels[edge]["unit"].setEnabled(False)
            layout.addWidget(self.edgeLabels[edge]["label"], iedge, 0)
            layout.addWidget(self.edgeLabels[edge]["energy"], iedge, 1)
            layout.addWidget(self.edgeLabels[edge]["unit"], iedge, 2)

        # --- characteristic lines --- #
        for iline, line in enumerate(self.Lines.keys()):
            self.lineLabels[line] = {
                "label": QtWidgets.QLabel(
                    f"{line}:",
                    alignment=QtCore.Qt.AlignmentFlag.AlignVCenter
                    | QtCore.Qt.AlignmentFlag.AlignRight,
                ),
                "energy": QtWidgets.QLabel(
                    "", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
                ),
                "unit": QtWidgets.QLabel(
                    "keV",
                    alignment=QtCore.Qt.AlignmentFlag.AlignVCenter
                    | QtCore.Qt.AlignmentFlag.AlignLeft,
                ),
            }
            self.lineLabels[line]["label"].setMinimumWidth(50)
            self.lineLabels[line]["energy"].setMinimumWidth(50)
            self.lineLabels[line]["unit"].setMinimumWidth(30)
            if (currentLine is not None) and (currentLine != self.Lines[line]):
                self.lineLabels[line]["label"].setEnabled(False)
                self.lineLabels[line]["energy"].setEnabled(False)
                self.lineLabels[line]["unit"].setEnabled(False)
            layout.addWidget(self.lineLabels[line]["label"], iline, 3)
            layout.addWidget(self.lineLabels[line]["energy"], iline, 4)
            layout.addWidget(self.lineLabels[line]["unit"], iline, 5)

        self.setLayout(layout)

    def setLabels(self, Z=None):
        """
        Setting values for absorption edges' and characteristic lines' energies.
        """

        # --- edges --- #
        for edge in self.Edges.keys():
            if Z is None:
                self.edgeLabels[edge]["energy"].setText("")
                continue
            try:
                self.edgeLabels[edge]["energy"].setText(
                    f"{xraylib.EdgeEnergy(Z, self.Edges[edge]):.4f}"
                )
            except Exception:
                self.edgeLabels[edge]["energy"].setText("NaN")

        # --- characteristic lines --- #
        for line in self.Lines.keys():
            if Z is None:
                self.lineLabels[line]["energy"].setText("")
                continue
            try:
                self.lineLabels[line]["energy"].setText(
                    f"{xraylib.LineEnergy(Z, self.Lines[line]):.4f}"
                )
            except Exception:
                self.lineLabels[line]["energy"].setText("NaN")


# --- --- EXECUTABLE --- --- #

# --- running the application --- #
if __name__ == "__main__":
    main.main()
