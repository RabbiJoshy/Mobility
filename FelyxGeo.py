import pandas as pd
import contextily as ctx
import matplotlib.pyplot as plt
import geopandas as gpd
import random
import numpy as np
import os
import FelyxPredictions.FelyxUtils

# directory = 'L:\\UserData\\Joshua'#\\2023\\03\\2023-03-07.tar.xz'
# file = os.path.join(directory, '2023', '03', 'Amsterdam')
os.makedirs(os.path.join('CleanData', 'Felyx', '2023','03', 'month'), exist_ok= True)
df = pd.read_pickle(os.path.join('CleanData', 'Felyx', '2023','03', 'month', 'Amsterdam25'))

view = df[df['carId'] == df['carId'].unique()[0]]


def MakeFelyxGeo(df):
    felyxgeo = gpd.GeoDataFrame(
        df,
        geometry = gpd.points_from_xy(df.lon, df.lat),
        crs='EPSG:4326'
    )
    felyxgeo.geometry.crs = "EPSG:4326"
    felyxgeo.to_crs('EPSG:4326')

    return felyxgeo

df = df.set_index('time')
# resampled = df['lon'].resample('30T').mean()

geodf = MakeFelyxGeo(df)

plates = geodf['licencePlate'].unique()
print(len(plates))
geodf = geodf[geodf['licencePlate'] == plates[0]]

def nthtimes(df, timeres ='1T'):
    grouped = df.groupby(pd.Grouper(freq=timeres)).nth(0)
    return grouped

os.makedirs(os.path.join('Felyx Animations', 'data', timeres), exist_ok = True)
grouped.to_pickle(os.path.join('Felyx Animations', 'data', timeres, plates[0]))

# districts =gpd.read_file('amsregions.json')

# for i in range(len(grouped[:9])):
#     print(i)
#     subdf = grouped.iloc[i:i+1, :]
#     fig, ax = plt.subplots()
#     subdf.iloc[0:1, :].plot(ax = ax, markersize='fuelLevel', column = 'licencePlate',
#                categorical = True,
#                marker = '.',
#         legend = False)
#                #alpha = felyx['fuelLevel'])#, color = 'licencePlate') cmap='tab5', ax.legend(loc='upper center')
#     districts.plot(ax = ax, facecolor="none",
#                   edgecolor='black', lw=0.7)
#     # ctx.add_basemap(ax, crs='EPSG:4326')
#     plt.show()




