# Python Script Instructions

## Prerequisites

Make sure you have the following installed:
- [Python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [pandas](https://pypi.org/project/pandas/)
- [prettytable](https://pypi.org/project/prettytable/)

## Usage

Download the following CSV files from [wago.tools](https://wago.tools/db2) to this directory
```
ProfessionEffect
ProfessionEffectType
ProfessionTrait
ProfessionTraitXEffect
ProfessionTraitXLabel
SpellLabel
TraitCond
TraitDefinition
TraitNodeEntry
TraitNodeGroupXTraitNode
TraitNodeXTraitCond
TraitNodeXTraitNodeEntry
```

To build the sqlite db, use the following command, passing the downloaded build version:

```sh
python generate_database.py 11.0.2.55959
```

To generate the spreadsheet, use the following command, passing the downloaded build version:

```sh
python generate_spreadsheet.py
```