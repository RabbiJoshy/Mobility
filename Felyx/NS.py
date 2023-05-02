import pandas as pd
import json
import tarfile
import os
day = '0307'

def fixjsonNS(file, addition = '', replace_gen = True, replace_het = True, replace_quotes = True):

    txt = file.read()
    txt = txt.decode("utf-8")
    # if replace_het == True:
    txt = txt.replace('\"\'s-', '\"ss-')
    # txt = txt.replace('\'s-', 'ss-')
    txt = txt.replace("\'t ", "het ")
    txt = txt.replace(u'\\xa0', u' ')
    txt = txt.replace("True", "true")
    txt = txt.replace("\'", "\"")


    return txt


def NS(path):
    df = pd.DataFrame()
    for filename in os.listdir(path):
        if filename.startswith('ns'):
            filenameinfo = filename.replace(".tar.gz", "")
            timestamp = filenameinfo[-12:]

            tar = tarfile.open(os.path.join(path, filename), 'r:gz')
            members = tar.getmembers()
            for subfilename in members:
                print(subfilename)
                if subfilename.name == 'station_status':
                    cleanjson = fixjsonNS(tar.extractfile(subfilename))
                    jsondict = json.loads(cleanjson)
                    data = jsondict['data']['stations']
                    subdf = pd.DataFrame.from_dict(data, orient='columns')

                    time = pd.Timestamp(year=int(timestamp[:4]), month=int(timestamp[4:6]), day=int(timestamp[6:8]), hour=int(timestamp[8:10]), minute= int(timestamp[10:12]))
                    subdf['city'] = filenameinfo[7:-23]
                    subdf['time'] = time
                    # print(subdf)
                    # df = pd.concat([subdf, df])

                elif subfilename.name == 'station_information':
                    cleanjson = fixjsonNS(tar.extractfile(subfilename))
                    jsondict = json.loads(cleanjson)
                    infodata = jsondict['data']['stations']
                    infosubdf = pd.DataFrame.from_dict(infodata, orient='columns')
                    # timestamp = filenameinfo[-12:]
                    # infosubdf['time'] = timestamp

            combined = pd.merge(subdf, infosubdf, on='station_id')
            df = pd.concat([combined, df])

    # GeoDF = make_geo(df)
    # Geo_DF = gpd.GeoDataFrame(GeoDF, geometry='geometry')
    #
    os.makedirs('CleanData/NS/0307', exist_ok=True)
    df.to_pickle(os.path.join('CleanData/NS/0307', path[-2:]))

    return df
NSTest = NS(os.path.join('NS310304'))