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


app = Flask(__name__)

@app.route('/')
def main():
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
    
    slice_for_zip_code = df.loc[df['dropoff_zip_code'] == str(inp)]
    df_daily_ride_count = slice_for_zip_code.groupby(['trip_date'])['trip_id'].count().reset_index(name ='total_trips')
    df_weekly_ride_count = slice_for_zip_code.groupby(['trip_week'])['trip_id'].count().reset_index(name ='total_trips')
    df_monthly_ride_count = slice_for_zip_code.groupby(['trip_month'])['trip_id'].count().reset_index(name ='total_trips')

    df_end_trip_count = df.groupby(['trip_end_timestamp_clean'])['trip_id'].count().reset_index(name ='Total_Number_of_orders_per_month')
    df_end_trip_count

    df_end_trip_count = df_end_trip_count.rename(columns = {'trip_end_timestamp_clean': 'ds',
                                    'Total_Number_of_orders_per_month': 'y'})
    
    model = Prophet(yearly_seasonality=True, daily_seasonality=True)
    model.fit(df_end_trip_count) 
    future_dates = model.make_future_dataframe(periods = 50, freq='W')
    forecast = model.predict(future_dates)

    model.plot(forecast);
    
    return 


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)