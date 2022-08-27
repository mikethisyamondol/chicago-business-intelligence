from flask import Flask
import psycopg2
import pandas as pd
import prophet
import os
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.plot import plot_plotly, plot_components_plotly


def preds():
     # inp = input('Please Provide a Zip Code in Chicago.')
    inp = '60604'
    conn = psycopg2.connect(
        dbname='chicago_business_intelligence',
        host=os.environ.get('DB_HOST'),
        port=5432,
        user='postgres',
         password='root'
    )
    
    cur = conn.cursor()
    conn.autocommit=True
    
    query = '''
        select
        id,
        trip_id,
        date(trip_start_timestamp) as trip_date,
        date(date_trunc('week', trip_start_timestamp) + '6 days'::interval) as trip_week,
        to_char(trip_start_timestamp, 'YYYY-MM') as trip_month,
        pickup_zip_code,
        dropoff_zip_code
        from public.taxi_trips
        where dropoff_zip_code is not null
        and dropoff_zip_code != ''
        '''
    
    df = pd.read_sql(query, conn)
    
    # slice_for_zip_code = df.loc[df['dropoff_zip_code'] == str(inp)]
    # df_daily_ride_count = slice_for_zip_code.groupby(['trip_date'])['trip_id'].count().reset_index(name ='total_trips')
    # df_weekly_ride_count = slice_for_zip_code.groupby(['trip_week'])['trip_id'].count().reset_index(name ='total_trips')
    # df_monthly_ride_count = slice_for_zip_code.groupby(['trip_month'])['trip_id'].count().reset_index(name ='total_trips')

    df_trip_count = df.groupby(['trip_month'])['trip_id'].count().reset_index(name ='Total_Rides_Per_Month')
    
    df_trip_count = df_trip_count.rename(columns = {'trip_month': 'ds',
                                    'Total_Rides_Per_Month': 'y'})
    
    model = Prophet(yearly_seasonality=True, daily_seasonality=True)
    model.fit(df_trip_count) 
    future_dates = model.make_future_dataframe(periods = 50, freq='W')
    forecast = model.predict(future_dates)

    # model.plot(forecast);


    model.plot_components(forecast).savefig('static/IMG/predict_image.png')


app = Flask(__name__)

img = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = img

@app.route('/')
def main():
    preds()
    predict_img = os.path.join(app.config['UPLOAD_FOLDER'], 'predict_image.png')
    return render_template("index.html", user_image=predict_img)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)