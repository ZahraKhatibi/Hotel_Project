# Hotel Project

![](images/pic.png)

This project focuses on assigning guests to hotel rooms based on different strategies and generating reports on guest satisfaction, hotel income, and other key metrics. The goal is to create a system that can simulate guest assignments to hotels and analyze the results based on various strategies.

## Table of Contents

- [Project Overview](#project-overview)
- [Functions](#functions)
  - [assign_random](#assign_random)
  - [assign_priority](#assign_priority)
  - [assign_availability](#assign_availability)
  - [assign_low_price](#assign_low_price)
  - [create_report](#create_report)
- [Results](#results)

## Project Overview

This project loads data from three Excel files:

- **preferences.xlsx**: Contains guest preferences regarding hotels.
- **guests.xlsx**: Contains guest data.
- **hotels.xlsx**: Contains hotel data, including room availability and pricing.

The project then implements four different guest assignment strategies:
1. **Random Assignment**: Guests are assigned to rooms randomly until all rooms or guests are exhausted.
2. **Priority Assignment**: Guests are assigned to their preferred hotels based on their priority list.
3. **Availability-based Assignment**: Guests are assigned to the most available hotels first.
4. **Low-price Assignment**: Guests are assigned to hotels with the lowest prices first.

After assignment, a report is generated containing statistics such as the number of guests settled in, hotel booking rates, guest satisfaction, and total hotel income.

## Functions

### `assign_random(df_g, df_h)`

This function randomly assigns guests to hotel rooms based on their preferences until rooms or guests are exhausted.

- **Input**: `df_g` (guests DataFrame), `df_h` (hotels DataFrame)
- **Output**: Modified `df_g` with hotel assignments.

### `assign_priority(df_g, df_h)`

This function assigns guests to their preferred hotels based on their priority list, ensuring that guests are assigned to available rooms.

- **Input**: `df_g` (guests DataFrame), `df_h` (hotels DataFrame)
- **Output**: Modified `df_g` with hotel assignments.

### `assign_availability(df_g, df_h)`

This function assigns guests to hotels based on room availability, starting with the hotel with the most rooms available.

- **Input**: `df_g` (guests DataFrame), `df_h` (hotels DataFrame)
- **Output**: Modified `df_g` with hotel assignments.

### `assign_low_price(df_g, df_h)`

This function assigns guests to hotels based on the lowest price available for rooms, prioritizing cheaper options.

- **Input**: `df_g` (guests DataFrame), `df_h` (hotels DataFrame)
- **Output**: Modified `df_g` with hotel assignments.

### `create_report(df_g, df_h)`

This function generates a report on guest satisfaction, hotel occupancy, and revenue after guest assignments. The report includes:

- Number of guests settled in.
- Percentage of hotels fully booked.
- Average guest satisfaction.
- Total hotel income.

- **Input**: `df_g` (guests DataFrame), `df_h` (hotels DataFrame)
- **Output**: Modified `df_g` and `df_h` with additional metrics, along with a result list containing key statistics.

# Results

The following charts compare the results of four hotel guest assignment strategies: **Random**, **Priority**, **Low Price**, and **Availability**. The metrics assessed are the number of guests settled in, percentage of hotels fully booked, guest satisfaction, and hotel income.

## Conclusion
- **Priority** assignment leads to the highest satisfaction and revenue, but it doesn't fully maximize hotel occupancy.
- **Low Price** results in the highest percentage of fully booked hotels but with lower guest satisfaction and reduced income.
- **Random** assignment results in a balanced outcome, though with lower satisfaction.
- **Availability** maximizes room allocation based on availability but results in lower income and satisfaction.

