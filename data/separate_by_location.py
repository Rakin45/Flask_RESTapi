import pandas as pd
import os

df = pd.read_csv('./original_data/dataset_prepared.csv')

location_ids = df['Location ID'].unique()

for location_id in location_ids:
    df_location = df[df['Location ID'] == location_id]
    
    output_file_name = f'{location_id}.csv'
    output_file_path = os.path.join('./data', output_file_name)
    
    df_location.to_csv(output_file_path, index=False)

