import sqlite3
import csv
import json
import os
from pathlib import Path

def load_query(filename):
    """Load SQL query from a file."""
    with open(filename, 'r') as file:
        return file.read()

def execute_query(db_connection, query_file, params):
    """Execute a SQL query with parameters."""
    query = load_query(query_file)
    cursor = db_connection.cursor()
    cursor.execute(query, params)
    db_connection.commit()
    return cursor


if __name__ == '__main__':
    conn = sqlite3.connect((Path(__file__).parent / '../wow_profession_tree.db').resolve())
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = (Path(__file__).parent / 'select_all_spell_data.sql').resolve()
    cur = execute_query(conn, query,  ())
    
    rows = cur.fetchall()

    column_names = [description[0] for description in cur.description]

    conn.close()

    jsonProfessionsData = {}

    # Process the data
    for record in rows:
        spell_id = record['SpellID']
        stat = record['Stat']
        amount = record['Amount']
        ranks = record['MaxRanks']

        # If the spellID is not in the result dictionary, add it
        if spell_id not in jsonProfessionsData:
            jsonProfessionsData[spell_id] = {}

        # If the stat is not in the sub-dictionary, add it with the amount
        if stat not in jsonProfessionsData[spell_id]:
            jsonProfessionsData[spell_id][stat] = amount * ranks
        else:
            # Otherwise, add the amount to the existing value
            jsonProfessionsData[spell_id][stat] += amount * ranks

    json_str = json.dumps(jsonProfessionsData, indent=4)

    js_str = f'const data = {json_str};'

    output_file_path = (Path(__file__).parent / '../output/js_profession_traits.js').resolve()
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w') as file:
        file.write(js_str)

    print(f'The query results have been exported to {output_file_path}.')