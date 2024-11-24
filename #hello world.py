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

#at frist, assign nan to all guest for their hotel number
guests['hotel_num'] = np.nan

#define guests priority dictionary 
guest_priority_dict = preferences.groupby('guest')['hotel'].apply(list).to_dict()

#show example
print(guest_priority_dict['guest_1'])

#define hotels capacity list
hotel_capacity = hotels.groupby('hotel')['rooms'].apply(list)

#example
print(hotel_capacity['hotel_2'])