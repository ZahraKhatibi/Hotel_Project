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

def create_report(df_g, df_h):
    # Ensure `preferences` is defined or passed to the function if used
    priority = preferences.groupby('guest')['hotel'].apply(list).to_dict()
    capacity = df_h.groupby('hotel')['rooms'].apply(list)
    
    # Initialize new columns
    df_g['price_after_discount'] = np.nan
    df_g['satisfaction'] = np.nan
    
    for index, row in df_g.iterrows():
        if not isinstance(df_g.loc[index, 'hotel_num'], str):
            df_g.at[index, 'satisfaction'] = 0.00
        else:
            room_number = int(df_g.loc[index, 'hotel_num'][6:]) - 1
            df_g.at[index, 'price_after_discount'] = (
                df_h.loc[room_number, 'price'] - df_g.loc[index, 'discount']
            )
            df_g.at[index, 'satisfaction'] = round(
                100 - ((priority[row['guest']].index(df_g.loc[index, 'hotel_num'])) / 
                       len(priority[row['guest']]) * 100), 2
            )

    # Count guests for each hotel

    
    hotel_counts = df_g['hotel_num'].value_counts()
    hotel_counts = hotel_counts.reindex(sorted(hotel_counts.index, key=lambda x: int(x.split('_')[1])), fill_value=0)
    df_h['guest_count'] = hotel_counts.tolist()
    # Calculate total income for each hotel

    hotels_income = df_g.groupby('hotel_num')['price_after_discount'].sum()
    hotels_income = hotels_income.reindex(sorted(hotels_income.index, key=lambda x: int(x.split('_')[1])),fill_value=0)
    df_h['hotel_income'] = hotels_income.tolist()

    
    # Print reports
    print("How many guests have settled in?", (df_g['hotel_num'].notnull().sum()))
    print("What percentage of hotels are fully booked?", 
          ( sum(df_h['rooms'] == df_h['guest_count']) / len(df_h) * 100), "%")
    print("How satisfied are guests with their hotel?", df_g['satisfaction'].mean())
    
    return df_g
