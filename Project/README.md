
# <img src="icon.png" width="128"> XRF Spectra ROI Definer

![MIT License](https://img.shields.io/badge/License-MIT-green.svg)

*SciCompPy project application* for defining energetic regions of interest (ROIs)
for X-ray Fluorescence spectra analysis.

© Filip J. Baran 2026

## Installation and starting

Create virtual enviroment for the application and install libraries with specified below versions:
- python = ">=3.14.3,<3.15",
- xraylib = ">=4.2.1,<5",
- pyside6 = ">=6.11.1,<7".

Download application's files and start by typing `python main.py` with available options:
- `-h, --help` show help message and exit,
- `-e, --energy ENERGY` define excitation energy in eV,
- `-r, --returning {vars,json}` set returning data to console: 'vars' for variables, 'json' for JSON string.

Starting command structure is shown below:
```bash
python main.py [-h] [-e ENERGY] [-r {vars,json}]
```

## Example usage

After starting, for example with specified exciting energy equal to 12500 eV, a window with periodic table opens.

<img src="screenshots/xrfTab.png">

While the mouse is over an element, the information about its name, absorption edges and characteristic lines energies is showing.

For choosing a standard elemental ROI, the corresponding button must be toggled. 

<img src="screenshots/xrfTab_Cr.png">

If a button is gray and it don't toggle, it means that the excitation energy is too small for the corresponding element's characteristic line. It can be changed by pressing "Energy" button at the toolbar.

By default, the application is showing a periodic table for Kα characteristic lines, but if other lines are interesting the appropirate table can be opened by choosing a tab:

<img src="screenshots/xrfTab_Cr_arrow.png">

Then, another standard characteristic line ROI can be choosen.

<img src="screenshots/xrfTab_Au.png">

If the interesting ROI is not standard, it can be defined manually by pressing "Manual" tab:

<img src="screenshots/xrfTab_Au_arrow.png">

The already defined ROIs are presented in the table with its name, energy range, and channels range for all defined detectors.

<img src="screenshots/manualTab_Cr-Au.png">

~~The properties of detectors can be changed by pressing "Detectors" button at the toolbar.~~ (it will be implemented in the future)

To define a ROI manualy, the form above the table must be filled with apropriate values, and "Add ROI" button must be pressed. Two modes of energy definition can be choosen:
- energy line in eV and its width defined by:
  - standard deviation calculated by the application (only id detectors are defined),
  - energy in eV.
- energy range in eV.

<img src="screenshots/manualTab_Cr-Au-ExampleROI.png">

If the user try to add a ROI with the name that already exists, the application detects it and adds a suffix to the name.

<img src="screenshots/manualTab_Cr-Au-ExampleROI-2.png">

At every moment, defined ROIs can be exported to a JSON file or imported from a JSON file by pressing "Export" or "Import" buttons at the toolbar.

Additionally, the application can be reseted to the default values and properties by pressing "Reset" button at the toolbar. 