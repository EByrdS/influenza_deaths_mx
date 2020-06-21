# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 21:16:12 2020

@author: Emmanuel Byrd Suárez
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from lib.grouping_functions import daily_deaths_global
from lib.constants import YEARS_STABLE_DAYS

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

def multiplot_365(dfs, title, labels):    
    plt.figure(figsize=(15,5))
    for i, df in enumerate(dfs):
        plt.plot(df, label=labels[i])
    plt.title(title)
    plt.xlabel('Day of the year')
    plt.ylabel('Deaths sum')
    plt.legend()
    plt.show()

def by_global_day_range(df, s, e, codes):
    daily = daily_deaths_global(df, s, e, codes)
    
    years_avgs = pd.merge(YEARS_STABLE_DAYS, daily,
                          left_index=True, right_index=True)
    years_behavior = years_avgs.groupby('center').mean()['deaths_sum']
    
    for_regression = years_behavior.to_frame()
    for_regression.columns = ['avg_deaths']
    
    
    x = np.array(for_regression.index).squeeze()
    y = np.array(for_regression[['avg_deaths']]).squeeze()
    log_y_data = np.log(y)
    
    fit_params = np.polyfit(x, log_y_data, 1)
    y_pred = np.exp(fit_params[1]) * np.exp(fit_params[0]*x)
    
    plt.figure(figsize=(15,5))
    plt.plot(daily, linewidth=1)
    plt.plot(years_behavior, marker='o', color='red', linewidth=1)
    plt.plot(x, y_pred, marker='.', color='#00D803', linewidth=1)
    plt.title("Daily deaths of codes '" + str(codes) + "', grouped.")
    plt.xlim(s, e)
    plt.ylabel('Number of deaths')
    plt.xlabel('Day number')
    plt.show()
    
    behavior_fit_df = pd.DataFrame(y_pred,
                                 index=x,
                                 columns=['deaths_fit'])
    
    return daily, years_behavior, behavior_fit_df, fit_params

def poly_fit_365(daily_df, degree, plot=False, concept=None):
    x_range = list(range(1, 366))
    x = np.array(daily_df.index).squeeze()[:, np.newaxis]
    y = np.array(daily_df[['deaths_sum']].squeeze())[:, np.newaxis]
    
    poly_features = PolynomialFeatures(degree=degree)
    x_poly = poly_features.fit_transform(x)
    
    model = LinearRegression(normalize=True)
    model.fit(x_poly, y)
    y_pred = model.predict(x_poly)
    
    prediction = pd.DataFrame(y_pred,
                              index=x_range,
                              columns=['deaths_sum'])
    if plot:
      rmse = np.sqrt(mean_squared_error(y, y_pred))
      r2 = r2_score(y, y_pred)
      print("RMSE of behavior curve: " + str(round(rmse, 4)))
      print("R2 score of behavior curve: " + str(r2))
    
      plt.figure(figsize=(15,5))
      plt.plot(daily_df)
      plt.plot(x, y_pred, color='green', linewidth=1)
      plt.title(concept + " with fit curve of " + str(degree) + " degree.")
      plt.xlim(0, x_range[-1]) # xlim starts in 0?
      plt.ylabel('Number of deaths')
      plt.xlabel('Day number')
      plt.show()
    
    return prediction, model
    
def multi_plot_with_format(data, title, x_label, y_label, labels):
    plt.figure(figsize=(15,5))
    for i, data in enumerate(data):
        plt.plot(data, label=labels[i])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()