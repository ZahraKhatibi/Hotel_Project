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

def assign_random(df_g ,df_h):
    
    priority = preferences.groupby('guest')['hotel'].apply(list).to_dict()
    capacity = df_h.groupby('hotel')['rooms'].apply(list)
    
    df_g['hotel_num'] = np.nan
    for index , row in df_g.iterrows(): 
        while(len(priority[row['guest']])>0 or row['hotel_num'] == np.nan):
            random_room = random.choice(priority[row['guest']])
            if capacity[random_room][0]>=1:
                df_g.at[index, 'hotel_num'] = random_room
                capacity[random_room][0] -= 1
                break
            else:
                priority[row['guest']].remove(random_room)
    return df_g

def assign_priority(df_g ,df_h):
    
    priority = preferences.groupby('guest')['hotel'].apply(list).to_dict()
    capacity = df_h.groupby('hotel')['rooms'].apply(list)
    
    df_g['hotel_num'] = np.nan
    df_g.drop(columns=['satisfaction', 'price_after_discount'], inplace=True)

    for index , row in df_g.iterrows():       
        for hlt in priority[row['guest']]:
            if capacity[hlt][0]>=1:
                capacity[hlt][0] -= 1
                df_g.at[index, 'hotel_num'] = hlt
                break        
    return df_g

def assign_availability(df_g ,df_h):
    priority = preferences.groupby('guest')['hotel'].apply(list).to_dict()
    capacity = df_h.groupby('hotel')['rooms'].apply(list)
    max_capacity = list(df_h.sort_values(by='rooms', ascending=[False])['hotel'])
    df_g['hotel_num'] = np.nan
    df_g.drop(columns=['satisfaction', 'price_after_discount'], inplace=True)
    for index , row in df_g.iterrows():     
        for hlt in max_capacity:
            if hlt in priority[row['guest']]:
                if capacity[hlt][0]>=1:
                    capacity[hlt][0] -= 1
                    df_g.at[index, 'hotel_num'] = hlt
                    break      
    return df_g

def assign_low_price(df_g ,df_h):    
    priority = preferences.groupby('guest')['hotel'].apply(list).to_dict()
    capacity = df_h.groupby('hotel')['rooms'].apply(list)
    min_price = list(df_h.sort_values(by='price', ascending=[False])['hotel'])
    df_g['hotel_num'] = np.nan
    df_g.drop(columns=['satisfaction', 'price_after_discount'], inplace=True)
    for index , row in df_g.iterrows():     
        for hlt in min_price:
            if hlt in priority[row['guest']]:
                if capacity[hlt][0]>=1:
                    capacity[hlt][0] -= 1
                    df_g.at[index, 'hotel_num'] = hlt
                    break          
    return df_g

