#step  ii


# Import the dependencies.


from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
# create an engine for the table
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)
# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB

session = Session(bind=engine)
#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
#Start at the homepage.

#List all the available routes.
@app.route("/")
def home():
    print("Welcome to the home section.")
    return (f"Welcome to my Climate API <br/>"
        f"Linked Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>/"
    )
        
        





#       Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("loading in precipitation section.")
    # Find the most recent date
    lastest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_date = pd.to_datetime(lastest_date) - pd.DateOffset(years=1)
    
     #Query the precipitation data for the last 12 months
    Data_precipation_s = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_date.date()).all()
    
    # Convert the query results to a dictionary with date as the key and prcp as the value
    precipation_dict = {date: prcp for date, prcp in Data_precipation_s}
    
#Return the JSON representation of your dictionary.
    return jsonify(precipation_dict)
    #print(one_year_date.date())
#precipitation()

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    print("loading into Station Section.")
    
    station_list = session.query(Station.station)\
    .order_by(Station.station).all() 
    print()
    print("Station List:")   
    for row in station_list:
        print (row[0])
  #witht the presence of return you do not else
    print("Exceeding Station area.")
    return jsonify(station_list)




#Query the dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    print("loading in tobs section.")
    most_active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).\
                                    order_by(func.count(Measurement.station).desc()).first()[0]

    most_recent_date = session.query(Measurement.date).filter(Measurement.station == most_active_stations).\
                       order_by(Measurement.date.desc()).first()[0]

    one_year_date = pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)
    one_year_date
#Return a JSON list of temperature observations for the previous year.
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station == most_active_stations).\
            filter(Measurement.date >= one_year_date.date()).all()
#query results to a dictonary list
    tobs_list = [{"Date": date, "Temperature": temp} for date, temp in tobs_data]

    return jsonify(tobs_list)

from flask import Flask, request, jsonify 
import datetime as dt 
import numpy as np 
from sqlalchemy import func



#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
@app.route('/api/stats')


def stats():
    # Get 'start' and 'end' parameters from the URL query string
    start = request.args.get('start', None)  # Defaults to None if not provided
    end = request.args.get('end', None)      # Defaults to None if not provided
    # Select statement for TMIN, TAVG, TMAX
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # If a start date is provided
    if start:
        # Convert start date string to datetime object
        start = dt.datetime.strptime(start, "%Y-%m-%d")
        # Query to calculate min, avg, max temperature from the start date
        results = session.query(*sel).filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        session.close()
        return jsonify(temps)
    # If both start and end dates are provided
    if start and end:
        # Convert end date string to datetime object
        end = dt.datetime.strptime(end, "%Y-%m-%d")
        # Query to calculate min, avg, max temperature between start and end date
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        session.close()
        return jsonify(temps)
    # If no start or end date is provided, return an empty result
    return jsonify({"error": "No valid date provided"}), 404
if __name__ == '__main__':
    app.run(debug=True)





#





















