import pandas as pd
import numpy as np

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
