# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 18:05:45 2020

@author: Emmanuel Byrd Suárez
"""

import os
import numpy as np
import pandas as pd
import functools
from tqdm import tqdm
from simpledbf import Dbf5
from datetime import datetime
from calendar import monthrange

dbf_dir = './Mortalidad-INEGI/dbf'
dbf_years = ['05', '06', '07', '08', '09', '10', '11']

csv_dir = './Mortalidad-INEGI/csv'
csv_years = [2012, 2013, 2014, 2015, 2016, 2017, 2018]
csv_paths = [
  'defunciones_generales_2012.csv',
  'defunciones_generales_2013.csv',
  'defunciones_generales_2014.csv',
  'defunciones_generales_2015.csv',
  'defunciones_generales_2016.csv',
  'conjunto_de_datos_defunciones_generales_2017.CSV',
  'conjunto_de_datos_defunciones_registradas_2018.csv']

hdf_output_dir = 'deaths_hdf'
hdf_output_name = 'deaths_05_18_clean_checkpoint_1.h5'

def code_range(letter, start, end_inclusive):
    num = list(map(lambda i: str(i).zfill(2), 
                   list(range(start, end_inclusive+1))))
    return list(map(lambda n: letter + n, num))

codes = code_range('J', 9, 18)

useful_cols = [
    'ent_resid', 'causa_def', 'sexo', 'dia_ocurr',
    'mes_ocurr', 'anio_ocur', 'edad_agru']

records_tracker = {}

def data_of_interest(df, rec_year):
    df = df.replace(np.nan, '', regex=True)
    df = df[useful_cols]
    
    year = str(rec_year)
    records_tracker[year] = {'original': df.shape[0]}
    
    df['death_cie10'] = df['causa_def'].astype(str).str[:3]
    df = df[df['death_cie10'].isin(codes)]
    # 5-99 years old, exclude unspecified
    df = df[df['edad_agru'].isin(range(6, 25))]
    # male or female, exclue unspecified
    df = df[df['sexo'].isin([1, 2])]
    df = df.loc[df['anio_ocur'] >= 2004]
    # exclude unspecified month of death
    df = df.loc[df['mes_ocurr'] != 99]
    # exclude unspecified day of death
    df = df.loc[df['dia_ocurr'] != 99]
    
    records_tracker[year]['final'] = df.shape[0]
    
    return df

def clean_cols(df):
    df['ent_resid'] = df['ent_resid'].astype(int)
    df['edad_agru'] = df['edad_agru'].astype(int)
    return df

def correct_day_of_row(row):
    day = row['dia_ocurr']
    try:
        datetime(row['anio_ocur'], row['mes_ocurr'], row['dia_ocurr'])
    except ValueError:
        # I found in practice that all errors account for
        # days being above the range of the specified month,
        # and decided to fix it to its corresponding maximum day.
        # Another alternative is to drop these rows.
        day = monthrange(row['anio_ocur'], row['mes_ocurr'])[1]
    return day

def correct_values(df):
    df['dia_ocurr'] = df.apply(correct_day_of_row, axis=1)
    return df

def convert_dbfs_to_dataframes():
    print("Converting .dbf to Dataframes...")
    
    dataframes = []
    
    for year in tqdm(dbf_years):
        df = Dbf5(os.path.join(dbf_dir, "DEFUN" + year) + ".dbf")
        df = df.to_dataframe()
        df.columns = map(str.lower, df.columns)
        
        df = clean_cols(df)
        df = data_of_interest(df, 2000 + int(year))
        df = correct_values(df)
        
        dataframes.append(df)
        
    print("Done.")
    
    return dataframes

def convert_csvs_to_dataframes():
    print("Converting .csv to Dataframes...")
    
    dataframes = []
    
    for i, path in enumerate(tqdm(csv_paths)):
        df = pd.read_csv(os.path.join(csv_dir, path),
                         delimiter=",", header=0, encoding='latin-1')
        
        df = clean_cols(df)
        
        year = csv_years[i]
        df = data_of_interest(df, year)
        
        df = correct_values(df)
        dataframes.append(df)
    
    print("Done.")
        
    return dataframes

dataframes_05_11 = convert_dbfs_to_dataframes()
deaths_05_11 = functools.reduce(lambda a, b: a.append(b), dataframes_05_11)

dataframes_12_18 = convert_csvs_to_dataframes()
deaths_12_18 = functools.reduce(lambda a, b: a.append(b), dataframes_12_18)

deaths = deaths_05_11.append(deaths_12_18)
deaths.to_hdf(os.path.join(hdf_output_dir, hdf_output_name),
              key='deaths', format='table')

print(records_tracker)

original = 0
final = 0
for year in records_tracker:
    original += records_tracker[year]['original']
    final += records_tracker[year]['final']
    
print("Original rows: " + str(original))
print("Selected rows: " + str(final))