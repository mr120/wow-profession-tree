import sqlite3
import pandas as pd
import sys
import os

if len(sys.argv) > 1:
    # Read the first argument after the filename
    wagoversion = sys.argv[1]
else:
    print("No wago version provided.")
    exit()

# Connect to (or create) an SQLite database
conn = sqlite3.connect('wow_profession_tree.db')
cur = conn.cursor()

tables_arr = [
    {
        'filename': 'SpellLabel',
        'table_name': 'spelllabel',
        'create_table_query': 'CREATE TABLE {table_name} (ID int, LabelID int, SpellID int)'
    },
    {
        'filename': 'ProfessionEffect',
        'table_name': 'professioneffect',
        'create_table_query': 'CREATE TABLE {table_name} (ID int, ProfessionEffectTypeEnumID int, Amount int, ModifiedCraftingReagentSlotID int)'
    },
    {
        'filename': 'ProfessionEffectType',
        'table_name': 'professioneffecttype',
        'create_table_query': 'CREATE TABLE {table_name} (ID int, Name_lang text, EnumID int)'
    },
    {
        'filename': 'ProfessionTrait',
        'table_name': 'professiontrait',
        'create_table_query': 'CREATE TABLE {table_name} (ID int, TraitDefinitionID int)'
    },
    {
        'filename': 'ProfessionTraitXEffect',
        'table_name': 'professiontraitXeffect',
        'create_table_query': 'CREATE TABLE {table_name} (ID int, ProfessionTraitID int, ProfessionEffectID int, "_Index" int)'
    },
    {
        'filename': 'ProfessionTraitXLabel',
        'table_name': 'professiontraitXlabel',
        'create_table_query': 'CREATE TABLE {table_name} (ID int, ProfessionTraitID int, LabelID int)'
    },
    {
        'filename': 'TraitDefinition',
        'table_name': 'traitdefinition',
        'create_table_query': 'CREATE TABLE {table_name} (OverrideName_lang text, OverrideSubtext_lang text, OverrideDescription_lang text, ID int, SpellID int, OverrideIcon int, OverridesSpellID int, VisibleSpellID int)'
    },
    {
        'filename': 'TraitNodeXTraitNodeEntry',
        'table_name': 'traitnodeXtraitnodeentry',
        'create_table_query': 'CREATE TABLE {table_name} (ID int, TraitNodeID int, TraitNodeEntryID int, "_Index" int)'
    },
    {
        'filename': 'TraitNodeEntry',
        'table_name': 'traitnodeentry',
        'create_table_query': 'CREATE TABLE {table_name} (ID int, TraitDefinitionId int, MaxRanks int, NodeEntryType int, TraitSubTreeID int)'
    },
]

for table in tables_arr:
    # Read the CSV file into a pandas DataFrame
    filename = table['filename']

    file_path = f'{filename}.{wagoversion}.csv'

    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        exit()

    df = pd.read_csv(file_path)

    # Extract column names from the DataFrame
    column_names = df.columns.tolist()

    table_name = table['table_name']
    # Create a table with columns based on the CSV headers
    drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
    cur.execute(drop_table_query)
    create_table_query = table['create_table_query'].format(table_name=table_name)
    cur.execute(create_table_query)

    # Insert data into the table
    for row in df.itertuples(index=False, name=None):
        placeholders = ', '.join(['?' for _ in column_names])
        insert_query = f'INSERT INTO {table_name} ({", ".join(column_names)}) VALUES ({placeholders})'
        cur.execute(insert_query, row)

    # Commit
    conn.commit()

# Close the connection
conn.close()
