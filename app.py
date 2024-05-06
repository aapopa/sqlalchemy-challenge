# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt 





#################################################
# Database Setup
#################################################

# create engine and mapped base 
Base = automap_base()
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#refelct the tables 
Base.prepare(autoload_with=engine)
#Assign measurement class to variable called 'Measurement' and 
#the station class to variable 'Station' 


#Create session 
session = Session(engine) 
app = Flask(__name__)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station 

# Create our session (link) from Python to the DB
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#################################################
# Flask Setup
#################################################


#got the constants from instructor 
last_date = dt.datetime(2017, 8, 23)
one_year_ago = dt.datetime (2017, 8, 23) - dt.timedelta(days=365)


#################################################
# Flask Routes
#################################################
#@app.route("/")
#def welcome (): 
   # return "List of Routes:"

#@app.route("/api/v1.0/precipitation")
#def precipitation(): 
    #pass 
   
#@app.route("/api/v1.0/stations")
#def stations(): 
 #   results = session.query(Station.station).all
    
  #  return jsonify(list(np.ravel(results)))

#@app.route("/api/v1.0/tobs")
#def tobs(): 
 #   pass 
#@app.route("/api/v1.0/temp/<start>")
#@app.route("/api/v1.0/temp/<start>/")
#@app.route("/api/v1.0/temp/<start>/<end>")
#def temp (start, end=None): 
         
 #   start_date = dt.datetime.strptime(start, "%m%d%Y")
  #  if end is not None: 
   #     end_date = dt.datetime.strptime(end, "%m%d%Y")
    #else: 
     #   end_date = Last_Date 
    #return f"{start_date}-{end_date}"
    

#if __name__=='__main__': 
 #   app.run(debug=True)
@app.route("/")
def welcome():"List of Routes:\n"\
           "/api/v1.0/precipitation\n"\
           "/api/v1.0/stations\n"\
           "/api/v1.0/tobs\n"\
           "/api/v1.0/temp/<start>\n"\
           "/api/v1.0/temp/<start>/<end>"
 

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query precipitation data for the last year in the database
    results = session.query(Measurement.date, Measurement.prcp).\
              filter(Measurement.date >= one_year_ago).\
              filter(Measurement.date <= last_date).all()
    
    # Create a dictionary to store precipitation data with date as key and precipitation as value
    precipitation_data = {date: prcp for date, prcp in results}
    
    # Return the JSON representation of the precipitation data
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    # Query all stations in the database
    results = session.query(Station.station).all()
    
    # Convert the query results to a list of station names
    station_names = [result[0] for result in results]
    
    # Return the JSON representation of the station names
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query temperature observations for the most active station (USC00519281) for the last year
    most_active_station = "USC00519281"
    results = session.query(Measurement.date, Measurement.tobs).\
              filter(Measurement.station == most_active_station).\
              filter(Measurement.date >= one_year_ago).\
              filter(Measurement.date <= last_date).all()
    
    # Create a list of dictionaries with temperature observations
    temperature_data = [{"date": date, "temperature": tobs} for date, tobs in results]
    
    # Return the JSON representation of the temperature data
    return jsonify(temperature_data)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/")
@app.route("/api/v1.0/temp/<start>/<end>")
def temp(start, end=None):
    # Parse start date
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    
    # Parse end date or use last_date as end_date if not specified
    if end:
        end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    else:
        end_date = last_date
    
    # Query temperature data for the specified date range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start_date).\
              filter(Measurement.date <= end_date).all()
    
    # Create a dictionary to store temperature summary
    temperature_summary = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "min_temperature": results[0][0],
        "avg_temperature": results[0][1],
        "max_temperature": results[0][2]
    }
    
    # Return the JSON representation of the temperature summary
    return jsonify(temperature_summary)

if __name__ == '__main__':
    app.run(debug=True)