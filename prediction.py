import settings

import datetime
import math


import numpy as np
import pandas as pd
import tensorflow as tf

import os

residentsAtHome = pd.read_csv(settings.DATA_URL, sep=",")

# slice [start:stop:step], starting from index 0 take every 3th record -> every half an hour
residentsAtHome = residentsAtHome[0::3]

residentsAtHome.columns = ['datetime', 'numResidents', 'holiday','actualTemp']

residentsAtHome.pop('actualTemp')

# extract real number of residents from 6:00
startTime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(hours=6, minutes=0)
# print(startTime)

real_residentsAtHome = residentsAtHome.loc[(residentsAtHome['datetime'] >= startTime.strftime('%Y-%m-%d %H:%M:%S'))]['numResidents'] 
# print(real_residentsAtHome)

date_time = pd.to_datetime(residentsAtHome.pop('datetime'), format='%Y-%m-%d %H:%M:%S')
timestamp_s = date_time.map(datetime.datetime.timestamp)

day = 24*60*60
week = 7*day
twoWeek = 2*week

residentsAtHome['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
residentsAtHome['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))

residentsAtHome['Week sin'] = np.sin(timestamp_s * (2 * np.pi / week))
residentsAtHome['Week cos'] = np.cos(timestamp_s * (2 * np.pi / week))

residentsAtHome['Two weeks sin'] = np.sin(timestamp_s * (2 * np.pi / twoWeek))
residentsAtHome['Two weeks cos'] = np.cos(timestamp_s * (2 * np.pi / twoWeek))


column_indices = {name: i for i, name in enumerate(residentsAtHome.columns)}

n = len(residentsAtHome)
train_residentsAtHome = residentsAtHome[0:int(n*1)]

num_features = residentsAtHome.shape[1]

class WindowGenerator():
  def __init__(self, input_width, label_width, shift,
               train_df=train_residentsAtHome,
               label_columns=None):
    # Store the raw data.
    self.train_df = train_df

    # Work out the label column indices.
    self.label_columns = label_columns
    if label_columns is not None:
      self.label_columns_indices = {name: i for i, name in
                                    enumerate(label_columns)}
    self.column_indices = {name: i for i, name in
                           enumerate(train_df.columns)}

    # Work out the window parameters.
    self.input_width = input_width
    self.label_width = label_width
    self.shift = shift

    self.total_window_size = input_width + shift

    self.input_slice = slice(0, input_width)
    self.input_indices = np.arange(self.total_window_size)[self.input_slice]

    self.label_start = self.total_window_size - self.label_width
    self.labels_slice = slice(self.label_start, None)
    self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

  def split_window(self, features):
    inputs = features[:, self.input_slice, :]
    labels = features[:, self.labels_slice, :]
    if self.label_columns is not None:
      labels = tf.stack(
          [labels[:, :, self.column_indices[name]] for name in self.label_columns],
          axis=-1)

    # Slicing doesn't preserve static shape information, so set the shapes
    # manually. This way the `tf.data.Datasets` are easier to inspect.
    inputs.set_shape([None, self.input_width, None])
    labels.set_shape([None, self.label_width, None])

    return inputs, labels

  def make_dataset(self, data):
    data = np.array(data, dtype=np.float32)
    ds = tf.keras.preprocessing.timeseries_dataset_from_array(
        data=data,
        targets=None,
        sequence_length=self.total_window_size,
        sequence_stride=1,
        shuffle=True,
        batch_size=32,)

    ds = ds.map(self.split_window)

    return ds


  @property
  def train(self):
    return self.make_dataset(self.train_df)


MAX_EPOCHS = settings.MAX_EPOCHS

def compile_and_fit(model, window, patience=2):
  model.compile(loss=tf.losses.MeanSquaredError(),
                optimizer=tf.optimizers.Adam(),
                metrics=[tf.metrics.MeanAbsoluteError()])

  history = model.fit(window.train, epochs=MAX_EPOCHS, verbose=0)
  return history


INPUT_WIDTH = 36
OUT_STEPS = 36
multi_window = WindowGenerator(input_width=INPUT_WIDTH, label_width=OUT_STEPS, shift=OUT_STEPS)


multi_dense_model = tf.keras.Sequential([
    # Take the last time step.
    # Shape [batch, time, features] => [batch, 1, features]
    tf.keras.layers.Lambda(lambda x: x[:, -1:, :]),
    # Shape => [batch, 1, dense_units]
    tf.keras.layers.Dense(512, activation='relu'),
    # Shape => [batch, out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*num_features, kernel_initializer=tf.initializers.zeros),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, num_features])
])

history = compile_and_fit(multi_dense_model, multi_window)


startTimestamp_s = startTime.timestamp()
#print(startTimestamp_s)

prediction_data=[]
for n in range(36):
  data_point = [
    0,
    0,
    np.sin(startTimestamp_s * (2 * np.pi / day)),
    np.cos(startTimestamp_s * (2 * np.pi / day)),
    np.sin(startTimestamp_s * (2 * np.pi / week)),
    np.cos(startTimestamp_s * (2 * np.pi / week)),
    np.sin(startTimestamp_s * (2 * np.pi / twoWeek)),
    np.cos(startTimestamp_s * (2 * np.pi / twoWeek))
  ]
  prediction_data.append(data_point)
  startTimestamp_s += 1800

#print(prediction_data)

prediction_df = pd.DataFrame(prediction_data, columns=['numResidents', 'holiday', 'Day sin', 'Day cos', 'Week sin', 'Week cos', 'Two weeks sin', 'Two weeks cos'])

def split_window(features):
  inputs = features[:, slice(0, INPUT_WIDTH), :]
  labels = features[:, slice(0, 36), :]
  
  if prediction_df.columns is not None:

    # Work out the label column indices.
    label_columns = ["numResidents"]
    if label_columns is not None:
      label_columns_indices = {name: i for i, name in
                                    enumerate(label_columns)}
    column_indices = {name: i for i, name in
                           enumerate(prediction_df.columns)}

    labels = tf.stack(
        [labels[:, :, column_indices[name]] for name in label_columns],
        axis=-1)

  # Slicing doesn't preserve static shape information, so set the shapes
  # manually. This way the `tf.data.Datasets` are easier to inspect.
  inputs.set_shape([None, INPUT_WIDTH, None])
  labels.set_shape([None, 36, None])

  return inputs, labels

def make_dataset(data):
  data = np.array(data, dtype=np.float32)
  ds = tf.keras.preprocessing.timeseries_dataset_from_array(
      data=data,
      targets=None,
      sequence_length=36,
      sequence_stride=1,
      shuffle=True,
      batch_size=32,)

  ds = ds.map(split_window)

  return ds

prediction_tensor=make_dataset(prediction_df)




prediction = multi_dense_model.predict(prediction_tensor)
# print(prediction)

targetTemps = settings.targetTemps
targetTemp = []
predicted_residentsAtHome = []
times = []
for i in range(36):
  times.append(startTime.strftime("%H:%M")) 
  predicted_residentsAtHome.append(prediction[0][i][0])
  if predicted_residentsAtHome[i] < settings.switchingThresholds[0]:
    targetTemp.append(targetTemps[0])
  elif predicted_residentsAtHome[i] >= settings.switchingThresholds[0] and predicted_residentsAtHome[i] < settings.switchingThresholds[1]:
    targetTemp.append(targetTemps[1])
  else:
    targetTemp.append(targetTemps[2])
  print(times[i], predicted_residentsAtHome[i], targetTemp[i]) # print(startTime, prediction[0][i][0])
  startTime+=datetime.timedelta(minutes=30)


