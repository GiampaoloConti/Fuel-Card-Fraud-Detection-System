import json

metadata = {
    "tables": {
        "vehicles": {
            "primary_key": "vehicle_id",
            "columns": { 
                "vehicle_id": {
                    "sdtype": "id",
                    "regex_format": "U_[0-9]{9}"
                },
                "max_capacity": {
                    "sdtype": "numerical"
                },
                "fuel_type": {
                    "sdtype": "categorical"
                },
                "remaining_capacity": {
                    "sdtype": "numerical"
                },
                "latitude_vehicle": {
                    "sdtype": "numerical"
                },
                "longitude_vehicle": {
                    "sdtype": "numerical"
                },
                "avg_speed": {
                    "sdtype": "numerical"
                },
                "avg_fuel_consumption": {
                    "sdtype": "numerical"
                }
            }
        },
        "employees": {
            "primary_key": "employee_id",
            "columns": {
                "employee_id": {
                    "sdtype": "id",
                    "regex_format": "U_[0-9]{9}"
                }, 
                "affidability": {
                    "sdtype": "numerical"
                },
                "vehicle_id": {
                    "sdtype": "id",
                    "regex_format": "U_[0-9]{9}"
                },
                "card_id": {
                    "sdtype": "id",
                    "regex_format": "U_[0-9]{9}"
                }
            }
        },
        "cards": {
            "primary_key": "card_id",
            "columns": {
                "card_id": {
                    "sdtype": "id",
                    "regex_format": "U_[0-9]{9}"
                }, 
                "max_amount": {
                    "sdtype": "numerical"
                },
                "remaining_amount": {
                    "sdtype": "numerical"
                },
                "employee_id": {
                    "sdtype": "id",
                    "regex_format": "U_[0-9]{9}"
                },
                "last_transaction": {
                    "sdtype": "datetime",
                    #"format": "%Y-%m-%d"
                }
            }
        },
        "transactions": {
            "primary_key": "transaction_id",
            "columns": {
                "transaction_id": {
                    "sdtype": "id",
                    "regex_format": "U_[0-9]{9}"
                }, 
                "latitude": {
                    "sdtype": "numerical"
                },
                "longitude": {
                    "sdtype": "numerical"
                },
                "amount": {
                    "sdtype": "numerical"
                },
                "erogation_type": {
                    "sdtype": "categorical"
                },
                "card_id": {
                    "sdtype": "id",
                    "regex_format": "U_[0-9]{9}",
                },
                "employee_id": {
                    "sdtype": "id",
                    "regex_format": "U_[0-9]{9}",
                }, 
                "vehicle_id": {
                    "sdtype": "id",
                    "regex_format": "U_[0-9]{9}",
                },  
                
                "fuel_price": {
                    "sdtype": "numerical"
                },
                "time": {
                    "sdtype": "datetime",
                    #"format": "%Y-%m-%d"
                }
            }
        }
    },
    
    "relationships": [{
        "parent_table_name": "cards",
        "parent_primary_key": "card_id",
        "child_table_name": "transactions",
        "child_foreign_key": "card_id"
    }]
        
}


with open('metadata.json', 'w') as f:
    json.dump(metadata, f, indent=4)

print("Metadata with foreign keys and categorical values has been written to metadata_with_foreign_keys_and_categorical_values.json")


from sdv.metadata import Metadata

# Load the metadata JSON file
metadata = Metadata.load_from_json('metadata.json')

# Print or inspect the metadata
print(metadata)
