import pandas as pd
import contextily as ctx
import matplotlib.pyplot as plt
import geopandas as gpd
import random
import numpy as np
import os

# directory = 'L:\\UserData\\Joshua'#\\2023\\03\\2023-03-07.tar.xz'
# file = os.path.join(directory, '2023', '03', 'Amsterdam')
df = pd.read_pickle('CleanData\\Felyx\\2023\\03\\month\\Amsterdamplates')

def MakeFelyxGeo(df):
    felyxgeo = gpd.GeoDataFrame(
        df,
        geometry = gpd.points_from_xy(df.lon, df.lat),
        crs='EPSG:4326'
    )
    felyxgeo.geometry.crs = "EPSG:4326"
    felyxgeo.to_crs('EPSG:4326')

    return felyxgeo
geodf = MakeFelyxGeo(df)

plates = geodf['licencePlate'].unique()
print(len(plates))
geodf = geodf[geodf['licencePlate'] == plates[0]]


fig, ax = plt.subplots()
geodf.plot(ax = ax, markersize='fuelLevel', column = 'licencePlate',
           categorical = True,
           marker = '.',
    legend = False)
           #alpha = felyx['fuelLevel'])#, color = 'licencePlate') cmap='tab5',
# ax.legend(loc='upper center')
ctx.add_basemap(ax, crs='EPSG:4326')
plt.show()

