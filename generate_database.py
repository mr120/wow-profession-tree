import sqlite3
import csv
import sys
import os
import http.client
import json
import urllib.parse
import requests
from pathlib import Path

tables_arr = [
    {
        'name': 'CraftingData',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'CraftingDifficulty', 'type': 'int'},
        ]
    },
    {
        'name': 'CraftingDataItemQuality',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'ItemID', 'type': 'int'},
            {'name': 'CraftingDataID', 'type': 'int'},
        ]
    },
    {
        'name': 'CraftingOrder',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'SkillLineAbilityID', 'type': 'int'},
        ]
    },
    {
        'name': 'ItemEffect',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'SpellID', 'type': 'int'},
        ]
    },
    {
        'name': 'ModifiedCraftingSpellSlot',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'SpellID', 'type': 'int'},
            {'name': 'Slot', 'type': 'int'},
            {'name': 'ModifiedCraftingReagentSlotID', 'type': 'int'},
            {'name': 'ReagentCount', 'type': 'int'},
            {'name': 'ReagentReCraftCount', 'type': 'int'},
        ]
    },
    {
        'name': 'ProfessionEffect',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'ProfessionEffectTypeEnumID', 'type': 'int'},
            {'name': 'Amount', 'type': 'int'},
            {'name': 'ModifiedCraftingReagentSlotID', 'type': 'int'},
        ]
    },
    {
        'name': 'ProfessionEffectType',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'Name_lang', 'type': 'text'},
            {'name': 'EnumID', 'type': 'int'},
        ]
    },
    {
        'name': 'ProfessionTrait',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'TraitDefinitionID', 'type': 'int'},
        ]
    },
    {
        'name': 'ProfessionTraitXEffect',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'ProfessionTraitID', 'type': 'int'},
            {'name': 'ProfessionEffectID', 'type': 'int'},
            {'name': 'Field_10_0_0_44649_003', 'type': 'int'}, #index
        ]
    },
    {
        'name': 'ProfessionTraitXLabel',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'ProfessionTraitID', 'type': 'int'},
            {'name': 'LabelID', 'type': 'int'},
        ]
    },
    {
        'name': 'SkillLine',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'DisplayName_lang', 'type': 'text'},
        ]
    },
    {
        'name': 'SkillLineAbility',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'Spell', 'type': 'int'},
            {'name': 'SkillLine', 'type': 'int'}, #profID
            {'name': 'SkillupSkillLineID', 'type': 'int'}, #profIDperexp
        ]
    },
    {
        'name': 'SpellAuraOptions',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'CumulativeAura', 'type': 'int'},
            {'name': 'SpellID', 'type': 'int'},
        ]
    },
    {
        'name': 'SpellLabel',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'LabelID', 'type': 'int'},
            {'name': 'SpellID', 'type': 'int'},
        ]
    },
    {
        'name': 'SpellEffect',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'EffectAura', 'type': 'int'},
            {'name': 'EffectIndex', 'type': 'int'},
            {'name': 'EffectTriggerSpell', 'type': 'int'},
            {'name': 'EffectBasePointsF', 'type': 'int'},
            {'name': 'EffectMiscValue_0', 'type': 'int'},
            {'name': 'SpellID', 'type': 'int'},
        ]
    },
    {
        'name': 'SpellMisc',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'Attributes_0', 'type': 'text'},
            {'name': 'SpellID', 'type': 'int'},
        ]
    },
    {
        'name': 'SpellReagents',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'SpellID', 'type': 'int'},
            {'name': 'Reagent_0', 'type': 'int'},
            {'name': 'Reagent_1', 'type': 'int'},
            {'name': 'Reagent_2', 'type': 'int'},
            {'name': 'Reagent_3', 'type': 'int'},
            {'name': 'Reagent_4', 'type': 'int'},
            {'name': 'Reagent_5', 'type': 'int'},
            {'name': 'Reagent_6', 'type': 'int'},
            {'name': 'ReagentCount_0', 'type': 'int'},
            {'name': 'ReagentCount_1', 'type': 'int'},
            {'name': 'ReagentCount_2', 'type': 'int'},
            {'name': 'ReagentCount_3', 'type': 'int'},
            {'name': 'ReagentCount_4', 'type': 'int'},
            {'name': 'ReagentCount_5', 'type': 'int'},
            {'name': 'ReagentCount_6', 'type': 'int'},
            {'name': 'ReagentReCraftCount_0', 'type': 'int'},
            {'name': 'ReagentReCraftCount_1', 'type': 'int'},
            {'name': 'ReagentReCraftCount_2', 'type': 'int'},
            {'name': 'ReagentReCraftCount_3', 'type': 'int'},
            {'name': 'ReagentReCraftCount_4', 'type': 'int'},
            {'name': 'ReagentReCraftCount_5', 'type': 'int'},
            {'name': 'ReagentReCraftCount_6', 'type': 'int'},
        ]
    },
    {
        'name': 'TraitCond',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'TraitTreeID', 'type': 'int'},
            {'name': 'TraitNodeGroupID', 'type': 'int'},
            {'name': 'TraitNodeID', 'type': 'int'},
            {'name': 'SpentAmountRequired', 'type': 'int'},
        ]
    },
    {
        'name': 'TraitDefinition',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'OverrideName_lang', 'type': 'text'},
            {'name': 'OverrideSubtext_lang', 'type': 'text'},
            {'name': 'OverrideDescription_lang', 'type': 'text'},
            {'name': 'SpellID', 'type': 'int'},
            {'name': 'OverrideIcon', 'type': 'int'},
            {'name': 'OverridesSpellID', 'type': 'int'},
            {'name': 'VisibleSpellID', 'type': 'int'},
        ]
    },
    {
        'name': 'TraitNodeEntry',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'TraitDefinitionID', 'type': 'int'},
            {'name': 'MaxRanks', 'type': 'int'},
            {'name': 'NodeEntryType', 'type': 'int'},
            {'name': 'TraitSubTreeID', 'type': 'int'},
        ]
    },
    {
        'name': 'TraitNodeGroupXTraitNode',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'TraitNodeGroupID', 'type': 'int'},
            {'name': 'TraitNodeID', 'type': 'int'},
            {'name': '_Index', 'type': 'int'},
        ]
    },
    {
        'name': 'TraitNodeXTraitCond',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'TraitCondID', 'type': 'int'},
            {'name': 'TraitNodeID', 'type': 'int'},
        ]
    },
    {
        'name': 'TraitNodeXTraitNodeEntry',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'TraitNodeID', 'type': 'int'},
            {'name': 'TraitNodeEntryID', 'type': 'int'},
            {'name': '_Index', 'type': 'int'},
        ]
    },
]

