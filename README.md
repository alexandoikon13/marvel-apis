# marvel-apis
## Try out the app [here](https://marvel-apis-d7832617b49a.herokuapp.com/)

A Flask-based web application to explore data from the Marvel Universe using the Marvel API. This project demonstrates data ingestion, processing, and visualization of Marvel characters, comics, series, events, and stories. Users can interact with the data via a simple frontend interface, leveraging filters and summaries.

## Features

- **Data Extraction**: Locally fetch data from the Marvel API using Python and the marvel package.
- **Data Storage**: Store data in a PostgreSQL database hosted on Heroku, by ingesting data from an S3 bucket in AWS.
- **Frontend Interface**: Use a web application built with Flask to explore Marvel data.
  - View comics for selected characters.
  - See series and events associated with characters.
  - Analyze comic counts and character summaries.
- **Backend Logic**: Python scripts for data and database interaction, together with the frontend.

## Technologies Used

- **Frontend**: HTML, CSS (Bootstrap), JavaScript.
- **Backend**: Python, Flask.
- **Database**: PostgreSQL (hosted on Heroku), AWS S3 bucket.
- **Data Handling**: Pandas for CSV processing.
- **API**: Marvel API for data fetching.
- **Deployment**: Docker for containerization. Heroku cluster for deploying the containerized app.
