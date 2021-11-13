
def solving_columns(dataf):
    dataf["payment_type"] = dataf["payment_type"].str.lower()
    dataf['pickup_datetime'] = pd.to_datetime(dataf['pickup_datetime']) 
    dataf['dropoff_datetime'] = pd.to_datetime(dataf['dropoff_datetime'])
    dataf['min_diff'] = (dataf['dropoff_datetime'] - dataf['pickup_datetime'])/ pd.Timedelta(minutes=1)
    dataf['pickup_day']= dataf['pickup_datetime'].dt.strftime("%Y-%m-%d").astype("datetime64")
    dataf['pickup_hour']= dataf['pickup_datetime'].dt.strftime("%H:%M:%S")
    dataf['dropoff_day']= dataf['dropoff_datetime'].dt.strftime("%Y-%m-%d").astype("datetime64")
    dataf['dropoff_hour']= dataf['dropoff_datetime'].dt.strftime("%H:%M:%S")
    dataf['Dia_semana'] = dataf['pickup_day'].dt.dayofweek
    dataf.drop(columns=['rate_code','store_and_fwd_flag','pickup_datetime','dropoff_datetime'], axis=1, inplace=True)
    return dataf
