import pandas as pd
import numpy as np
import random

# Load the data
preferences = pd.read_excel(r"D:\github\x\dse\Python_Project\preferences.xlsx")
guests = pd.read_excel(r"D:\github\x\dse\Python_Project\guests.xlsx")
hotels = pd.read_excel(r"D:\github\x\dse\Python_Project\hotels.xlsx")

# check data
print(preferences.head())
print(guests.head())
print(hotels.head())
#------------------------------------------------------------------------#
# random assign
# customers are randomly distributed to the rooms until the seats or customers are exhausted;
#------------------------------------------------------------------------#
hotel_rooms_list = []
for _, row in hotels.iterrows():
    hotel_name = row['hotel']
    num_rooms = row['rooms']
    # Create a list of tuples (hotel_name, room_number) for each hotel
    hotel_rooms_list.extend([(hotel_name, i) for i in range(1, num_rooms + 1)])

#watching the result
print(hotel_rooms_list[0:20])

#create new column for assinging hotel to each guests
# fill them with nan
guests['hotel&room'] = np.nan

hotel_rooms_list = random.shuffle(hotel_rooms_list)