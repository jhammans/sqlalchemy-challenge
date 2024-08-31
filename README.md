# sqlalchemy-challenge

## Description:
This project aims to analyze and explore the climate data for Honolulu, Hawaii, to assist with vacation planning. Using Python, SQLAlchemy, Pandas, and Matplotlib, we conduct a comprehensive climate analysis and create a RESTful API using Flask to share the findings.

## Key Features
### Part 1: Climate Data Analysis
- Data Exploration: Utilize SQLAlchemy ORM queries to connect to a SQLite database and explore the climate data.
- Precipitation Analysis: Analyze the precipitation levels for the last 12 months to understand seasonal patterns.
- Station Analysis: Examine data from various weather stations to identify the most active station.
### Part 2: Flask API Development
- Home Route: Provides an overview of all available API routes.
- Precipitation Route (/api/v1.0/precipitation): Returns JSON data of the last 12 months of precipitation, with dates as keys and precipitation levels as values.
- Stations Route (/api/v1.0/stations): Returns a JSON list of all weather stations in the dataset.
- Temperature Observations Route (/api/v1.0/tobs): Provides temperature observations from the most active station for the previous year.
- Temperature Summary Routes (/api/v1.0/<start> and /api/v1.0/<start>/<end>): Returns a JSON list of the minimum, average, and maximum temperatures for a specified date range.

## Project Structure:
The repository is organized as follows:

```bash
sqlalchemy-challenge/
├── Resources/                   # Data files and sqllite database
├── Starter_Code/     
├── SurfsUp/                     # Main project folder
|└── app.py                      # Python script containing Flask API application
|└── climate_analysis.ipynb      # Jupyter notebook containing climate data analysis for Part 1
└── README.md                    # Project README file
```

## Deployment
To deploy this project

```bash
#Clone the repository
git clone https://github.com/jhammans/sqlalchemy-challenge.git
cd sqlalchemy-challenge/SurfsUp
```
