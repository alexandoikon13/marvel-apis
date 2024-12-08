import sqlalchemy
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from config import database_url

## Script containing functions to query and calculate metrics from the database

## Create SQLAlchemy engine and session for database interaction
engine = sqlalchemy.create_engine(database_url)
Session = sessionmaker(bind=engine)

def get_comics_for_character(session, character_name):
    """
    Fetch all comics for a specific character.
    """
    query = text('''
        SELECT c.name AS character_name, cm.comic_name, c.thumbnail
        FROM characters c
        JOIN comics cm ON c.character_id = cm.character_id
        WHERE c.name = :character_name;
    ''')
    try:
        # print(f"Executing query for character_name={character_name}")  # Debug log
        result = session.execute(query, {"character_name": character_name}).fetchall()
        # print(f"Query returned {len(result)} rows")  # Debug log
        return result
    except Exception as e:
        # print(f"Query error: {e}")  # Debug log
        raise


def get_series_and_events_for_character(session, character_name):
    """
    Fetch all series and events for a specific character.
    """
    query = text('''
        SELECT c.name AS character_name, s.series_name, e.event_name
        FROM characters c
        LEFT JOIN series s ON c.character_id = s.character_id
        LEFT JOIN events e ON c.character_id = e.character_id
        WHERE c.name = :character_name;
    ''')
    result = session.execute(query, {"character_name": character_name}).fetchall()
    return result

def count_comics_per_character(session, character_name=None):
    """
    Count the number of comics per character, optionally filtered by character_name.
    """
    base_query = '''
        SELECT c.name AS character_name, COUNT(cm.character_id) AS comic_count
        FROM characters c
        JOIN comics cm ON c.character_id = cm.character_id
    '''
    if character_name:
        query = text(base_query + '''
            WHERE c.name = :character_name
            GROUP BY c.character_id, c.name
            ORDER BY comic_count DESC;
        ''')
        result = session.execute(query, {"character_name": character_name}).fetchall()
    else:
        query = text(base_query + '''
            GROUP BY c.character_id, c.name
            ORDER BY comic_count DESC;
        ''')
        result = session.execute(query).fetchall()

    return result

def get_character_summary(session, character_name=None):
    """
    Get a summary of the total comics, series, and events for each character, optionally filtered by character_name.
    """
    base_query = '''
        WITH character_summary AS (
            SELECT
                c.character_id,
                c.name AS character_name,
                COUNT(DISTINCT cm.character_id) AS total_comics,
                COUNT(DISTINCT s.character_id) AS total_series,
                COUNT(DISTINCT e.character_id) AS total_events
            FROM
                characters c
            LEFT JOIN comics cm ON c.character_id = cm.character_id
            LEFT JOIN series s ON c.character_id = s.character_id
            LEFT JOIN events e ON c.character_id = e.character_id
    '''
    if character_name:
        query = text(base_query + '''
            WHERE c.name = :character_name
            GROUP BY c.character_id, c.name
        )
        SELECT
            character_name,
            total_comics,
            total_series,
            total_events
        FROM
            character_summary
        ORDER BY
            total_comics DESC;
        ''')
        result = session.execute(query, {"character_name": character_name}).fetchall()
    else:
        query = text(base_query + '''
            GROUP BY c.character_id, c.name
        )
        SELECT
            character_name,
            total_comics,
            total_series,
            total_events
        FROM
            character_summary
        ORDER BY
            total_comics DESC;
        ''')
        result = session.execute(query).fetchall()

    return result