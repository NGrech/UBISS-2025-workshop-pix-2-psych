import time
from data_collection import export_tables_to_csv
from datetime import datetime, timedelta
from dotenv import dotenv_values
import yaml
import os
from pytz import timezone, utc


DEVICE_IDS = ['ca904fe8-f242-4306-85dc-0f1182443365', '2b2edf90-f71c-4f4d-9804-c91c71e80f84', '669164ce-b5a6-414d-9a97-f1d0e6c1ebc2']
TABLES = [
    'accelerometer',
    'applications_foreground',
    'applications_notifications',
    'battery',
    'esms',
    'gravity',
    'gyroscope',
    'linear_accelerometer',
    'locations',
    'screen',
    'telephony',
    'touch',
    'aware_log',           # optional
    'aware_studies'        # optional
]

def run_aware_narrator_cfg(dates):

    # getting the time ranges
    day_timestamps = []
    for date in dates:
        # Parse the date string
        day = datetime.strptime(date, "%Y-%m-%d")
        # Set timezone to GMT+2
        tz = timezone('Etc/GMT-2')  # GMT+02:00 is Etc/GMT-2 in pytz
        # Start at 8:00 AM in GMT+2
        start_dt = tz.localize(day.replace(hour=8, minute=0, second=0, microsecond=0))
        # End at 7:59:59 AM the next day in GMT+2
        end_dt = tz.localize((day + timedelta(days=1)).replace(hour=7, minute=59, second=59, microsecond=0))
        # Convert to milliseconds since epoch
        start_time = int(start_dt.timestamp() * 1000)
        end_time = int(end_dt.timestamp() * 1000)
        day_timestamps.append((start_time, end_time))
    
    # loading .env variables
    config = dotenv_values(".env")

    # Read credentials
    user = config['MYSQL_USER']
    password = config['MYSQL_PASSWORD']
    host = config['MYSQL_HOST']
    database = config['MYSQL_DATABASE']



    # getting the data 
    for start_ts, end_ts in day_timestamps:
        print(f"Processing data from {start_ts} to {end_ts}")
        # Create a subdirectory for each day based on the start date
        day_str = datetime.fromtimestamp(start_ts / 1000).strftime("%Y-%m-%d")
        export_path = os.path.join(".", "csv_exports", day_str)
        export_tables_to_csv(host, user, password, database, TABLES, export_path, start_ts, end_ts)


        for device_id in DEVICE_IDS:
            # for each device, update the narrator config
            # Load the config
            with open(os.path.join(".", "config.yaml"), "r") as f:
                narrator_cfg = yaml.safe_load(f)

            # Update fields
            narrator_cfg['DEVICE_IDs'] = [device_id]
            # Convert timestamps to the required string format in GMT+02:00
            tz = timezone('Etc/GMT-2')  # GMT+02:00 is Etc/GMT-2 in pytz (note the sign is reversed)
            start_dt_local = datetime.fromtimestamp(start_ts / 1000, tz)
            end_dt_local = datetime.fromtimestamp(end_ts / 1000, tz)
            narrator_cfg['START_TIME'] = start_dt_local.strftime("%Y-%m-%d %H:%M:%S")
            narrator_cfg['END_TIME'] = end_dt_local.strftime("%Y-%m-%d %H:%M:%S")
            narrator_cfg['timezone'] = 'Etc/GMT-2'
            narrator_cfg['daily_output_dir'] = os.path.join(".", "narrator_logs", device_id, day_str)
            narrator_cfg['output_file'] = os.path.join(".", "narrator_logs", device_id, day_str, f"{device_id}_{day_str}.txt")
            #narrator_cfg['GOOGLE_MAP_KEY'] = config.get('GOOGLE_MAP_KEY', '')
            narrator_cfg['csv_directory'] = export_path

            # Save the updated config
            updated_cfg_path = os.path.join(".", "config.yaml")
            with open(updated_cfg_path, "w") as f:
                yaml.safe_dump(narrator_cfg, f)
            # run the narrator with the updated config
            print(f"Running narrator for device {device_id} on {day_str} ")
            os.system(f'pixi run python {os.path.join("externals", "aware_narrator", "AWARE_Narrator.py")}')
            break
            

    # Reload the config file and remove the GOOGLE_MAP_KEY
    cfg_path = os.path.join(".", "config.yaml")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r") as f:
            narrator_cfg = yaml.safe_load(f)
        if 'GOOGLE_MAP_KEY' in narrator_cfg:
            narrator_cfg['GOOGLE_MAP_KEY'] = ''
            with open(cfg_path, "w") as f:
                yaml.safe_dump(narrator_cfg, f)



# Example usage:
if __name__ == "__main__":
    # Define the dates for which you want to run the narrator
    dates = ['2025-06-12'] 
    # Run the Aware Narrator configuration for the specified dates
    run_aware_narrator_cfg(dates)