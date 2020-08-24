import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# print(Base.classes.keys())

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"Welcome to the Hawaii Weather App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<startDate><br/>"
        f"/api/v1.0/start<startDate>/end<endDate>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # """Precipitation for last year recorded"""
    # Query prcp
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_data = session.query(measurement.date, measurement.prcp).filter(measurement.date > last_year).all()

    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    all_prcp = []
    for date, prcp in precip_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():

    """Return a list of all stations"""
    # Query all stations
    stations = session.query(station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active 
    # station for the last year of data.
    session.query(measurement.date).order_by(measurement.date.desc()).first()

    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    temp_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date > last_year).\
        filter(measurement.station == 'USC00519281').all()

    year_data = list(np.ravel(temp_data))

    return jsonify(year_data)

@app.route("/api/v1.0/start<startDate>")
def start(startDate):
    
    # Return a JSON list of the minimum temperature, the average temperature, 
    # and the max temperature for a given start range.
    start_date = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs),
            func.max(measurement.tobs)).\
            filter(func.strftime("%Y-%m-%d", measurement.date) >= startDate).\
            group_by(measurement.date).all()
    start_list = list(start_date)
    return jsonify(start_list)

@app.route("/api/v1.0/start<startDate>/end<endDate>")
def start_end(startDate, endDate):
    
    # Return a JSON list of the minimum temperature, the average temperature, 
    # and the max temperature for a given start range.
    start_end_date = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs),
            func.max(measurement.tobs)).\
            filter(func.strftime("%Y-%m-%d", measurement.date) >= startDate).\
            filter(func.strftime("%Y-%m-%d", measurement.date) <= endDate).\
            group_by(measurement.date).all()
    start_end_list = list(start_end_date)
    return jsonify(start_end_list)


if __name__ == '__main__':
    app.run(debug=True)