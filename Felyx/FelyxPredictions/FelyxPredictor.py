import pandas as pd
import geopandas as gpd
import os
from FelyxPredictions.FelyxUtils import MakeFelyxGeo
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
districts =gpd.read_file('AmsterdamGeoJsons/AmsterdamGebieden.json')
df = pd.read_pickle(os.path.join(
    'CleanData', 'Felyx', '2023','03', 'month', 'Amsterdam50'))#.sample
df = df[['carId', 'fuelLevel', 'time', 'lat', 'lon']]
geodf = MakeFelyxGeo(df)
geodf = geodf.sjoin(districts, how="inner", predicate='intersects')
geodf = geodf[['carId', 'fuelLevel', 'time', 'geometry',
       'Gebied', 'Stadsdeel']]
geodf.to_pickle('GeoData/Felyx/Mar23_50')

import pandas as pd
geodf = pd.read_pickle('GeoData/Felyx/Mar23_50')

# geodf['hour'] = geodf['time'].iloc[0].hour
period = '30T'
grouped = geodf.groupby(['Gebied',pd.Grouper(key = 'time', freq= period)]).nunique()['carId'].reset_index()
grouped.to_pickle(os.path.join('GeoData','Felyx','GroupedMar2023','P50' + period))


geo = pd.read_pickle('GeoData/Felyx/Mar23')
sub = geo.sample(30000)
sub['prev_value'] = sub.groupby('carId')['Stadsdeel'].shift()
sub = sub.dropna()

X_train, X_test, y_train, y_test = train_test_split(
    sub[['Stadsdeel', 'lat', 'lon']],
    sub[['prev_value']], test_size=0.33, random_state=42)

le = LabelEncoder()
y_train = le.fit_transform(y_train)
X_train.iloc[:,0] = le.fit_transform(X_train.iloc[:,0])
X_test.iloc[:,0] = le.fit_transform(X_test.iloc[:,0])
y_test = le.fit_transform(y_test)


clf = xgb.XGBClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)


print(accuracy_score(y_test, y_pred))
predictionDF = pd.DataFrame({'test': y_test, 'pred': y_pred})
predictionDF['test'].value_counts()
len(sub[sub['Stadsdeel'] == sub['prev_value']])/len(sub)