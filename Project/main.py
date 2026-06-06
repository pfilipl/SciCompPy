import sys
from PySide6 import QtWidgets

import periodic_table


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("XRF spectra ROI definer")
        self.setCentralWidget(periodic_table.PeriodicTable())
        self.setFixedSize(1000, 600)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
