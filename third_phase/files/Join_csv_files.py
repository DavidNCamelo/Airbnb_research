''' 
Created By David Camelo on 11/02/2024
'''
#Import Required Libraries
import pandas as pd
import os
import csv

#There is some file enconding on Latin-1 is necessary to read in this and change its enconding to utf-8
def opening_csv(files, encode = 'latin-1'):
    with open(files, 'r', encoding = encode) as file:
        room = pd.read_csv(file)
    return room

#Read the Latin-1 encoded files
rooms4 = opening_csv('exnulls_data_rooms.csv')

#read the utf-8 encoded file
rooms1 = pd.read_csv('data_rooms - data_rooms.csv', dtype={'id': str})
rooms1['id'] = pd.to_numeric(rooms1['id'], errors='coerce', downcast='integer')
rooms3 = pd.read_csv('data_rooms_duban - data_rooms.csv')
rooms2 =pd.read_csv('corrected_data_rooms.csv')

#Drop extra columns generated during the previous transformation but don't exist already
rooms3 = rooms3.drop(['Unnamed: 14', 'Unnamed: 15'], axis = 1)

#Concat files to work with only one dataframe
entire_rooms = pd.concat([rooms1, rooms2, rooms3, rooms4], ignore_index = True)

#Drop duplicated ids if necessary
entire_rooms = entire_rooms.drop_duplicates(subset = ['id'])

#print(rooms1.head())
rooms4.info()
entire_rooms.info()

#Save the final file on the main folder where are currently located
location = os.path.join(os.path.pardir, 'all_data_rooms.csv')
entire_rooms.to_csv(location, index=False)