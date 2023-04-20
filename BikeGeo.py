import pandas as pd
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
#CKL bikes don't move on 0307
#NS says nothing
#Donkey and GoAbout don't move

def create_geo_df_day(day = '0307', operator = 'GoAbout', save = False):
    path = os.path.join('CleanData', operator, day, 'Day', day)
    df = pd.read_csv(path)

    GeoDF = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.lon, df.lat),
        crs='EPSG:4326'
    )
    GeoDF.geometry.crs = "EPSG:4326"
    GeoDF.to_crs('EPSG:4326')

    if save == True:
        os.makedirs(os.path.join('CleanData', operator, day, 'Geo'), exist_ok=True)
        GeoDF.to_csv(os.path.join('CleanData', operator, day, 'Geo', day + '_GEO'))

    return GeoDF

GeoDF = create_geo_df_day(operator = 'Donkey')



subgeo = GeoDF.sample(10000)
column = 'bike_id'
# subgeo = subgeo.reset_index()
# subgeo = subgeo[['geometry', 'num_bikes_available']]
subgeo = subgeo[subgeo.lat.between (51,52)]
# subgeo = subgeo[subgeo.lon.between (5.6,5.7)]
ten = subgeo.bike_id.unique()[:10]
subgeo = subgeo[subgeo.bike_id.isin(ten)]

fig, ax = plt.subplots()
subgeo.plot(ax = ax, column = column,
           categorical = True, cmap='tab10',
           marker = '.', markersize = 1000,
            legend = True)

ctx.add_basemap(ax, crs='epsg:4326', source=ctx.providers.Stamen.TonerLite)
# ctx.add_basemap(ax, crs='EPSG:4326')
plt.show()