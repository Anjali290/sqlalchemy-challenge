import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
# Database Setup

engine = create_engine("sqlite:///Resorurces/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Flask Setup
app = Flask(__name__)

# flask route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns json with the date as the key and the value as the precipitation"""
    results= session.query(Measurement.date,Measurement.prcp ).\
    filter(Measurement.date <= '2017-08-23' ).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    all_dates = list(np.ravel(results))

    return jsonify(all_dates)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations= list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
     # Create our session (link) from Python to the DB
    session = Session(engine)
    #  Query the dates and temperature observations of the most-active station for the previous year of data
    # Return a JSON list of temperature observations for the previous year.
    most_active= session.query(Measurement.station).group_by(Measurement.station).\
             order_by(func.count(Measurement.id).desc()).first()
    date_temp = session.query(Measurement.date,Measurement.tobs).group_by(Measurement.station == 'USC00519281').filter(func.strftime("%Y", Measurement.date) == "2016").\
             order_by(func.min(Measurement.tobs)).all()

   
    session.close()

    return jsonify(date_temp)


if __name__ == '__main__':
    app.run(debug=True)

