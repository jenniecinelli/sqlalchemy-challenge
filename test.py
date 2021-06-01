import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func

# 1. import Flask
from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurements = Base.classes.measurement
Stations = Base.classes.station


# index
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"

    )


# precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
   
    session = Session(engine)

    results = (session.query(Measurements.date, Measurements.prcp)
                .order_by(Measurements.date))

    session.close()
            
    precipitation_list = []
    for each_row in results: 
        dt_dict = {}
        dt_dict['date'] = each_row.date
        dt_dict['prcp'] = each_row.prcp
        precipitation_list.append(dt_dict)
    
    return jsonify(precipitation_list)

# stations
@app.route("/api/v1.0/stations")
def station():
   
    session = Session(engine)

    results = (session.query(Stations.id, Stations.station, Stations.name)
                .group_by(Stations.id))

    session.close()
            
    station_list = []
    for each_row in results: 
        dt_dict = {}
        dt_dict['id'] = each_row.id
        dt_dict['station'] = each_row.station
        dt_dict['name'] = each_row.name
        station_list.append(dt_dict)
    
    return jsonify(station_list)

#tobs
@app.route("/api/v1.0/tobs")
def tobs():
   
    session = Session(engine)
    last_date = (session.query(Measurements.date, Measurements.tobs)
                .order_by((Measurements.date).desc()).first())
    year_ago = (dt.date(2017, 8, 23) - dt.timedelta(days=365))
    
    results = (session.query(Measurements.date, Measurements.tobs)
                .filter(Measurements.date >= year_ago)
                .filter(Measurements.station == 'USC00519281')
                .order_by((Measurements.date).desc()))
    session.close()
            
    tobs_list = []
    for each_row in results: 
        dt_dict = {}
        dt_dict['date'] = each_row.date
        dt_dict['tobs'] = each_row.tobs
        tobs_list.append(dt_dict)
    
    return jsonify(tobs_list)
    
#start dates
@app.route("/api/v1.0/<start>")
def start_temps(start):

    session = Session(engine)
    
    results = (session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs))
                    .filter(Measurements.date >= start))
    
    session.close()

    temp_min = results[0][0]
    temp_avg = results[0][1]
    temp_max = results[0][2]

    print_results = (['Start Date: ' + start,
                        'The minimum temperature was: ' +str(temp_min),
                        'The average temperature was: ' + str(temp_avg),
                        'The maximum temperature was: ' + str(temp_max)])
    
    return jsonify(print_results)

#start and end dates
@app.route("/api/v1.0/<start>/<end>")
def temps(start, end):

    session = Session(engine)
    
    results = (session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs))
                    .filter(Measurements.date >= start)
                    .filter(Measurements.date <= end))
    
    session.close()

    temp_min = results[0][0]
    temp_avg = results[0][1]
    temp_max = results[0][2]

    print_temps = (['Dates: ' + start + ' between ' + end,
                        'The minimum temperature was: ' +str(temp_min),
                        'The average temperature was: ' + str(temp_avg),
                        'The maximum temperature was: ' + str(temp_max)])
    
    return jsonify(print_temps)

if __name__ == "__main__":
    app.run(debug=True)