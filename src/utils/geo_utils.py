from math import radians, sin, cos, sqrt, atan2

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


from math import radians, sin, cos, sqrt, atan2

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
