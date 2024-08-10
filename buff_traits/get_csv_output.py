import sqlite3
import csv
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

    query = (Path(__file__).parent / 'select_all_profession_buffs_data.sql').resolve()
    cur = execute_query(conn, query,  ())

    rows = cur.fetchall()

    column_names = [description[0] for description in cur.description]

    conn.close()

    output_file_path = (Path(__file__).parent / '../output/general_buff_traits.csv').resolve()
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(column_names)
        writer.writerows(rows)

    print(f'The query results have been exported to {output_file_path}.')