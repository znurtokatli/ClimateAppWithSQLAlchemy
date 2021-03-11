# dependencies
import numpy as np
import datetime as dt  

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# db connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# save reference to the table
measurement = Base.classes.measurement
Station = Base.classes.station

# set up flask
app = Flask(__name__)
  
# routes
@app.route("/")
def home():
    "Welcome Home! List All Available Api Routes:"
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperatures: /api/v1.0/tobs<br/>"
        f"Start Date: /api/v1.0/start<br/>"
        f"Date Range: /api/v1.0/date_range <br/> "
    ) 

# precipitation for last year
@app.route("/api/v1.0/precipitation")
def precipitation():
     # create session
    session = Session(engine) 

    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    earliest_date = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days = 365) 
 
    data = session.query(measurement.date, measurement.prcp).\
                            filter(measurement.date >= earliest_date).all() 
                            
    result = []

    for date, prcp in data:
        prcp = {}
        prcp["date"] = date
        prcp["prcp"] = prcp
        result.append(prcp)

    session.close()

    return jsonify(result)

# stations
@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine) 

    data = session.query(Station.station, Station.name).all()

    result = [] 

    for station, name in data:
        stt = {}
        stt["station"] = station
        stt["name"] = name
        result.append(stt)
 
    session.close()
 
    return jsonify(result)

# tobs
@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)

    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    earliest_date = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days = 365) 
  
    data = session.query(measurement.tobs, measurement.date).filter(measurement.date >= earliest_date).all()
 
    result = []

    for tobs, date in data:
        temp = {}
        temp["date"] = date
        temp["tobs"] = tobs
        result.append(temp)

    session.close()

    return jsonify(result)

# start_date
@app.route("/api/v1.0/start_date")
def start_date(pdate):
    
    session = Session(engine)

    data = session.query(func.min(measurement.tobs), func.max(measurement.tobs), \
                         func.avg(measurement.tobs)).\
                         filter(measurement.date >= pdate).all()
 
    result = []

    for min, avg, max in data:
        start= {}
        start["min"] = min
        start["max"] = max
        start["avg"] = avg
        result.append(start)

    session.close() 

    return jsonify(result)

# date range
@app.route("/api/v1.0/date_range")
def date_range(date_from, date_to): 

    session = Session(engine)

    data = session.query(func.min(measurement.tobs), func.max(measurement.tobs), \
                         func.avg(measurement.tobs)).\
                         filter(measurement.date >= date_from).filter(measurement.date <= date_to).all()
 
    result = []

    for min, avg, max in data:
        describe = {}
        describe["min"] = min
        describe["max"] = max
        describe["avg"] = avg
        result.append(describe) 

    session.close()

    return jsonify(result)
 
# run 
if __name__ == "__main__":
    app.run(debug=True)     