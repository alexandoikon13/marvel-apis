from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database_setup import Base
from queries import get_comics_for_character, get_series_and_events_for_character, count_comics_per_character, get_character_summary
from data_ingestion import ingest_data
from config import database_url

''' This script sets up a Flask web application to visualize and interact with the data '''

## Initialize Flask application
app = Flask(__name__)

## Setting up database connection using SQLAlchemy
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)

## Ensure tables are created at app startup
Base.metadata.create_all(engine)

## Run data ingestion after table creation
## Might cause runtime timeout due to big data; can be run separately
# try:
#     print("Running data ingestion...")
#     ingest_data()
#     print("Data ingestion completed.")
# except Exception as e:
#     print(f"Error during data ingestion: {e}")

@app.route('/')
def index():
    """
    Render the landing page for the Marvel API Explorer.
    """
    return render_template('index.html')

@app.route('/api/character/names')
def get_character_names():
    """
    Fetch all character names for dropdown.
    """
    session = Session()
    try:
        query = text('SELECT name FROM characters ORDER BY name ASC;')
        result = session.execute(query).fetchall()
        character_names = [row.name for row in result]
        return jsonify(character_names)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/api/character/comics')
def comics_for_character():
    """
    Fetch all comics for a specific character.
    """
    character_name = request.args.get('character_name')
    if not character_name:
        return jsonify({"error": "Missing character_name parameter"}), 400

    session = Session()
    try:
        # print(f"Fetching comics for character: {character_name}")  # Debug log
        result = get_comics_for_character(session, character_name)
        # print(f"Query result: {result}")  # Debug log

        data = [
            {"character_name": row.character_name, "comic_name": row.comic_name, "thumbnail": row.thumbnail}
            for row in result
        ]
        # print(f"Formatted data: {data}")  # Debug log
        return jsonify(data)
    except Exception as e:
        # print(f"Error fetching comics: {e}")  # Debug log
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@app.route('/api/character/series_and_events')
def series_and_events_for_character():
    """
    Fetch all series and events for a specific character.
    """
    character_name = request.args.get('character_name')
    if not character_name:
        return jsonify({"error": "Missing character_name parameter"}), 400

    session = Session()
    try:
        # print(f"Fetching series and events for character: {character_name}")  # Debug log
        result = get_series_and_events_for_character(session, character_name)
        # print(f"Query result: {result}")  # Debug log

        data = [
            {
                "character_name": row.character_name,
                "series_name": row.series_name,
                "event_name": row.event_name,
            }
            for row in result
        ]
        # print(f"Formatted data: {data}")  # Debug log
        return jsonify(data)
    except Exception as e:
        # print(f"Error fetching series and events: {e}")  # Debug log
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@app.route('/api/character/comic_counts')
def comic_counts():
    """
    Count the number of comics per character.
    """
    character_name = request.args.get('character_name')
    session = Session()
    try:
        result = count_comics_per_character(session, character_name)
        data = [
            {"character_name": row.character_name, "comic_count": row.comic_count}
            for row in result
        ]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/api/character/summary')
def character_summary():
    """
    Get a summary of the total comics, series, and events for each character.
    """
    character_name = request.args.get('character_name')
    session = Session()
    try:
        result = get_character_summary(session, character_name)
        data = [
            {
                "character_name": row.character_name,
                "total_comics": row.total_comics,
                "total_series": row.total_series,
                "total_events": row.total_events,
            }
            for row in result
        ]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.errorhandler(Exception)
def handle_exception(e):
    response = {"error": str(e)}
    return jsonify(response), 500


if __name__ == '__main__':
    app.run(debug=True)
