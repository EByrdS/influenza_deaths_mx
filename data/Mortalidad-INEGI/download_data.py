# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 22:42:26 2020

@author: Emmanuel Byrd Suárez
"""

import zipfile
import shutil
import requests
import os
from io import BytesIO
from tqdm import tqdm

dbf_dir = 'dbf'
csv_dir = 'csv'

if not os.path.isdir(dbf_dir):
    os.mkdir(dbf_dir)
    
if not os.path.isdir(csv_dir):
    os.mkdir(csv_dir)

dbf1 = 'https://www.inegi.org.mx/contenidos/programas/mortalidad/microdatos/defunciones/datos/defunciones_generales_base_datos_2005_2009_dbf.zip'
dbf2 = 'https://www.inegi.org.mx/contenidos/programas/mortalidad/microdatos/defunciones/datos/defunciones_generales_base_datos_2010_2014_dbf.zip'

def dbf_name(year_suffix):
    return ('defunciones_base_datos_20' + year_suffix + '_dbf/DEFUN' + 
            year_suffix + '.dbf')

def dbf_dest(year_suffix):
    return os.path.join(dbf_dir, 'DEFUN' + year_suffix + '.dbf')

print("Fetching 2005-2009 as DBF...")
r = requests.get(dbf1, allow_redirects=True)
zipdata = BytesIO(r.content)
with zipfile.ZipFile(zipdata) as z:
    for y in ['05', '06', '07', '08', '09']:
        with z.open(dbf_name(y)) as zf, open(dbf_dest(y), 'wb') as f:
            shutil.copyfileobj(zf, f)
print("Done.")            

print("Fetching 2010-2011 as DBF...")            
r = requests.get(dbf2, allow_redirects=True)
zipdata = BytesIO(r.content)
with zipfile.ZipFile(zipdata) as z:
    for y in ['10', '11']:
        with z.open(dbf_name(y)) as zf, open(dbf_dest(y), 'wb') as f:
            shutil.copyfileobj(zf, f)
print("Done.")

csv_www = [
    'https://www.inegi.org.mx/contenidos/programas/mortalidad/datosabiertos/defunciones/2012/defunciones_base_datos_2012_csv.zip',
    'https://www.inegi.org.mx/contenidos/programas/mortalidad/datosabiertos/defunciones/2013/defunciones_base_datos_2013_csv.zip',
    'https://www.inegi.org.mx/contenidos/programas/mortalidad/datosabiertos/defunciones/2014/defunciones_base_datos_2014_csv.zip',
    'https://www.inegi.org.mx/contenidos/programas/mortalidad/datosabiertos/defunciones/2015/defunciones_base_datos_2015_csv.zip',
    'https://www.inegi.org.mx/contenidos/programas/mortalidad/datosabiertos/defunciones/2016/defunciones_base_datos_2016_csv.zip',
    'https://www.inegi.org.mx/contenidos/programas/mortalidad/datosabiertos/defunciones/2017/conjunto_de_datos_defunciones_generales_2017_csv.zip',
    'https://www.inegi.org.mx/contenidos/programas/mortalidad/datosabiertos/defunciones/2018/conjunto_de_datos_defunciones_registradas_2018_csv.zip'
    ]

csv = [
  'defunciones_generales_2012.csv',
  'defunciones_generales_2013.csv',
  'defunciones_generales_2014.csv',
  'defunciones_generales_2015.csv',
  'defunciones_generales_2016.csv',
  'conjunto_de_datos_defunciones_generales_2017.CSV',
  'conjunto_de_datos_defunciones_registradas_2018.csv']

def csv_name(name):
    return ('conjunto_de_datos/' + name)

def csv_dest(name):
    return os.path.join(csv_dir, name)

print("Fetching csv...")
for i, www in enumerate(tqdm(csv_www)):
    r = requests.get(www, allow_redirects=True)
    zipdata = BytesIO(r.content)
    with zipfile.ZipFile(zipdata) as z:
        with z.open(csv_name(csv[i])) as zf, open(csv_dest(csv[i]), 'wb') as f:
            shutil.copyfileobj(zf, f)
print("Finished downloading.")