import pandas as pd
import numpy as np
import datetime
import sklearn
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score, r2_score 
from math import sqrt

def my_model(data, time_step, num_day_shown):
   #Scale the data
   scaler = MinMaxScaler(feature_range = (0, 1))
   close_data = scaler.fit_transform(np.array(data['close']).reshape(-1, 1))

   #Split train and valid set
   train_size = int(close_data.shape[0] * 0.8)
   train_data, valid_data = close_data[0:train_size, :], close_data[train_size:close_data.shape[0],]
   #Create train and valid set for modeling
   X_train, y_train = [], []
   for i in range(len(train_data)- time_step - 1):
      a = train_data[i:(i+time_step), 0]  
      X_train.append(a)
      y_train.append(train_data[i + time_step, 0])
   
   X_valid, y_valid = [], []
   for i in range(len(close_data) - len(valid_data) - time_step, len(close_data) - time_step):
      a = close_data[i:(i+time_step), 0]
      X_valid.append(a)
      y_valid.append(close_data[i + time_step, 0])

   #Model
   model = SVR(kernel= 'rbf', C= 1e2, gamma= 0.1)
   model.fit(X_train, y_train)

   print(len(X_valid))
   #Predict X_valid
   valid_pred = model.predict(X_valid)
   
   #Evaluate
   rmse = round(sqrt(mean_squared_error(valid_data, valid_pred)), 2)
   mae = round(mean_absolute_error(valid_data, valid_pred), 2)
   evs = round(explained_variance_score(valid_data, valid_pred), 2)
   r2s = round(r2_score(valid_data, valid_pred), 2)

   #Inverse transform
   valid_pred = valid_pred.reshape(-1, 1)
   valid_pred = scaler.inverse_transform(valid_pred)
   valid_pred = valid_pred.ravel()

   #Append new valid prediction column
   data['valid_pred'] = np.nan
   data['valid_pred'].iloc[close_data.shape[0] - len(valid_pred):close_data.shape[0]] = valid_pred
   
   #Predict next 15 days price
   future_pred = np.empty(shape= (1, 0))
   X_init = close_data[close_data.shape[0] - time_step:close_data.shape[0], :].reshape(1, -1)
   num_day_pred = 15
   while num_day_pred > 0:
      next_day = model.predict(X_init)
      X_init = X_init[:, 1:time_step].reshape(1, -1)
      X_init = np.append(X_init, next_day)
      X_init = X_init.reshape(1, time_step)
      future_pred = np.append(future_pred, next_day)
      num_day_pred -= 1
   
   #Inverse transform future prediction
   future_pred = future_pred.reshape(-1, 1)
   future_pred = scaler.inverse_transform(future_pred)
   future_pred = future_pred.ravel()
   
   #Extend dataset with future prediction   
   last_date = str(data['date'].iloc[-1])[:10]
   last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d")
   date_list = []
   for i in range(1, 15 + 1):
      date_list.append((last_date + datetime.timedelta(days= i)).strftime("%Y-%m-%d"))
   new = {'date': date_list}
   data = data.append(pd.DataFrame(new))
   
   #Append new future prediction column
   data['future_pred'] = np.nan
   data['future_pred'].iloc[close_data.shape[0]:data.shape[0]] = future_pred
   
   #Slice dataset
   data.to_csv('data.csv', index= False)
   data = data.iloc[data.shape[0] - num_day_shown:data.shape[0]]
   
   return data, rmse, mae, evs, r2s
