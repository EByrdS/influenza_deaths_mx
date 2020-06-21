# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 20:21:14 2020

@author: Emmanuel Byrd Suárez
"""

import os
import numpy as np
import pandas as pd
import functools

from lib.plot_functions import (daily_deaths_global, multi_plot_with_format,
                                by_global_day_range, poly_fit_365,
                                multiplot_365)
from lib.grouping_functions import daily_deaths
from lib.constants import (DAYS_CUMULATIVES, YEARS_CENTER, START_DAY_AVG, 
                           END_DAY_AVG, COL_MEANINGS)

hdf_dir = os.path.join('data', 'deaths_hdf')
hdf_source_name = 'deaths_05_18_new_cols_checkpoint_1.h5'

deaths = pd.read_hdf(os.path.join(hdf_dir, hdf_source_name))

target_disease = ['J09', 'J10', 'J11', 'J13', 'J14']
deviating_codes = ['J12', 'J15', 'J16', 'J18']

t = deaths[deaths['death_cie10'].isin(target_disease + deviating_codes)]
print(t['death_cie10'].value_counts())


"""
Code names retrieved from: https://icd.who.int/browse10/2016/en (20/06/2020)
J09-J18: Influenza and pneumonia

J09: Influenza due to identified zoonotic or pandemic influenza virus
J10: Influenza due to identified seasonal influenza virus
J11: Influenza, virus not identified
J12: Viral pneumonia, not elsehwere classified
J13: Pneumonia due to Streptococcus pneumoniae
J14: Pneumonia due to Haemophilus influenzae
J15: Bacterial pneumonia, not elsewhere classified
J16: Pneumonia due to other infectious organisms, not elsewhere classified
J17: * Pneumonia in diseases classified elsewhere
J18: Pneumonia, organism unspecified

* Does not apply for a cause of death and so it does not appear in the DB.
"""

"""
Thought process:
1. The group of diseases J12, J16, J15, J16, J18 have a predictable behavior.
2. For that group in 2009, there will be more deaths than expected.
2.1 We need to count how many are above our prediction.
3. The group of diseases J09, J10, J11, J13, J14 will have a similar behavior
   as the difference obtained in 2.1.
