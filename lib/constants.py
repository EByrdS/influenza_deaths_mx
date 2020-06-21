# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 20:51:25 2020

@author: Emmanuel Byrd Suárez
"""

import pandas as pd
from datetime import datetime

years = range(2004, 2018 + 1)
pivot_day = (366 // 2) + 50
pivot_day_reach = 14 

def create_days_of_year():
    days_of_year = {}
    
    for year in list(years):
        jan_first = datetime(year, 1, 1)
        dec_31 = datetime(year, 12, 31)
        days_of_year[year] = (dec_31 - jan_first).days + 1
    
    return days_of_year

def create_days_cumulatives():
    days_of_year = create_days_of_year()
    days_cumulatives = {
        years[0]: -days_of_year[years[0]],
        years[1]:0
    }

    for year in list(years)[2:]:
        days_cumulatives[year] = (days_cumulatives[year-1] + 
                                  days_of_year[year-1])
    
    return days_cumulatives

def create_years_center():
    days_cumulatives = create_days_cumulatives()
    years_center = {}
    
    for year in list(days_cumulatives.keys())[1:]:
        years_center[year] = days_cumulatives[year] + pivot_day
        
    return years_center

def create_years_stable_days():
    years_center = create_years_center()
    years_center_series = []
    days_series = []
    
    for year in years_center:
        years_center_series += [years_center[year]]*(pivot_day_reach*2)
        days_series += list(range(years_center[year] - pivot_day_reach,
                                  years_center[year] + pivot_day_reach))
    
    # It is not really the 'center' of the year,
    # it is the center in which to plot the average of deaths
    # within a range of days I found with less variance.
    years_avg_days = pd.DataFrame(years_center_series,
                                  index=days_series,
                                  columns=['center'])
    
    return years_avg_days

DAYS_OF_YEAR = create_days_of_year()
DAYS_CUMULATIVES = create_days_cumulatives()
YEARS_CENTER = create_years_center()
YEARS_STABLE_DAYS = create_years_stable_days()
START_DAY_AVG = pivot_day - pivot_day_reach
END_DAY_AVG = pivot_day + pivot_day_reach
COL_MEANINGS = {
    'sexo':{
        'en': 'sex',
        'vals': {
            1: 'men',
            2: 'women',
            9: 'unspecified'
        }
    },
    'ent_resid':{
        'en': 'living state',
        'vals': {
          1: 'Aguascalientes',
          2: 'Baja California',
          3: 'Baja California Sur',
          4: 'Campeche',
          5: 'Coahuila',
          6: 'Colima',
          7: 'Chiapas',
          8: 'Chihuahua',
          9: 'Mexico City',
          10: 'Durango',
          11: 'Guanajuato',
          12: 'Guerrero',
          13: 'Hidalgo',
          14: 'Jalisco',
          15: 'State of Mexico',
          16: 'Michoacan',
          17: 'Morelos',
          18: 'Nayarit',
          19: 'Nuevo Leon',
          20: 'Oaxaca',
          21: 'Puebla',
          22: 'Queretaro',
          23: 'Quintana Roo',
          24: 'San Luis Potosi',
          25: 'Sinaloa',
          26: 'Sonora',
          27: 'Tabasco',
          28: 'Tamaulipas',
          29: 'Tlaxcala',
          30: 'Veracruz',
          31: 'Yucatan',
          32: 'Zacatecas',
          33: 'United States of America',
          34: 'other countries of latin america',
          35: 'other countries',
          88: 'does not apply for A00-R99 and V90-Y89',
          99: 'unspecified'            
        }
    },
    'new_age_group': {
        'en': 'age group',
        'vals': {
            0: '5-9',
            1: '10-19',
            2: '20-29',
            3: '30-39',
            4: '40-49',
            5: '50-59',
            6: '60-69',
            7: '70-79',
            8: '80-89',
            9: '90-99'
        }
    }
}
