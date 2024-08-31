"""
This script sets up a Flask application to provide API endpoints for temperature statistics.
"""
# Import the dependencies.
from datetime import datetime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_
from flask import Flask, jsonify, abort

import numpy as np


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "<h1>Available Routes:</h1>"
        "<ul>"
            "<li>/api/v1.0/precipitation</li>"
            "<li>/api/v1.0/stations</li>"
            "<li>/api/v1.0/tobs</li>"
            "<li>/api/v1.0/&lt;start&gt;</li>"
            "<li>/api/v1.0/&lt;start&gt;/&lt;end&gt;</li>"
        "</ul>"
    )


#################################################
# Flask Route - /api/v1.0/precipitation
#################################################
@app.route("/api/v1.0/precipitation")
def precip():
    """Return a list of dates and precipitation"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find the most recent date in the data set.
    precipitation_subquery = session.query(func.max(Measurement.date)).scalar_subquery()

    results = (
        session.query(Measurement.date, Measurement.prcp.label("precipitation")).filter(
            and_(
                Measurement.date >= func.date(precipitation_subquery, "-12 months"),
                Measurement.prcp.isnot(None),
            )
        )
    ).all()

    session.close()

    # Convert list of tuples into normal list
    precipitation_list = []
    for date, precipitation in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = precipitation
        precipitation_list.append(precipitation_dict)

    return jsonify(precipitation_list)


#################################################
# Flask Route - /api/v1.0/stations
#################################################
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # List the stations and their counts in descending order.
    results = session.query(Measurement.station).group_by(Measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


#################################################
# Flask Route - /api/v1.0/tobs
#################################################
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of dates and temperatures of the most-active station for the previous year"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find the most recent date in the data set.
    station_subquery = (
        session.query(func.max(Measurement.date))
        .where(Measurement.station == "USC00519281")
        .scalar_subquery()
    )

    # Main query
    results = (
        session.query(Measurement.date, Measurement.tobs.label("temperature")).filter(
            Measurement.station == "USC00519281",
            Measurement.date >= func.date(station_subquery, "-12 months"),
        )
    ).all()

    session.close()

    # Convert list of tuples into normal list
    tobs_list = []
    for date, temperature in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temperature"] = temperature
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)


#################################################
# Flask Route - /api/v1.0/<start_date>/<end_date>
#################################################
@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_start_end(start_date, end_date):
    """Return a JSON list of the min, avg, and max temp for specified start and end range"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Define the date format
    date_format = "%Y-%m-%d"

    # Validate start_date
    try:
        start_date = datetime.strptime(start_date, date_format).date()
    except ValueError:
        abort(400, description="Invalid start_date. Format should be YYYY-MM-DD.")

    # Validate end_date
    try:
        end_date = datetime.strptime(end_date, date_format).date()
    except ValueError:
        abort(400, description="Invalid end_date. Format should be YYYY-MM-DD.")

    # Query to calculate tmin, tmax, and tavg
    results = (
        session.query(
            func.min(Measurement.tobs).label("tmin"),
            func.max(Measurement.tobs).label("tmax"),
            func.avg(Measurement.tobs).label("tavg"),
        )
        .filter(Measurement.date >= start_date)
        .filter(Measurement.date <= end_date)
        .all()
    )

    # Convert the query result into a dictionary
    temp_stats = {
        "tmin": results[0].tmin,
        "tmax": results[0].tmax,
        "tavg": results[0].tavg,
    }

    return jsonify(temp_stats)

#################################################
# Flask Route - /api/v1.0/<start_date>
#################################################
@app.route("/api/v1.0/<start_date>")
def temp_start(start_date):
    """Return a JSON list of the min, avg, and max temp for specified start date"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Define the date format
    date_format = "%Y-%m-%d"

    # Validate start_date
    try:
        start_date = datetime.strptime(start_date, date_format).date()
    except ValueError:
        abort(400, description="Invalid start_date. Format should be YYYY-MM-DD.")

    # Query to calculate tmin, tmax, and tavg
    results = (
        session.query(
            func.min(Measurement.tobs).label("tmin"),
            func.max(Measurement.tobs).label("tmax"),
            func.avg(Measurement.tobs).label("tavg"),
        )
        .filter(Measurement.date >= start_date)
        .all()
    )

    # Convert the query result into a dictionary
    temp_stats = {
        "tmin": results[0].tmin,
        "tmax": results[0].tmax,
        "tavg": results[0].tavg,
    }

    return jsonify(temp_stats)


if __name__ == "__main__":
    app.run(debug=True)
