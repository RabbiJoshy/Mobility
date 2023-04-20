import pandas as pd
import contextily as ctx
import matplotlib.pyplot as plt
import geopandas as gpd
import random
import tarfile
import numpy as np
import os
day = '03-07'

path = os.path.join('Felyx', '2023-' + day + '.tar.xz')
df = pd.DataFrame()
print('opening')
tar = tarfile.open(os.path.join(path), 'r:xz')
members = tar.getmembers()

def sampletimes(members):
    ordered = sorted([member.name for member in members])
    sixties = list(np.arange(1, len(members), 60))
    times = [members[i] for i in sixties]


def CollateFelyxDay(day, save = True):
    path = os.path.join('Felyx', '2023-' + day + '.tar.xz')
    dflist = []
    tar = tarfile.open(os.path.join(path), 'r:xz')
    members = tar.getmembers()
    subset_of_times = random.sample(members, 5)

    for subfilename in subset_of_times:
        print(subfilename.name)
        data = tar.extractfile(subfilename)
        event_df = pd.read_json(data)
        event_df['time'] = pd.to_datetime(subfilename.name[11:21], unit='s')
        dflist.append(event_df)
    df = pd.concat(dflist)
    df = df.drop(['serviceType', 'title', 'vehicleStateId',
                  'reservationState', 'distance', 'address'], axis = 1)

    if save == True:
        os.makedirs(os.path.join('CleanData/Felyx'), exist_ok=True)
        df.to_pickle(os.path.join('CleanData/Felyx', day[:2]+day[3:]))

    return df
df = CollateFelyxDay(day)

len(df['licencePlate'].unique())

def CollateFelyxDays():
    li = []

    for filename in os.listdir(os.path.join('CleanData/Felyx')):
        df = pd.read_csv(os.path.join('CleanData/Felyx', filename))
        li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)

    return df
collate = CollateFelyxDays()

def MakeFelyxGeo(df):
    felyxgeo = gpd.GeoDataFrame(
        df,
        geometry = gpd.points_from_xy(df.lon, df.lat),
        crs='EPSG:4326'
    )
    felyxgeo.geometry.crs = "EPSG:4326"
    felyxgeo.to_crs('EPSG:4326')

    return felyxgeo



# subdf = df.sample(100000)
subdf = collate
# subdf = subdf[subdf['city'] != 'Shenzhen City']
subdf = subdf[subdf['city'] == 'Amsterdam']
# subdf = subdf[subdf['licencePlate'] == 'FKB53G']
plates = df['licencePlate'].unique()
subdf = subdf[subdf['licencePlate'].isin(plates[:1])]

geodf = MakeFelyxGeo(subdf)



fig, ax = plt.subplots()

# berkeley.to_crs('EPSG:3857').plot(ax = ax, figsize=(9, 9), edgecolor="red", facecolor="none")
# ctx.add_basemap(ax)

geodf.plot(ax = ax, markersize='fuelLevel', column = 'licencePlate',
           categorical = True,
           marker = '.',
    legend = False)
           #alpha = felyx['fuelLevel'])#, color = 'licencePlate') cmap='tab5',
# ax.legend(loc='upper center')
ctx.add_basemap(ax, crs='EPSG:4326')
plt.show()

