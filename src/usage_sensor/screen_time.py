import numpy as np
import pandas as pd



#def main_executor():


#screen status, one of the following: 0=off, 1=on, 2=locked, 3=unlocked
# Maybe check if screen on, extract timestamps, and from those gather usage
# instead of check app & then check screen time
#TODO: order dfs!
def main_executor(screen_path, apps_path):
    screen_df = pd.read_csv(screen_path)
    app_df = pd.read_csv(apps_path)
    app_df.sort_values(by=['timestamp'], inplace=True)
    screen_df.sort_values(by=['timestamp'], inplace=True)

    # Convert to datetime column
    app_df['datetime'] = pd.to_datetime(app_df['timestamp'], unit='ms')
    app_df["date"] = app_df["datetime"].dt.date
    app_df["time"] = app_df["datetime"].dt.time
    # Convert to datetime column
    screen_df['datetime'] = pd.to_datetime(screen_df['timestamp'], unit='ms')
    screen_df["date"] = screen_df["datetime"].dt.date
    screen_df["time"] = screen_df["datetime"].dt.time
    print(app_df['datetime'].min(), app_df['datetime'].max())
    print(screen_df['datetime'].min(), screen_df['datetime'].max())

    # screen off or locked
    #TODO: group by hour
    data = find_stop_time(app_df, screen_df[screen_df["screen_status"].isin([0, 2])])

    for key, value in data.items():
        print(" ----" , app_df[["datetime", "application_name"]].iloc[key])
        print(pd.to_datetime(value, unit = "ms")) # if value is not -1...
        print("----------")

    '''# Sort both by time (required for merge_asof)
    app_df = app_df.sort_values('datetime')
    screen_df = screen_df.sort_values('datetime')

    min_time = min(app_df["timestamp"].min(), screen_df["timestamp"].min())
    max_time = max(screen_df["timestamp"].max(), app_df["timestamp"].max())

    min_time =  pd.to_datetime(min_time, unit='ms')
    max_time = pd.to_datetime(max_time, unit='ms')'''

    '''
    #either this or n^2...
    # Make sure bins span full range
    bin_edges = pd.date_range(start=min_time, end=max_time + pd.Timedelta(minutes=10), freq='10min')
    print(bin_edges)
    # For df1
    app_df['bin'] = pd.cut(app_df['datetime'], bins=bin_edges)

    # For df2
    screen_df['bin'] = pd.cut(screen_df['datetime'], bins=bin_edges)

    print(app_df[["datetime","bin"]].head(), "\n",screen_df[["datetime","bin"]].head())

    '''

def extract_usage(screen_df, app_df):
    df_len = len(app_df)
    for index, row in app_df.iterrows():
        # Ignore last element
        if index == df_len -1:
            break
        app_name = row["application_name"]
        start_time = row["timestamp"]
        end_time = app_df.iloc[index+1]["timestamp"]
        screen_events = []


def find_stop_time(app_df, screen_df):
    """
    For each df1 row finds the closest timestamp that indicates a stopped execution of it (lock screen, off, or switch to another app)
    :param app_df:
    :param screen_df:
    :return: dict { K : V } where K is index of df1 and V is a timestamp
    """
    # ordered ascent by timestamp
    index2 = 0

    df2_len = len(screen_df)
    df1_len = len(app_df)
    data = dict()
    for index, row in app_df.iterrows():
        data[index] = - 1
        if index == df1_len - 1:
            continue
        cur_timestamp = row["timestamp"]
        next_timestamp = app_df.iloc[index+1]["timestamp"]
        data[index] = next_timestamp
        # O(n^2) ç_ç
        for i in range(0, df2_len-1):
            row2 = screen_df.iloc[i]
            timestamp_difference = cur_timestamp - row2["timestamp"]
            if  timestamp_difference < 0:
                if data[index] > row2["timestamp"]:
                    data[index] = row2["timestamp"]
                break

    return (data)

'''def find_next_lock(app_df, screen_df):
    """
    For each df1 row finds the closest screen lock event
    :param app_df:
    :param screen_df:
    :return:
    """
    # ordered ascent by timestamp

    index2 = 0

    df2_len = len(screen_df)
    data = { x : [-1, -1] for x in range(0,len(app_df)) }
    for index, row in app_df.iterrows():
        previous_difference_right = -9999999999999999
        if index == 0:
            continue
        cur_timestamp = row["timestamp"]
        # O(n^2) ç_ç
        for i in range(0, df2_len-1):
            row2 = screen_df.iloc[i]
            timestamp_difference = cur_timestamp - row2["timestamp"]
            if  timestamp_difference < 0:
                data[index][1] = i
                break
    return (data)'''


'''
def find_closest_events(app_df, screen_df):
    """
    For each df1 row finds the closest df2 row in terms of timestamps, so the previous one and the next one.
    :param app_df:
    :param screen_df:
    :return:
    """
    # ordered ascent by timestamp

    index2 = 0

    df2_len = len(screen_df)
    data = { x : [-1, -1] for x in range(0,len(app_df)) }
    for index, row in app_df.iterrows():
        previous_difference_left = 9999999999
        previous_difference_right = -9999999999
        if index == 0:
            continue
        cur_timestamp = row["timestamp"]
        # O(n^2) ç_ç
        for i in range(0, df2_len-1):
            row2 = screen_df.iloc[i]
            timestamp_difference = cur_timestamp - row2["timestamp"]
            if timestamp_difference <= previous_difference_left and timestamp_difference > 0:
                data[index][0] = i

                previous_difference_left = timestamp_difference
            if timestamp_difference >= previous_difference_right and timestamp_difference < 0:  # No good fit, index2 getting too big anyway
                data[index][1] = i
                previous_difference_right = timestamp_difference
                break



    return (data)'''

app_path = r"C:\Users\Ubicomp\Desktop\apps.csv"
screen_path = r"C:\Users\Ubicomp\Desktop\screen.csv"
main_executor(screen_path, app_path)