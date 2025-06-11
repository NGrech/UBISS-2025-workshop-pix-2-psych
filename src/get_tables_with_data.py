import pymysql
from dotenv import dotenv_values

def get_non_empty_tables(host, user, password, database):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    non_empty_tables = []
    try:
        with conn.cursor() as cursor:
            # Get list of all table names
            cursor.execute("SHOW TABLES;")
            tables = [row[0] for row in cursor.fetchall()]

            for table in tables:
                query = f"SELECT COUNT(*) FROM `{table}`;"
                cursor.execute(query)
                count = cursor.fetchone()[0]
                if count > 0:
                    non_empty_tables.append(table)

                    print(f"Table `{table}` has {count} rows.")

    finally:
        conn.close()

    return non_empty_tables


# Example usage:
if __name__ == "__main__":
    # Load environment variables from .env
    config = dotenv_values(".env")

    # Read credentials
    user = config['MYSQL_USER']
    password = config['MYSQL_PASSWORD']
    host = config['MYSQL_HOST']
    database = config['MYSQL_DATABASE']

    tables = ["accelerometer"] 
    output_dir = "./csv_exports" 

    print(get_non_empty_tables(host, user, password, database))