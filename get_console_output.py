import sqlite3
import csv
from prettytable import PrettyTable

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
    cur = conn.cursor()

    query = 'select_all_spell_data.sql'
    cur = execute_query(conn, query,  ())

    rows = cur.fetchall()

    column_names = [description[0] for description in cur.description]

    conn.close()

    table = PrettyTable()

    table.field_names = column_names
    for row in rows:
        table.add_row(row)

    print(table)
