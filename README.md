
# Fuel Card Fraud Detection

This project simulates and detects fuel card fraud using synthetic data for transactions, vehicles, employees, and cards. It includes steps for data generation, feature engineering, and fraud filtering. Part of the FuelWise project for B future Challenge Emilia Romagna 1st edition 2024/25

## Project Structure

```
fuel_card_fraud/
├── data/
│   ├── raw/                # Raw synthetic input data
│   └── processed/          # Data after feature engineering
├── src/
│   ├── data_generation/    # Scripts for creating synthetic datasets
│   ├── data_processing/    # Scripts to clean and process data
 |      |------- ml/ # Scripts with the NN and RF models
│   └── utils/              # Helper functions (e.g., geolocation)
 |----- metadata.json # Metadata of datasets for synthetic generation
└── README.md
```

## Key Components

- **Data Generation**: Uses SDV to synthesize hierarchical data and fetch fuel station locations. Datasets are created using both SDV and distribution sampling.
- **Feature Engineering**: Calculates distance traveled, fuel usage, and time intervals, filter outliers and applies heuristic rules to label or filter suspicious transactions.

## How to Use

1. Run `src/data_generation/*.py` to generate synthetic data (or use directly the data present in the folder 'data')
2. Use `src/data_processing/*.py` to process and feature engineer (change the path of the datasets if new datasets were created).
3. Run 'src/ml/*.py` to run the NN and RF model.
4. Analyze and compare the output of the models.

I also included an html version of the entire system working to see it in action without executing the files.
See the PDF for the full idea presented at the Hackaton!