"""
    
def scale_years(source, death_codes, source_years, factors, 
                divide_col=None, divide_val=None):
    selection = source['death_cie10'].isin(death_codes)
    if divide_col is not None:
      selection = selection & (source[divide_col] == divide_val)
    
    df = source[selection]
    
    dataframes = []
    for year in source_years:
        subset = df[df['anio_ocur'] == year]
        daily, _ = daily_deaths(subset)
      
        daily['deaths_sum'] = daily['deaths_sum'] * factors[year]
        daily['year'] = year
        daily = daily.reset_index()
        dataframes.append(daily)
    
    return functools.reduce(lambda a, b: a.append(b), dataframes)

def get_years_growth_factor(source, codes, source_years, target_avg):
    df = source[(source['death_cie10']).isin(codes)]
    
    dataframes = []
    factors = {}
    for year in source_years:
        subset = df[df['anio_ocur'] == year]
        daily, _ = daily_deaths(subset)
        year_avg = year_selected_avg(daily)
        
        factor = target_avg / year_avg
        factors[year] = factor
        daily['deaths_sum'] = daily['deaths_sum'] * factor
        daily['year'] = year 
        daily = daily.reset_index()
        dataframes.append(daily)
        
    return functools.reduce(lambda a, b: a.append(b), dataframes), factors

def year_selected_avg(daily_df):
    for_avg = daily_df.iloc[START_DAY_AVG:END_DAY_AVG+1]
    
    return for_avg.mean()['deaths_sum']

def get_difference(deaths, divide_by, train_years, target_year, target_disease,
                   deviating_codes, train_fit_degree, hard_fit_degree):
    days_range = list(range(1, 366))
    
    subgroups = list(deaths[divide_by].unique())
    subgroups.sort()
    
    df_by_day, y_growth, y_fit, exp_params = (
        by_global_day_range(deaths, DAYS_CUMULATIVES[train_years[0]], 
                            DAYS_CUMULATIVES[train_years[-1]+1], 
                            deviating_codes)
        )
    
    target_ref_day = YEARS_CENTER[target_year]
    target_ref_pop = (np.exp(exp_params[1]) * 
                      np.exp(exp_params[0]*target_ref_day))
    
    train_years_scaled, factors = get_years_growth_factor(deaths, 
                                                          deviating_codes, 
                                                          train_years, 
                                                          target_ref_pop)
    
    differences = pd.DataFrame(index=days_range, columns=subgroups)
    for i, group in enumerate(subgroups):
        train_group_scaled = scale_years(deaths, deviating_codes, train_years,
                                         factors, divide_col=divide_by,
                                         divide_val=group)
        
        train_group_avg = (train_group_scaled.
                           groupby('day_of_year_index').mean()['deaths_sum'])
        train_group_avg = train_group_avg.to_frame()
        
        target_group_pred, train_group_model = (
            poly_fit_365(train_group_avg, train_fit_degree,
                         plot=True, 
                         concept=("Average deaths using training years, for " +
                                  COL_MEANINGS[divide_by]['en'] + ': ' + 
                                  COL_MEANINGS[divide_by]['vals'][group])))
        
        deviations_target_group = (
            deaths[(deaths['anio_ocur'] == target_year) & 
                   (deaths['death_cie10'].isin(deviating_codes)) & 
                   (deaths[divide_by] == group)])
        
        deviations_daily_group, _ = daily_deaths(deviations_target_group)
        
        obs_devs_fit_group, obs_devs_model_group = (
            poly_fit_365(deviations_daily_group, hard_fit_degree,
                         plot=True,
                         concept=("Unknown deaths in " + str(target_year) +
                                  " for " + COL_MEANINGS[divide_by]['en'] + ': ' + 
                                  COL_MEANINGS[divide_by]['vals'][group])))
        
        multiplot_365(
            [target_group_pred, obs_devs_fit_group],
            ('Comparison between predicted and observed behavior in ' +
             str(target_year) + ' for ' + COL_MEANINGS[divide_by]['en'] +
             ': ' + COL_MEANINGS[divide_by]['vals'][group]),
            ['Prediction of unknown diseases', 
             'Smooth behavior of unknown diseases'])
        
        diff = (obs_devs_fit_group['deaths_sum'] -
                target_group_pred['deaths_sum'])
        diff = diff.to_frame()
        diff = diff[diff['deaths_sum'] > 1]
        diff.reindex(days_range, fill_value=0)
        differences[group] = diff['deaths_sum']
    
    total_diffs = differences.sum(axis=1)
    total_diffs = total_diffs.to_frame()
    total_diffs = total_diffs.reindex(days_range, fill_value=0)
    total_diffs.rename(columns={0: 'deaths_sum'}, inplace=True)
    
    findings_target_year = deaths[(deaths['anio_ocur'] == target_year) &
                                  (deaths['death_cie10'].isin(target_disease))]
    
    findings_daily, _ = daily_deaths(findings_target_year)
    observed_findings_fit, observed_findings_model = (
        poly_fit_365(findings_daily, hard_fit_degree, plot=True,
                     concept='Specified deaths in ' + str(target_year)))
    
    train_years_avg = (train_years_scaled.
                       groupby('day_of_year_index').mean()['deaths_sum'])
    train_years_avg = train_years_avg.to_frame()
    
    target_year_pred, _ = (
        poly_fit_365(train_years_avg, train_fit_degree, plot=True,
                     concept='Average deaths using training years'))
    
    deviations_target_year = (
        deaths[(deaths['anio_ocur'] == target_year) &
               (deaths['death_cie10'].isin(deviating_codes))])
    
    deviations_daily, _ = daily_deaths(deviations_target_year)
    
    multiplot_365(
        [findings_daily, total_diffs],
        'Comparison between findings and deviations',
        ['Specified diseases', 
         'Difference between observed and expected unknown diseases'])
    
    validation = target_year_pred['deaths_sum'] + total_diffs['deaths_sum']
    validation = validation.to_frame()
    multiplot_365([target_year_pred, validation, deviations_daily],
                  'Construction of unknown disease records',
                  ['Normal Behavior', 'Total prediction', 'Actual values'])
    
    global_daily_unknown = (
        daily_deaths_global(deaths, DAYS_CUMULATIVES[train_years[0]],
                            DAYS_CUMULATIVES[target_year+2], deviating_codes))
    global_daily_known = (
        daily_deaths_global(deaths, DAYS_CUMULATIVES[train_years[0]],
                            DAYS_CUMULATIVES[target_year+2], target_disease))
    
    global_unknown_adjusted = global_daily_unknown - global_daily_known 
    global_known_adjusted = global_daily_known + global_daily_known
    
    multi_plot_with_format(
        [global_daily_unknown, global_daily_known],
        'Respiratory deaths from 2005 to 2010',
        'Day number', 'Number of deaths', 
        ['Unspecified', 'Specified'])
    multi_plot_with_format(
        [global_unknown_adjusted, global_known_adjusted],
        'Respiratory deaths from 2005 to 2010, adjusted',
        'Day number', 'Number of deaths',
        ['Unspecified adjusted', 'Specified adjusted'])
    

# plot all years

get_difference(deaths,
               'sexo', # ('ent_resid', 'sexo', 'new_age_group')
               [2005, 2006, 2007, 2008], 2009,
               ['J09', 'J10', 'J11', 'J13', 'J14'],
               ['J12', 'J15', 'J16', 'J18'],
               12, 80)
