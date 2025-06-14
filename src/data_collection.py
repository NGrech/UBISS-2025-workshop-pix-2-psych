import pandas as pd
import os
import warnings
import pymysql
from dotenv import dotenv_values

def export_tables_to_csv(host, user, password, database, tables, output_dir, start_ts=None, end_ts=None):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        
    )
    try:
        for table in tables:
             # Build the query with optional timestamp filtering
            query = f"SELECT * FROM `{table}`"
            if start_ts is not None and end_ts is not None:
                query += f" WHERE `timestamp` >= {int(start_ts)} AND `timestamp` < {int(end_ts)}"
            elif start_ts is not None:
                query += f" WHERE `timestamp` >= {int(start_ts)}"
            elif end_ts is not None:
                query += f" WHERE `timestamp` < {int(end_ts)}"

            # Fetch data in chunks to avoid memory issues with large tables
            chunk_size = 1000000
            csv_path = os.path.join(output_dir, f"phone_{table}_raw.csv")
            if os.path.exists(csv_path):
                print(f"File {csv_path} already exists. Skipping export for table {table}.")
                continue
            os.makedirs(output_dir, exist_ok=True)
            first_chunk = True
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)
                print(f"getting chunks .")
                for chunk in pd.read_sql(query, conn, chunksize=chunk_size):
                    chunk.to_csv(csv_path, mode='w' if first_chunk else 'a', header=first_chunk, index=False)
                    first_chunk = False
                    print(f"Processed chunk of {len(chunk)} rows for table {table}")
                print(f"Exported {table} to {csv_path}")
    finally:
        conn.close()

# Example usage:
if __name__ == "__main__":
    # Load environment variables from .env
    config = dotenv_values(".env")

    # Read credentials
    user = config['MYSQL_USER']
    password = config['MYSQL_PASSWORD']
    host = config['MYSQL_HOST']
    database = config['MYSQL_DATABASE']
    tables = ['esm']
    output_dir = "./csv_exports" 

    os.makedirs(output_dir, exist_ok=True)
    export_tables_to_csv(host, user, password, database, tables, output_dir,   '1749715200000', '1749801600000')