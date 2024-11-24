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
guests['price_after_discount'] = np.nan

#define guests priority dictionary 
guest_priority_dict = preferences.groupby('guest')['hotel'].apply(list).to_dict()

#show example
print(guest_priority_dict['guest_1'])

#define hotels capacity list
hotel_capacity = hotels.groupby('hotel')['rooms'].apply(list)

#example
print(hotel_capacity['hotel_2'])

#define a function to assigning hotels randomly based on their priority
def assign_random(df_g ,df_h ,priority, capacity):
    
    for index , row in df_g.iterrows(): 
        while(len(priority[row['guest']])>0 or row['hotel_num'] == np.nan):

            random_room = random.choice(priority[row['guest']])

            if capacity[random_room][0]>=1:
                capacity[random_room][0] -= 1
                df_g.at[index, 'hotel_num'] = random_room
                df_g.at[index, 'price_after_discount'] = df_h['price'][int(random_room[6::])-1] - df_g['discount'][index]
                break
            else:
                priority[row['guest']].remove(random_room)
    return df_g

guests_hotel = assign_random(guests,hotels,guest_priority_dict,hotel_capacity)
print(guests_hotel)

# report

print("the number of customers accommodated: ", sum(guests_hotel['hotel_num']!= np.nan))


# How many rooms of each hotels are full?
hotel_counts = guests_hotel['hotel_num'].value_counts()
hotel_counts = hotel_counts.reindex(sorted(hotel_counts.index, key=lambda x: int(x.split('_')[1])))
hotels['guest_count'] = list(hotel_counts)

