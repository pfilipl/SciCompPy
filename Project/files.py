"""
Files module for *SciCompPy project application*.

It defines input and output files handling.

---
Copyright (C) 2026 Filip J. Baran
"""

# --- --- IMPORTS --- --- #

# --- standard libraries --- #
import json

# --- 3rd party libraries --- #

# --- own files --- #
import main


# --- --- CODE --- --- #

def exportJSON(fileName, /, energy, Detectors, ROIsTable):
    """
    Function for exporting JSON file with specified name.

    It creates JSON file with information about:
    excitation energy, detectors' properties, and defined ROIs.

    ---
    Exaple result:

    {
        "Excitation energy [eV]": null,
        "Detectors": {
            "SDD1": {
            "Zero [eV]": -647.684,
            "Gain [eV/channel]": 6.953,
            "Noise [eV]": 140,
            "Fano [-]": 0.006,
            "Epsilon [eV]": 3.85,
            "N [-]": 4096
            },
            "SDD2": {
            "Zero [eV]": -647.684,
            "Gain [eV/channel]": 6.953,
            "Noise [eV]": 140,
            "Fano [-]": 0.006,
            "Epsilon [eV]": 3.85,
            "N [-]": 4096
            }
        },
        "ROIsTable": {
            "Mn_Ka": {
            "Min energy [eV]": "5823",
            "Max energy [eV]": "5967",
            "SDD1 Min channel": "931",
            "SDD1 Max channel": "951",
            "SDD2 Min channel": "931",
            "SDD2 Max channel": "951"
            },
            "Au_La": {
            "Min energy [eV]": "9631",
            "Max energy [eV]": "9777",
            "SDD1 Min channel": "1478",
            "SDD1 Max channel": "1499",
            "SDD2 Min channel": "1478",
            "SDD2 Max channel": "1499"
            },
            "U_Ma1": {
            "Min energy [eV]": "3100",
            "Max energy [eV]": "3242",
            "SDD1 Min channel": "539",
            "SDD1 Max channel": "559",
            "SDD2 Min channel": "539",
            "SDD2 Max channel": "559"
            }
        }
    }
    """

    DetectorsJSON = {}
    for name, detector in Detectors.items():
        DetectorsJSON[name] = json.loads(detector.getJSON())

    with open(fileName, "w") as file:
        file.write(
            json.dumps(
                {
                    "Excitation energy [eV]": energy * 1000
                    if energy is not None
                    else None,
                    "Detectors": DetectorsJSON,
                    "ROIsTable": json.loads(ROIsTable.getJSON()),
                }
            )
        )


# --- --- EXECUTABLE --- --- #

# --- running the application --- #
if __name__ == "__main__":
    main.main()