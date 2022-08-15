# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Import dependencies for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# import Flask
from flask import Flask
from flask import jsonify


# Access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect database into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references for each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link
session = Session(engine)

# Define flask app
app = Flask(__name__)

# Create Flask Routes
@app.route('/')
def welcome():
    return (f"Welcome to the Climate Analysis API!<br/>"
        f"Avaliable Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end<br/>"
    )
# Define Precipitation URL
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Define Stations URL
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Define tobs URL
@ app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
     filter(Measurement.station == 'USC00519281').\
     filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Define Min and Max temps
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
