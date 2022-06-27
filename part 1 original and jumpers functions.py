# -*- coding: utf-8 -*-
"""
Created on Mon May 30 17:09:11 2022

@author: Braden
"""

import os

import pandas as pd

dir_in = 'C:/Users/Braden/OneDrive/Documents/Codings/machine learning/lihui atg2 atg8/testing week 3 0530/coding'

path_atg8 = os.path.join(dir_in, 'export atg8 0606.csv')
atg8 = pd.read_csv(path_atg8)

dis = 11     #this is the max. distance we choose between frames for recognizing if a puncta is in the same track

df = atg8[['LABEL', 'FRAME', 'POSITION_X', 'POSITION_Y']]
df = df.drop([0,1,2], axis = 0)

"""
FOR OTHER CSV FILES:
    x = 'POSITION_X'
    y = 'POSITION_Y'
    t = 'FRAME'
    FRAME = 'FRAME'
    TRACK_ID = 'LABEL'
    name = 'LABEL'
    
and then you can perform the following: 
    df = pd.DataFrame(columns = [x, y, t, name, TARCK_ID, FRAME, 'puncta', 'LABEL'])
    df[x] = atg2['CENTER_OF_OBJECT_0'] etc... 
    
    FOR POSITION_X, POSITION_Y, POSITION_T, FRAME we need to CONVERT from STRING to INT:
    workflow:
        df[x] = atg2['CENTER_OF_OBJECT_0']
        df[x] = df[x].astype(float).astype(int)
        etc...
    
    you then transforms the column data from the original CSV into a format which is more readable to trackmate
    i.e. track_in , position_t, position_x, etc... 
    trackmate needs: 
        track_id
        position_x
        position_y
        position_t (ideally) or z 
        frame
        
        adding 'puncta' and 'label' is useful for checking the progress while in the python IDE
"""

df['POSITION_Y'] = df['POSITION_Y'].astype(float).astype(int)
df['POSITION_X'] = df['POSITION_X'].astype(float).astype(int)
df['FRAME'] = pd.to_numeric(df['FRAME'], downcast = 'unsigned')

df['puncta']=None

def find_original (data):
    label = data.groupby(by = ['LABEL']) 
    tracked = 1
    for tracks, series in label:
        track = series.sort_values(by = 'FRAME', ascending = True)
        x, y, t = 'POSITION_X', 'POSITION_Y', 'FRAME'
        indice = track.loc[track['FRAME'] == track[t].min()]
        origy = int(track[y][indice.index])
        origx = int(track[x][indice.index])
        x_range = range(origx - dis , origx + dis, 1)
        y_range = range(origy - dis, origy + dis, 1)
        for index, row in track.iterrows():
            if row[x] in x_range and row[y] in y_range:
                data.at[index, 'puncta'] = 'original'
            elif row[x] not in x_range and row[y] not in y_range:
                data.at[index, 'puncta'] = '2 jumps'
            elif row[x] not in x_range or row[y] not in y_range:
                data.at[index,'puncta'] = '1 jump'
            else:
                return 'invalid'
        tracked +=1 
    data['TRACK_ID']=data['LABEL'].str.replace('track-',"")
    data['POSITION_T'] = data['FRAME']
    print(tracked)

find_original(df)

def find_jumpers (data, tracked):
    jumpers = data[data['puncta'] != 'original']
    label = jumpers.groupby(by = ['LABEL']) 
    size = tracked + 10
    for tracks, series in label:
        track = series.sort_values(by = 'FRAME', ascending = True)
        x, y, t = 'POSITION_X', 'POSITION_Y', 'FRAME'
        indice = track.loc[track['FRAME'] == track[t].min()]
        origy = int(track[y][indice.index])
        origx = int(track[x][indice.index])
        x_range = range(origx - dis , origx + dis, 1)
        y_range = range(origy - dis, origy + dis, 1)
        names = tracks
        for index, row in track.iterrows():
            if row[x] in x_range and row[y] in y_range:
                data.at[index, 'puncta'] = f'from {names}';
                data.at[index, 'LABEL'] = f'track-{size}'
            elif row[x] not in x_range and row[y] not in y_range:
                data.at[index, 'puncta'] = 'maybe'
            elif row[x] not in x_range or row[y] not in y_range:
                data.at[index,'puncta'] = 'maybe'
            else:
                return 'invalid'
        df['TRACK_ID']=df['LABEL'].str.replace('track-',"")
        df['POSITION_T'] = df['FRAME']
        size +=1
    if 'maybe' in data['puncta']:
        slackers = data[data['puncta']=='maybe']
        label = slackers.groupby(by = ['LABEL'])
        for tracks, series in label:
            track = series.sort_values(by = 'FRAME', ascending = True)
            x, y, t = 'POSITION_X', 'POSITION_Y', 'FRAME'
            indice = track.loc[track['FRAME'] == track[t].min()]
            origy = int(track[y][indice.index])
            origx = int(track[x][indice.index])
            x_range = range(origx - dis , origx + dis, 1)
            y_range = range(origy - dis, origy + dis, 1)
            names = tracks
            for index, row in track.iterrows():
                if row[x] in x_range and row[y] in y_range:
                    data.at[index, 'puncta'] = f'from {names}_2';
                    data.at[index, 'LABEL'] = f'track-{size}'
                elif row[x] not in x_range and row[y] not in y_range:
                    data.at[index, 'puncta'] = 'maybe'
                elif row[x] not in x_range or row[y] not in y_range:
                    data.at[index,'puncta'] = 'maybe'
                else:
                    return 'invalid' 
for x in df:
    find_jumpers(df, 23)
    if 'maybe' in df['puncta']:
        find_jumpers(df, 23)

#df.to_csv(os.path.join(dir_in,'part 1 atg8 presentation 0613.csv'),index = False)
            
