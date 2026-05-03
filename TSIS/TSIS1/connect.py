import psycopg2
from config import load_config

def connect(config):
    "Open a quick test connection to PostgreSQL."
    try:
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def create_tables():
    config = load_config()
    conn = psycopg2.connect(**config)
    cur = conn.cursor()

    # 1.Tables
    with open('schema.sql', 'r', encoding='utf-8') as f:
        cur.execute(f.read())

    # 2.Functions and Procedures
    with open('procedures.sql', 'r', encoding='utf-8') as f:
        cur.execute(f.read())

    conn.commit()
    cur.close()
    conn.close()
    print('Database updated.')

if __name__ == '__main__':
    config = load_config()
    connect(config)
    create_tables()