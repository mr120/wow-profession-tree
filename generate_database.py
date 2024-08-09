import sqlite3
import csv
import sys
import os
import http.client
import json
import urllib.parse
import requests

tables_arr = [
    {
        'filename': 'SpellLabel',
        'table_name': 'spelllabel',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'LabelID', 'type': 'int'},
            {'name': 'SpellID', 'type': 'int'},
        ]
    },
    {
        'filename': 'ProfessionEffect',
        'table_name': 'professioneffect',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'ProfessionEffectTypeEnumID', 'type': 'int'},
            {'name': 'Amount', 'type': 'int'},
            {'name': 'ModifiedCraftingReagentSlotID', 'type': 'int'},
        ]
    },
    {
        'filename': 'ProfessionEffectType',
        'table_name': 'professioneffecttype',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'Name_lang', 'type': 'text'},
            {'name': 'EnumID', 'type': 'int'},
        ]
    },
    {
        'filename': 'ProfessionTrait',
        'table_name': 'professiontrait',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'TraitDefinitionID', 'type': 'int'},
        ]
    },
    {
        'filename': 'ProfessionTraitXEffect',
        'table_name': 'professiontraitXeffect',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'ProfessionTraitID', 'type': 'int'},
            {'name': 'ProfessionEffectID', 'type': 'int'},
            {'name': 'Field_10_0_0_44649_003', 'type': 'int'}, #index
        ]
    },
    {
        'filename': 'ProfessionTraitXLabel',
        'table_name': 'professiontraitXlabel',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'ProfessionTraitID', 'type': 'int'},
            {'name': 'LabelID', 'type': 'int'},
        ]
    },
    {
        'filename': 'TraitDefinition',
        'table_name': 'traitdefinition',
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
        'filename': 'TraitNodeXTraitNodeEntry',
        'table_name': 'traitnodeXtraitnodeentry',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'TraitNodeID', 'type': 'int'},
            {'name': 'TraitNodeEntryID', 'type': 'int'},
            {'name': '_Index', 'type': 'int'},
        ]
    },
    {
        'filename': 'TraitNodeEntry',
        'table_name': 'traitnodeentry',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'TraitDefinitionID', 'type': 'int'},
            {'name': 'MaxRanks', 'type': 'int'},
            {'name': 'NodeEntryType', 'type': 'int'},
            {'name': 'TraitSubTreeID', 'type': 'int'},
        ]
    },
    {
        'filename': 'TraitNodeGroupXTraitNode',
        'table_name': 'traitnodegroupXtraitnode',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'TraitNodeGroupID', 'type': 'int'},
            {'name': 'TraitNodeID', 'type': 'int'},
            {'name': '_Index', 'type': 'int'},
        ]
    },
    {
        'filename': 'TraitCond',
        'table_name': 'traitcond',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'TraitTreeID', 'type': 'int'},
            {'name': 'TraitNodeGroupID', 'type': 'int'},
            {'name': 'TraitNodeID', 'type': 'int'},
            {'name': 'SpentAmountRequired', 'type': 'int'},
        ]
    },
    {
        'filename': 'TraitNodeXTraitCond',
        'table_name': 'traitnodeXtraitcond',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'TraitCondID', 'type': 'int'},
            {'name': 'TraitNodeID', 'type': 'int'},
        ]
    },
    {
        'filename': 'SkillLineAbility',
        'table_name': 'skilllineability',
        'columns': [
            {'name': 'ID', 'type': 'int'},
            {'name': 'Spell', 'type': 'int'},
            {'name': 'SkillLine', 'type': 'int'}, #profID
            {'name': 'SkillupSkillLineID', 'type': 'int'}, #profIDperexp
        ]
    }
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
    conn = sqlite3.connect('wow_profession_tree.db')
    cur = conn.cursor()

    for table in tables_arr:
        filename = table['filename']
        file_path = f'data_source/{filename}.{wagoversion}.csv'

        download_file(f'https://wago.tools/db2/{filename}/csv', file_path)

        if not os.path.exists(file_path):
            print(f"The file {file_path} does not exist.")
            exit()

        table_name = table['table_name']
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

        create_table_query = f'CREATE TABLE {table_name} ({", ".join(formatted_create_columns)})'
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