def fetch_data_from_api(api_url):
    # Parse the URL
    parsed_url = urllib.parse.urlparse(api_url)
    conn = http.client.HTTPSConnection(parsed_url.netloc)

    # Make the GET request
    conn.request("GET", parsed_url.path + ('?' + parsed_url.query if parsed_url.query else ''))

    # Get the response
    response = conn.getresponse()

    if response.status != 200:
        raise Exception(f"Failed to fetch data: {response.status} {response.reason}")

    # Read the response data
    data = response.read()

    # Parse the JSON data into a dictionary
    json_data = json.loads(data)

    return json_data

def download_file(url, local_path):
    if not os.path.exists(local_path):
        print(f"File {local_path} does not exist. Downloading...")

        # Download the file from the URL
        try:
            r = requests.get(url)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as outfile:
                outfile.write(r.content)

        except Exception as e:
            print(f"Failed to download the file: {e}")
    else:
        print(f"File {local_path} already exists. No download needed.")

if __name__ == '__main__':
    version_data = fetch_data_from_api('https://wago.tools/api/builds/wow_beta/latest')
    wagoversion = version_data['version']

    # Connect to (or create) an SQLite database
    conn = sqlite3.connect((Path(__file__).parent / 'wow_profession_tree.db').resolve())
    cur = conn.cursor()

    for table in tables_arr:
        filename = table['name']
        file_path = (Path(__file__).parent / f'data_source/{filename}.{wagoversion}.csv').resolve()

        download_file(f'https://wago.tools/db2/{filename}/csv', file_path)

        if not os.path.exists(file_path):
            print(f"The file {file_path} does not exist.")
            exit()

        table_name = table['name']
        columns = table['columns']

        formatted_create_columns = []
        formatted_insert_columns = []
        for column in columns:
            # Generate array of '{column name} {type}'
            formatted_create_columns.append(f"{column['name']} {column['type']}")

            # Generate array of '{column name}'
            formatted_insert_columns.append(column['name'])

        drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
        cur.execute(drop_table_query)

        create_table_query = f'CREATE TABLE {table_name} ({', '.join(formatted_create_columns)})'
        cur.execute(create_table_query)

        placeholders = ', '.join(['?' for _ in formatted_insert_columns])

        # Read the CSV file and insert the data into the database
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                insert_query = f'INSERT INTO {table_name} ({", ".join(formatted_insert_columns)}) VALUES ({placeholders})'
                row_data = tuple(row[column['name']] for column in columns)
                cur.execute(insert_query, row_data)

        conn.commit()

    # Close the connection
    conn.close()

    print(f"Database regenerated.")