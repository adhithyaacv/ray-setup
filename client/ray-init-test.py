import ray
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np

runtime_env = {"pip": ["scikit-learn","pandas", "numpy"]}

# Connect to the Ray cluster
ray.init("ray://0.0.0.0:10001",runtime_env=runtime_env)  # Connect to Ray cluster
# ray.init("ray://0.0.0.0:10001") 
# Sample data (as an example CSV format)
data = {
    "make": ["Honda", "Toyota", "Ford", "BMW", "Audi"],
    "model": ["Civic", "Corolla", "Focus", "320i", "A4"],
    "trim": ["EX", "LE", "SE", "Base", "Premium"],
    "year": [2021, 2020, 2019, 2022, 2023],
    "discount_price": [25000, 20000, 18000, 40000, 35000],
    "actual_price": [30000, 25000, 22000, 50000, 45000],
    "odometer": [10000, 15000, 20000, 5000, 12000],
    "pincode": [5001, 5002, 5003, 5004, 5005],
    "ytd": [15000, 12000, 10000, 30000, 18000],
    "ownership_weightage": [1.2, 1.1, 1.3, 1.5, 1.4],
    "fuel": ["Petrol", "Diesel", "Petrol", "Diesel", "Petrol"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Define data transformations
def transform_data(df):
    # Label Encoding for categorical columns
    label_encoder = LabelEncoder()
    df['make'] = label_encoder.fit_transform(df['make'])
    df['model'] = label_encoder.fit_transform(df['model'])
    df['trim'] = label_encoder.fit_transform(df['trim'])
    df['fuel'] = label_encoder.fit_transform(df['fuel'])

    # Scaling numeric columns
    scaler = StandardScaler()
    numeric_columns = ['discount_price', 'actual_price', 'odometer', 'ytd', 'ownership_weightage']
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    return df

# Ray remote function to process data in parallel
@ray.remote
def process_data_batch(df_batch):
    return transform_data(df_batch)

# Split the DataFrame into smaller chunks to distribute processing
num_chunks = 2  # Number of chunks for parallelism (adjust as needed)
chunks = np.array_split(df, num_chunks)

# Apply the transformation in parallel
results = ray.get([process_data_batch.remote(chunk) for chunk in chunks])

# Combine results back into a single DataFrame
final_result = pd.concat(results)

# Display the transformed data
print(final_result)

# Shutdown Ray after processing
ray.shutdown()
