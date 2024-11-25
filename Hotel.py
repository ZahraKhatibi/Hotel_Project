## Importing Libraries

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

# Load the data
preferences = pd.read_excel(r"D:\github\x\dse\Python_Project\preferences.xlsx")
guests = pd.read_excel(r"D:\github\x\dse\Python_Project\guests.xlsx")
hotels = pd.read_excel(r"D:\github\x\dse\Python_Project\hotels.xlsx")

# check data
print(preferences.head())
print(guests.head())
print(hotels.head())


# This function, assign_random, assigns hotels to guests based on their preferences and hotel room availability randomlly.
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

# The assign_priority function assigns hotels to guests based on their preferences, giving priority to the most preferred hotels while considering room availability.
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

# The assign_availability function assigns hotels to guests based on their preferences and hotel availability, prioritizing hotels with the most available rooms.
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

# The assign_low_price function assigns hotels to guests based on their preferences, prioritizing hotels with the lowest price while considering room availability.
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

#The create_report function generates a report based on guest hotel assignments, satisfaction, and hotel performance metrics.

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
    hotel_counts = guests['hotel_num'].value_counts()
    hotel_counts = hotel_counts.reindex(sorted(hotel_counts.index, key=lambda x: int(x.split('_')[1])), fill_value=0)
    hotel_counts = hotel_counts.reindex([f"hotel_{i}" for i in range(1, 401)], fill_value=0)
    df_h['guest_count'] = hotel_counts.tolist()
    
    # Calculate total income for each hotel

    hotels_income = df_g.groupby('hotel_num')['price_after_discount'].sum()
    hotels_income = hotels_income.reindex(sorted(hotels_income.index, key=lambda x: int(x.split('_')[1])),fill_value=0)
    hotels_income = hotels_income.reindex([f"hotel_{i}" for i in range(1, 401)], fill_value=0)
    df_h['hotel_income'] = hotels_income.tolist()

    
    # Print reports
    number_of_guest_settled_in = df_g['hotel_num'].notnull().sum()
    percentage_of_hotels_are_fully_booked = sum(df_h['rooms'] == df_h['guest_count']) / len(df_h) * 100
    satisfication = df_g['satisfaction'].mean()
    hotel_income = df_h['hotel_income'].sum()
    
    result_list = [number_of_guest_settled_in, percentage_of_hotels_are_fully_booked, satisfication,hotel_income ]
    print("How many guests have settled in?", number_of_guest_settled_in)
    print("What percentage of hotels are fully booked?", percentage_of_hotels_are_fully_booked)
    print("How satisfied are guests with their hotel?", satisfication)
    print("What is the total revenue of the hotels?",  hotel_income)
    
    return df_g, df_h, result_list


# random part
print(assign_random(guests, hotels))
df_guests_assign_random, df_hotels_assign_random , random_result = create_report(guests, hotels)
print(df_guests_assign_random)
print(df_hotels_assign_random)


#priority part
print(assign_priority(guests, hotels))
df_guests_assign_priority, df_hotels_assign_priority , priority_result = create_report(guests, hotels)
print(df_guests_assign_priority)
print(df_hotels_assign_priority)


#low price part
print(assign_low_price(guests, hotels))
df_guests_assign_low_price, df_hotels_assign_low_price , low_price_result = create_report(guests, hotels)
print(df_guests_assign_low_price)
print(df_hotels_assign_low_price)


#availability part
print(assign_availability(guests, hotels))
df_guests_assign_availability, df_hotels_assign_availability , availability_result = create_report(guests, hotels)
print(df_guests_assign_availability)
print(df_hotels_assign_availability)


data = [random_result, priority_result, low_price_result, availability_result]
labels = ['Random', 'Priority', 'Low Price', 'Availability']
titles = ['number of guest settled in', 'percentage of hotels_are fully booked', 'satisfication', 'hotel income']
# Create bar chart
for i in range(4):
    values = [lst[i] for lst in data]
    
    # Create the bar chart
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=['blue', 'green', 'orange', 'red'])
    
    # Add titles and labels
    plt.title(titles[i])
    plt.ylabel('Value')
    plt.xlabel('Result Types')
    
    # Show the plot
    plt.show()