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
guests['satisfaction'] = np.nan

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
                df_g.at[index, 'satisfaction'] = round(100-(guest_priority_dict[row['guest']].index(guests['hotel_num'][index])+1)/(len(guest_priority_dict[row['guest']]))*100,2)
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

print("What percentage of hotels are fully booked? ",sum(hotels['rooms']==hotels['guest_count'])/len(hotels)*100)

#How much revenue does each hotel generate?
hotels_income = guests.groupby('hotel_num')['price_after_discount'].sum()
hotels_income = hotels_income.reindex(sorted(hotels_income.index, key=lambda x: int(x.split('_')[1])))
hotels['hotel_income'] = list(hotels_income)

print(hotels)


def assign_priority(df_g ,df_h ,priority, capacity):
    
    for index , row in df_g.iterrows():
        
        for hlt in priority[row['guest']]:

            if capacity[hlt][0]>=1:
                capacity[hlt][0] -= 1
                df_g.at[index, 'hotel_num'] = hlt
                df_g.at[index, 'price_after_discount'] = df_h['price'][int(hlt[6::])-1] - df_g['discount'][index]
                df_g.at[index, 'satisfaction'] = round(100-(priority[row['guest']].index(guests['hotel_num'][index]))/(len(priority[row['guest']]))*100,2)
                break
            else:
                pass
        if type(df_g['hotel_num'][index]) != str:
            df_g.at[index, 'satisfaction'] = 0.00
            
    return df_g


guests_hotel = assign_priority(guests,hotels,guest_priority_dict,hotel_capacity)
print(guests_hotel)


# availability
max_capacity = list(hotels.sort_values(by='rooms', ascending=[False])['hotel'])

def assign_availability(df_g ,df_h ,priority, capacity):
    
    for index , row in df_g.iterrows():     
        for hlt in max_capacity:
            if hlt in priority[row['guest']]:
                if capacity[hlt][0]>=1:
                    capacity[hlt][0] -= 1
                    df_g.at[index, 'hotel_num'] = hlt
                    df_g.at[index, 'price_after_discount'] = df_h['price'][int(hlt[6::])-1] - df_g['discount'][index]
                    df_g.at[index, 'satisfaction'] = round(100-(priority[row['guest']].index(guests['hotel_num'][index]))/(len(priority[row['guest']]))*100,2)
                    break
                else:
                    pass
            else: 
                pass
        if type(df_g['hotel_num'][index]) != str:
            df_g.at[index, 'satisfaction'] = 0.00
            
    return df_g

guests_hotel = assign_availability(guests,hotels,guest_priority_dict,hotel_capacity)
print(guests_hotel)

# assign with using price of each hotel

min_price = list(hotels.sort_values(by='price', ascending=[False])['hotel'])

def assign_low_price(df_g ,df_h ,priority, capacity):
    
    for index , row in df_g.iterrows():     
        for hlt in min_price:
            if hlt in priority[row['guest']]:
                if capacity[hlt][0]>=1:
                    capacity[hlt][0] -= 1
                    df_g.at[index, 'hotel_num'] = hlt
                    df_g.at[index, 'price_after_discount'] = df_h['price'][int(hlt[6::])-1] - df_g['discount'][index]
                    df_g.at[index, 'satisfaction'] = round(100-(priority[row['guest']].index(guests['hotel_num'][index]))/(len(priority[row['guest']]))*100,2)
                    break
                else:
                    pass
            else: 
                pass
        if type(df_g['hotel_num'][index]) != str:
            df_g.at[index, 'satisfaction'] = 0.00
            
    return df_g


#example
guests_hotel = assign_low_price(guests,hotels,guest_priority_dict,hotel_capacity)
print(guests_hotel)