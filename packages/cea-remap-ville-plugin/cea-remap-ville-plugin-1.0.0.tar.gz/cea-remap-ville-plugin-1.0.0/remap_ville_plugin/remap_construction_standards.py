"""
Map the field ``typology.df:STANDARD`` to the new value, based on

- construction (BAU / NEP)
- year (2040 / 2060)
- district-archetype (URB, SURB, RRL)

This can be done on a new scenario, _before_ running archetypes-mapper.
"""
import os

import pandas as pd

import cea.config
import cea.inputlocator
import cea.utilities.dbf

__author__ = "Daren Thomas"
__copyright__ = "Copyright 2021, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Daren Thomas"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def main(config):
    district_archetype = config.remap_ville_scenarios.district_archetype
    year = config.remap_ville_scenarios.year
    construction = config.remap_ville_scenarios.construction

    locator = cea.inputlocator.InputLocator(scenario=config.scenario, plugins=config.plugins)

    mapping = read_mapping()
    typology = cea.utilities.dbf.dbf_to_dataframe(locator.get_building_typology())

    for index, row in typology.iterrows():
        building = row.Name
        old_standard = row.STANDARD
        use_type = row["1ST_USE"]
        new_standard = do_mapping(mapping, old_standard, district_archetype, use_type, year, construction)
        print(f"Updating {building}, {old_standard} => {new_standard}")

        typology.loc[index, "STANDARD"] = new_standard

    cea.utilities.dbf.dataframe_to_dbf(typology, locator.get_building_typology())


def do_mapping(mapping, old_standard, district_archetype, use_type, year, construction):
    try:
        new_standard = mapping[(old_standard, district_archetype, use_type, year, construction)]
    except KeyError:
        print("Key error!")
        new_standard = old_standard
    return new_standard


def read_mapping():
    """
    Create a dictionary version of the mapping because it's easier to use...
    :return:
    """
    mapping_df = pd.read_excel(os.path.join(os.path.dirname(__file__), "mapping_CONSTRUCTION_STANDARD.xlsx"))
    mapping = {}
    for _, row in mapping_df.iterrows():
        status_quo = row.STATUS_QUO
        district = row.DISTRICT
        use_type = row.USE_TYPE
        year = str(row.YEAR)
        mapping[(status_quo, district, use_type, year, "BAU")] = row.BAU
        mapping[(status_quo, district, use_type, year, "NEP")] = row.NEP
    return mapping


if __name__ == "__main__":
    main(cea.config.Configuration())
