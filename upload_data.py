import os
import csv
from datetime import datetime
from webapp import create_app, db
from webapp.models import WaterQualityData


app = create_app()
app.app_context().push()

csv_directory = './data'  
csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

def process_csv_file(csv_file_path, location_id):
    print(f"Processing {csv_file_path} for location {location_id}")
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            try:
                water_quality_entry = WaterQualityData(
                    location_id=location_id,
                    date=datetime.strptime(row[15], '%Y-%m-%d').date(),  
                    spec_cond_max=float(row[1]),  
                    ph_max=float(row[2]),  
                    ph_min=float(row[3]),  
                    spec_cond_min=float(row[4]),  
                    spec_cond_mean=float(row[5]),  
                    dissolved_oxy_max=float(row[6]),  
                    dissolved_oxy_mean=float(row[7]),  
                    dissolved_oxy_min=float(row[8]),  
                    temp_mean=float(row[9]),  
                    temp_min=float(row[10]),  
                    temp_max=float(row[11]),  
                    water_quality=float(row[12]),  
                    training=row[13].lower() == 'true'
                )
                db.session.add(water_quality_entry)
            except Exception as e:
                print(f"Error processing row {row}: {e}")
        db.session.commit()


def upload_data():
    print("Starting data upload...")
    app = create_app()
    with app.app_context():
        for csv_file in csv_files:
            location_id = int(csv_file.split('.')[0])  # Filename is the location ID
            csv_file_path = os.path.join(csv_directory, csv_file)
            process_csv_file(csv_file_path, location_id)
            
        db.session.commit()
    print("Data upload completed.")


if __name__ == '__main__':
    app = create_app()  
    with app.app_context():  
        upload_data()  

