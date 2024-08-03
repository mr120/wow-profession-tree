import sqlite3
import csv

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

    csv_file_path = 'output/profTalentData.csv'
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(column_names)
        writer.writerows(rows)

    print(f'The query results have been exported to {csv_file_path}.')