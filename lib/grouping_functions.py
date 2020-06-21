# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 21:18:45 2020

@author: Emmanuel Byrd Suárez
"""

import numpy as np

def daily_deaths_global(df, earliest_day, latest_day, codes):
    subset = df[(df['death_cie10'].isin(codes)) & 
                (df['day_global_index'].between(earliest_day, latest_day))]
    
    daily = subset.groupby('day_global_index').count()[['causa_def']]
    
    days_list = list(range(earliest_day, latest_day+1))
    
    daily = daily.reindex(days_list, fill_value=0)
    daily.rename(columns={'causa_def': 'deaths_sum'}, inplace=True)
    
    return daily

def daily_deaths(df):
    daily = df.groupby('day_of_year_index').count()[['causa_def']]
    
    days_list = list(range(1, 366))
    
    daily = daily.reindex(days_list, fill_value=0)
    daily.rename(columns={'causa_def': 'deaths_sum'}, inplace=True)
    
    return daily, np.array(daily.index).squeeze()

