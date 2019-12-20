import os
import numpy as np
import pandas as pd

fn = r"D:\TwitterData\Gazetteer_ASCII"
os.chdir(fn)

names = ['Record ID', 'Authority ID', 'State ID', 'Variant Name', 'Name', 
         'Feature Code', 'Status', 'Postcode', 'Concise Gazetteer', 
         'Longitude', 'Lon_D', 'Lon_M', 'Lon_S', 'Latitude', 'Lat_D', 
         'Lat_M', 'Lat_S', '100K Map', 'CGDN', 'Record ID2']

# add columns
df = pd.read_csv('Gazetteer2010_txt.csv', names=names)

# get all results with name of Kingsford
df[df['Name'] == 'Kingsford']

# get the suburb with name of Kingford
df[(df['Name'] == 'Kingsford')&(df['Feature Code'] == 'SUB')]

# db based on gazetteer
def search_suburbs(name, db):
    result = db[(db['Name'] == name)&(db['Feature Code'] == 'SUB')]
    return result
