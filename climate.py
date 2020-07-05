from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    recent_date = dt.date(2017, 8 ,23)
    one_year_ago = recent_date - dt.timedelta(days=365)

    past_temp = (session.query(Measurement.date, Measurement.prcp)
                .filter(Measurement.date <= recent_date)
                .filter(Measurement.date >= one_year_ago)
                .order_by(Measurement.date).all())
    
    precip = {date: prcp for date, prcp in past_temp}
    
    return jsonify(precip)

@app.route('/api/v1.0/stations')
def stations():

    all_stations = session.query(Station.station).all()

    return jsonify(all_stations)

@app.route('/api/v1.0/tobs') 
def tobs():  
    recent_date = dt.date(2017, 8 ,23)
    one_year_ago = maxDate - dt.timedelta(days=365)

    lastyear = (session.query(Measurement.tobs)
                .filter(Measurement.station == 'USC00519281')
                .filter(Measurement.date <= recent_date)
                .filter(Measurement.date >= one_year_ago)
                .order_by(Measurement.tobs).all())
    
    return jsonify(lastyear)

@app.route('/api/v1.0/<start>') 
def start(start=None):

    tobs = (session.query(Measurement.tobs).filter(Measurement.date.between(start, '2017-08-23')).all())
    
    tobs_df = pd.DataFrame(tobs)

    tobs_avg = tobs_df["tobs"].mean()
    tobs_max = tobs_df["tobs"].max()
    tobs_min = tobs_df["tobs"].min()
    
    return jsonify(tobs_avg, tobs_max, tobs_min)

@app.route('/api/v1.0/<start>/<end>') 
def startend(start=None, end=None):

    tobs = (session.query(Measurement.tobs).filter(Measurement.date.between(start, end)).all())
    
    tobs_df = pd.DataFrame(tobs)

    tobs_avg = tobs_df["tobs"].mean()
    tobs_max = tobs_df["tobs"].max()
    tobs_min = tobs_df["tobs"].min()
    
    return jsonify(tobs_avg, tobs_max, tobs_min)

if __name__ == '__main__':
    app.run(debug=True)