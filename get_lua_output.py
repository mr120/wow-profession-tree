import sqlite3
from slpp import slpp as lua  
import os

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
    conn = sqlite3.connect('wow_profession_tree.db')
    conn.row_factory = sqlite3.Row

    query = 'select_all_spell_data.sql'
    cur = execute_query(conn, query,  ())

    rows = cur.fetchall()

    column_names = [description[0] for description in cur.description]

    conn.close()

    traitNodes = {}
    # Just need to collect all the traits to iterate through
    for record in rows:
        if record['ExpansionName'] == 'Khaz Algar':
            professionExpansionID = record['professionExpansionID']
            TraitNodeID = record['TraitNodeID']
            if professionExpansionID not in traitNodes:
                traitNodes[professionExpansionID] = []

            traitNodes[professionExpansionID].append(TraitNodeID)
    
    out_path = 'output/traitnodes.lua'
    lua_str = f'TraitNodes = {lua.encode(traitNodes)};'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as file:
        file.write(lua_str)
    print(f'The query results have been exported to {out_path}.')