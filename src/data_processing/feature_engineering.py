from math import radians, sin, cos, sqrt, atan2
import pandas as pd
import numpy as np

transactions_df = pd.read_csv('data/raw/transactions.csv')
cards_df = pd.read_csv('data/raw/cards.csv')
employees_df = pd.read_csv('data/raw/employees.csv')
vehicles_df = pd.read_csv('data/raw/vehicles.csv')

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def calculate_fuel_bought(transaction, vehicle):
    discount, surcharge = 0,0
    
    amount_spent = transaction['amount']
    fuel_price = transaction['fuel_price']
    erogation_type = transaction['erogation_type']

    fuel_bought = amount_spent / fuel_price

    if erogation_type == 'self':
        discount = -0.02
    elif erogation_type == 'service':
        surcharge = 0.03
        
    fuel_bought /= (1 + surcharge + discount)

    return fuel_bought # liters

def calculate_fuel_consumed(distance_taken, avg_fuel_consumption):
 
    fuel_consumed = distance_taken * avg_fuel_consumption
    
    return fuel_consumed


processed_matrix = []

for index, transaction in transactions_df.iterrows():
    card = cards_df[cards_df['card_id'] == transaction['card_id']]
    if not card.empty:
        card_id = card['card_id'].iloc[0]
        
        employee = employees_df[employees_df['card_id'] == card_id]
        if not employee.empty:
            employee = employee.iloc[0] 
            
            vehicle = vehicles_df[vehicles_df['vehicle_id'] == employee['vehicle_id']]
            if not vehicle.empty:
                vehicle = vehicle.iloc[0]
                
                distance_taken = haversine(vehicle.latitude_vehicle, vehicle.longitude_vehicle, transaction.latitude, transaction.longitude) # Km
                trans_amount = transaction.amount
                max_card_amount = card.max_amount.iloc[0] 
                remaining_amount = card.remaining_amount.iloc[0] 
                fuel_bought = calculate_fuel_bought(transaction, vehicle)
                fuel_consumed = calculate_fuel_consumed(distance_taken, vehicle.avg_fuel_consumption)
                empl_affidability = employee.affidability
                delta_time = pd.to_datetime(transaction.time) - pd.to_datetime(card.last_transaction.iloc[0] )
                vehicle_capacity = vehicle.max_capacity
                processed_data = {
   
                    'distance_taken' : distance_taken,
                    'trans_amount' : trans_amount,
                    'max_card_amount' : max_card_amount,
                    'remaining_amount': remaining_amount,
                    'fuel_bought': fuel_bought,
                    'empl_affidability': empl_affidability,
                    'vehicle_max_capacity': vehicle_capacity,
                    'fuel_consumed' : fuel_consumed,
                    'delta_time':  delta_time

                }
                
                processed_matrix.append(processed_data)
                
                
processed_df = pd.DataFrame(processed_matrix)

processed_df = processed_df[processed_df['delta_time'] >= pd.Timedelta(0)]

for index, element in processed_df.iterrows():
    if ((float(element['trans_amount']) > float(element['remaining_amount']))
        or (element['delta_time'] < pd.Timedelta(0))
        or (float(element['fuel_bought']) > float(element['vehicle_max_capacity']))):
        
        processed_df.at[index, 'label'] = 1
    else: 
        processed_df.at[index, 'label'] = 0

        
processed_df.to_csv('processed_transactions.csv', index=False)

print("Data saved to processed_transactions.csv")

i = 0
for index, element in processed_df.iterrows():
    if ((float(element['empl_affidability']) <= 0.1)
        and (element['delta_time'] < pd.Timedelta(days=1))):
        i += 1
        processed_df.at[index, 'label'] = 1
        
processed_df.to_csv('processed_transactions.csv', index=False)

print(i)

data = processed_df

random_fraud_percentage = 0.1  # e.g., 5% of data as random fraud
num_random_frauds = int(len(data) * random_fraud_percentage)

random_fraud_indices = np.random.choice(data.index, size=num_random_frauds, replace=False)

data.loc[random_fraud_indices, 'label'] = 1

data.to_csv('processed_transactions_with_random_frauds.csv', index=False)

print(f"Assigned random fraud labels to {num_random_frauds} rows.")
