import os
import psycopg2
import pytest
import logging

DB_HOST = os.getenv("DB_HOST", "localhost")
USER = "postgres"
OPEN = 0


class DB:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def close(self):
        self.cursor.close()
        self.conn.close()


@pytest.fixture
def db(scope="class"):
    logging.info("Connecting to postgres database...")
    try:
        conn = psycopg2.connect(host=DB_HOST, user=USER)
        cursor = conn.cursor()
        db = DB(conn, cursor)
        yield db
        logging.info("closing database connection...")
        db.close()
    except:
        logging.error("Postgres database connection error!")


def test_db_connection(db):
    assert db.conn.closed == OPEN, "Connection closed unexpectedly"


def test_db_column_types(db):
    db.cursor.execute("""SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = N'votes'""")
    columns = db.cursor.fetchall()
    for column in columns:
        print(column)
        assert "votes" in column
        assert "id" or "votes" in column
        assert "character varying" in column
        assert 255 in column
        assert "varchar" in column
