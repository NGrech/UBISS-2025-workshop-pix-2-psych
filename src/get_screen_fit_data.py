from dotenv import dotenv_values
from data_collection import export_tables_to_csv
from datetime import datetime, timedelta
from movement_sensor.steps import step_executor
from usage_sensor.screen_time import screen_executor
import os
import warnings
import pandas as pd

def data_aggregator(csv_file_path, device_id):
    """
    From csv file path, returns pandas.DataFrame with data relevant to device_id user
    :param csv_file_path: path to a csv file that contains the "device_id" row
    :param device_id: device id as in aware.device
    :return: pandas.DataFrame with data corresponding only to that device_id
    """
    dataframe = pd.read_csv(csv_file_path)
    if "device_id" not in dataframe.columns:
        warnings.warn("device id column not in dataframe")
        return None
    return dataframe[dataframe["device_id"] == device_id]

def get_refined_data(device_id, start_ts = None, end_ts = None):
    """
     Get refined data of app usage and steps count from user specified by device_id.
     If either start or end timestamp is not passed, it'll use yesterday's data
    :param device_id: a device_id from aware.device table
    :param start_ts: optional, starting timestamp
    :param end_ts: optional, ending timestamps
    """
    if start_ts is None or end_ts is None:
        print("Processing yesterday's data...")
        # Yesterday start and end timestamps
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        start = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
        end = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59, 999999)
        # Convert to Unix timestamps in milliseconds
        start_ts = int(start.timestamp() * 1000)
        end_ts = int(end.timestamp() * 1000)

    # Load environment variables from .env
    config = dotenv_values(".env")

    # Read credentials
    user = config['MYSQL_USER']
    password = config['MYSQL_PASSWORD']
    host = config['MYSQL_HOST']
    database = config['MYSQL_DATABASE']
    tables = ['linear_accelerometer', 'gravity' ,'applications_foreground' ,'screen']
    output_dir = "./csv_exports"

    os.makedirs(output_dir, exist_ok=True)
    export_tables_to_csv(host, user, password, database, tables, output_dir,   start_ts, end_ts)

    # Call step count
    acceleration_path = os.path.join(output_dir, "phone_linear_accelerometer_raw.csv")
    gravity_path = os.path.join(output_dir, "phone_gravity_raw.csv")

    # Path for screen time
    apps_path = os.path.join(output_dir, "phone_applications_foreground_raw.csv")
    screen_path = os.path.join(output_dir, "phone_screen_raw.csv")

    steps_string = step_executor(data_aggregator(acceleration_path, device_id), data_aggregator(gravity_path, device_id))
    app_usage_string = screen_executor(data_aggregator(apps_path, device_id), data_aggregator(screen_path, device_id))


