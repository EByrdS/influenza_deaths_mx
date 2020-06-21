# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 19:31:32 2020

@author: Emmanuel Byrd Suárez
"""

import os
import pandas as pd
from datetime import datetime
from constants import DAYS_CUMULATIVES

hdf_dir = 'deaths_hdf'
hdf_source_name = 'deaths_05_18_clean_checkpoint_1.h5'
hdf_output_name = 'deaths_05_18_new_cols_checkpoint_1.h5'

deaths = pd.read_hdf(os.path.join(hdf_dir, hdf_source_name))
source_shape = deaths.shape

# import utils
    
def incr_day_by_year(row):
    year = row['anio_ocur']
    jan_first = datetime(year, 1, 1)
    
    date = datetime(year, row['mes_ocurr'], row['dia_ocurr'])
    
    return (date - jan_first).days + 1


def incr_day_global(row):
    return row['day_of_year_index'] + DAYS_CUMULATIVES[row['anio_ocur']]

def new_age_group(row):
    age_grouping = {
      6: 0, # 5-9 years old...
      7: 1, # 10-14
      8: 1, # 15-19
      9: 2, # 20-24
      10: 2, # 25-29
      11: 3, # 30-34
      12: 3, # 35-39
      13: 4, # 40-44
      14: 4, # 45-49
      15: 5, # 50-54
      16: 5, # 55-59
      17: 6, # 60-64
      18: 6, # 65-69
      19: 7, # 70-74
      20: 7, # 75-79
      21: 8, # 80-84
      22: 8, # 85-89
      23: 9, # 90-94
      24: 9 # 95-99
    }
    return age_grouping[row['edad_agru']]

deaths['new_age_group'] = deaths.apply(new_age_group, axis=1)
deaths['day_of_year_index'] = deaths.apply(incr_day_by_year, axis=1)
deaths['day_global_index'] = deaths.apply(incr_day_global, axis=1)
deaths = deaths[deaths['day_global_index'] >= 0]
final_shape = deaths.shape

deaths.to_hdf(os.path.join(hdf_dir, hdf_output_name), 
              key='deaths', format='table')

print("Original shape: " + str(source_shape))
print("Final shape: " + str(final_shape))