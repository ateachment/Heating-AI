import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split # pip install scikit-learn
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor

import settings
import os
import datetime

df = pd.read_csv(settings.DATA_URL,
                 names=['timestamp','residents','holiday','temperature'],
                 parse_dates=['timestamp'])
df = df.set_index('timestamp')
#print(df.head())

# bring data to half hour intervals
half_hour = df.resample('30min').last()

# Zustände fortschreiben
half_hour[['residents','holiday','temperature']] = \
    half_hour[['residents','holiday','temperature']].ffill()  # fill falls zu dem Zeitpunkt ein Log fehlt

#print(half_hour.head())


# prepare data for training (feature engineering: 
# 06:00–22:00 o'clock, yesterdays evening 18–22 mean, weekday, month, week parity, holiday, target: number of residents at home in the next 33 half hours)

days = []

for day, group in half_hour.groupby(half_hour.index.date):
    day_slice = group.between_time('06:00','22:00')

    # gestriger Abend 18–22 Uhr
    yesterday = pd.Timestamp(day) - pd.Timedelta(days=1)
    yesterday_slice = half_hour.loc[
        (half_hour.index.date == yesterday.date())
    ].between_time('18:00','22:00')

    if len(day_slice) == 33 and len(yesterday_slice) > 0:
        target = day_slice['residents'].values

        yesterday_evening_state = yesterday_slice['residents'].mean()

        days.append({
            'date': day,
            'weekday': day_slice.index[0].weekday(),
            'month': day_slice.index[0].month,
            'week_parity': day_slice.index[0].week % 2,
            'holiday': int(day_slice['holiday'].iloc[0]),
            'yesterday_evening_state': yesterday_evening_state,
            'target': target
        })

daily = pd.DataFrame(days)
daily = pd.DataFrame(days)
#print(daily.head())

# Features and target matrix
X = daily[['weekday','month','week_parity','holiday','yesterday_evening_state']]
Y = np.vstack(daily['target'].values)

# Train model with ALL available data (not just 80% for real prediction)
model = MultiOutputRegressor(RandomForestRegressor())
model.fit(X, Y)

# For real prediction: predict for the NEXT day (today) based on yesterday's evening data
# Assume the last day in our dataset is "yesterday" and we want to predict "today"

# Get yesterday's date (last day in dataset)
yesterday_date = daily['date'].iloc[-1]

# Calculate features for today
today = yesterday_date + pd.Timedelta(days=1)

# Check if we have data for today and get holiday information from it
today_data = df[df.index.date == today]
holiday_today = int(today_data['holiday'].iloc[0]) if len(today_data) > 0 else 0

yesterday = today - pd.Timedelta(days=1)
yesterday_key = yesterday.date() if hasattr(yesterday, 'date') else yesterday
yesterday_evening_state = df.loc[df.index.date == yesterday_key].between_time('18:00','22:00')['residents'].mean()

today_features = {
    'weekday': today.weekday(),
    'month': today.month,
    'week_parity': today.isocalendar().week % 2,
    'holiday': holiday_today,  # Get holiday info from today's data (3rd column)
    'yesterday_evening_state': yesterday_evening_state
}

# Make prediction for today
today_X = pd.DataFrame([today_features])
prediction_today = model.predict(today_X)[0]  # Get the prediction array

print(f"Prediction for {today.strftime('%Y-%m-%d')} (today):")
print(f"Based on yesterday evening average of residents (18:00–22:00): {today_features['yesterday_evening_state']:.2f} residents")


# Model trained with all available data for real predictions
print(f"Model trained with {len(X)} days of historical data")
print(f"Last available day: {yesterday_date.strftime('%Y-%m-%d')}")


# predict for the following day (the current day at 6 AM, data available until 5:30 AM)
targetTemps = settings.targetTemps
targetTemp = []
predicted_residentsAtHome = []
times = []

# Use today's prediction
startTime = pd.Timestamp("06:00").time()

for i in range(len(prediction_today)):
  times.append(startTime.strftime("%H:%M"))
  predicted_residentsAtHome.append(prediction_today[i])
  if predicted_residentsAtHome[i] < settings.switchingThresholds[0]:
    targetTemp.append(targetTemps[0])
  elif predicted_residentsAtHome[i] >= settings.switchingThresholds[0] and predicted_residentsAtHome[i] < settings.switchingThresholds[1]:
    targetTemp.append(targetTemps[1])
  else:
    targetTemp.append(targetTemps[2])
  startTime = (pd.Timestamp.combine(pd.Timestamp.today(), startTime) + pd.Timedelta(minutes=30)).time()

with open(os.path.join(os.path.dirname(__file__),'data', settings.PREDICTION_FILENAME),"w") as file:
  for i in range(len(predicted_residentsAtHome)):    
    file.write(times[i] + settings.SEPARATOR + str(predicted_residentsAtHome[i]) + settings.SEPARATOR + str(targetTemp[i]) + "\n") 
  file.close() 

