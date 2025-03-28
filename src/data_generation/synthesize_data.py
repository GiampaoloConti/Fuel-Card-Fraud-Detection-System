import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from random import choices

# Load fuel station data for reference
fuel_stations_df = pd.read_csv('fuel_stations_italy.csv')

num_vehicles = 20
num_employees = 20
num_cards = 20
num_transactions = 20000  # N transactions to 1 card

central_date = datetime(2024, 11, 1)  # Central date for distribution
date_std_dev = timedelta(hours=10)    # 30-day std deviation for variance

# Helper function to generate datetime within bounds using Gaussian distribution
def generate_dates(num_points, mean_date, std_dev_days):
    dates = [mean_date + timedelta(days=np.random.normal(0, std_dev_days)) for _ in range(num_points)]
    return dates

# Step 1: Create vehicles data
vehicles_data = {
    "vehicle_id": [f"U_{i:03}" for i in range(num_vehicles)],
    "max_capacity": np.random.uniform(30, 50, num_vehicles),
    "fuel_type": np.random.choice(["diesel", "fuel"], num_vehicles),
    "remaining_capacity": np.random.uniform(5, 50, num_vehicles),
    "avg_speed": np.random.uniform(40, 120, num_vehicles),
    "avg_fuel_consumption": np.random.uniform(5, 15, num_vehicles)
}
vehicles_df = pd.DataFrame(vehicles_data)

vehicles_df[['latitude', 'longitude']] = (
    fuel_stations_df[['latitude', 'longitude']]
    .sample(n=num_vehicles, replace=True)
    .reset_index(drop=True)
)
# Add a small random offset to spread the locations
vehicles_df['latitude'] += np.random.uniform(-0.05, 0.05, num_vehicles)
vehicles_df['longitude'] += np.random.uniform(-0.05, 0.05, num_vehicles)

# Step 2: Create employees data
employees_data = {
    "employee_id": [f"U_{i:03}" for i in range(num_employees)],
    "affidability": np.random.uniform(0, 1, num_employees),
    "vehicle_id": np.random.choice(vehicles_df["vehicle_id"], num_employees),
    "card_id": [f"U_{i:03}" for i in range(num_employees)]
}
employees_df = pd.DataFrame(employees_data)

# Step 3: Create cards data
max_amount = np.random.uniform(500, 1500, num_cards)
remaining_amount = np.random.uniform(0, max_amount)
cards_data = {
    "card_id": [f"U_{i:03}" for i in range(num_cards)],
    "max_amount": max_amount,
    "remaining_amount": remaining_amount,
    "employee_id": np.random.choice(employees_df["employee_id"], num_cards)
}
cards_df = pd.DataFrame(cards_data)

# Step 4: Create transactions data
transactions_data = {
    "transaction_id": [f"U_{i:03}" for i in range(num_transactions)],
    "amount": np.random.uniform(10, 60, num_transactions),
    "erogation_type": np.random.choice(["service", "self"], num_transactions),
    "card_id": np.random.choice(cards_df["card_id"], num_transactions),  # N:1 relationship
    "fuel_price": np.random.uniform(1.0, 2.5, num_transactions)
}
transactions_df = pd.DataFrame(transactions_data)

# Generate dates for transactions and card last transactions
transactions_df['time'] = generate_dates(num_transactions, central_date, date_std_dev.days)
cards_df['last_transaction'] = generate_dates(num_cards, central_date, date_std_dev.days)

# Step 5: Assign transaction locations based on vehicle locations
# Merge tables to get vehicle location for each transaction
transactions_df = transactions_df.merge(cards_df[['card_id', 'employee_id']], on='card_id', how='left')
transactions_df = transactions_df.merge(employees_df[['employee_id', 'vehicle_id']], on='employee_id', how='left')

# Rename columns to avoid conflicts in the next merge step
vehicles_df = vehicles_df.rename(columns={'latitude': 'latitude_vehicle', 'longitude': 'longitude_vehicle'})
transactions_df = transactions_df.merge(vehicles_df[['vehicle_id', 'latitude_vehicle', 'longitude_vehicle']], on='vehicle_id', how='left')

# Function to assign transaction location close to vehicle's location or randomly with a small chance
def assign_transaction_location(row, fuel_stations_df, random_chance=0.01):
    if np.random.rand() < random_chance:
        # Randomly select any fuel station in Italy
        selected_location = fuel_stations_df[['latitude', 'longitude']].sample(1).iloc[0]
    else:
        # Select a fuel station near the vehicle's location
        lat, lon = row['latitude_vehicle'], row['longitude_vehicle']
        nearby_stations = fuel_stations_df[
            (fuel_stations_df['latitude'].between(lat - 0.5, lat + 0.5)) &
            (fuel_stations_df['longitude'].between(lon - 0.5, lon + 0.5))
        ]
        
        if not nearby_stations.empty:
            selected_location = nearby_stations[['latitude', 'longitude']].sample(1).iloc[0]
        else:
            # If no nearby station, fallback to a random station
            selected_location = fuel_stations_df[['latitude', 'longitude']].sample(1).iloc[0]
    
    return pd.Series([selected_location['latitude'], selected_location['longitude']])

# Apply the function to each row in transactions_df
transactions_df[['latitude', 'longitude']] = transactions_df.apply(
    assign_transaction_location, axis=1, args=(fuel_stations_df,)
)

# Drop helper columns after assigning locations
transactions_df.drop(columns=['latitude_vehicle', 'longitude_vehicle'], inplace=True)

# Save DataFrames to CSV
vehicles_df.to_csv("vehicles.csv", index=False)
employees_df.to_csv("employees.csv", index=False)
cards_df.to_csv("cards.csv", index=False)
transactions_df.to_csv("transactions.csv", index=False)

print("Synthetic data with Italy-constrained locations and datetime elements generated and saved to CSV files.")



from sdv.multi_table import HMASynthesizer
from sdv.metadata import Metadata

metadata = Metadata.load_from_json('metadata.json')


# Initialize synthesizer with metadata
my_synthesizer = HMASynthesizer(metadata)

# Consolidate all constraints in a list
constraints = [
    {
        'constraint_class': 'ScalarRange',
        'table_name': 'transactions',
        'constraint_parameters': {
            'column_name': 'latitude',
            'low_value': 36.71703,
            'high_value': 46.99623,
            'strict_boundaries': False
        }
    },
    {
        'constraint_class': 'ScalarRange',
        'table_name': 'transactions',
        'constraint_parameters': {
            'column_name': 'longitude',
            'low_value': 0,
            'high_value': 18.37819,
            'strict_boundaries': False
        }
    },
    {
    'constraint_class': 'Inequality',
    'table_name': 'cards', # for multi table synthesizers
    'constraint_parameters': {
        'low_column_name': 'remaining_amount',
        'high_column_name': 'max_amount',
        'strict_boundaries': True
    }
}
]
# Prepare the data for the synthesizer
data = {
    'vehicles': vehicles_df,
    'employees': employees_df,
    'cards': cards_df,
    'transactions': transactions_df
}

# Add all constraints at once
my_synthesizer.add_constraints(constraints=constraints)

# Fit and sample the data
my_synthesizer.fit(data)
synthetic_data = my_synthesizer.sample(scale=1)

# Save each table to a CSV file if data is available
if synthetic_data:
    for table_name, table_data in synthetic_data.items():
        file_name = f"{table_name}_synthetic.csv"
        table_data.to_csv(file_name, index=False)
        print(f"Saved {table_name} as {file_name}")
else:
    print("No synthetic data generated.")
