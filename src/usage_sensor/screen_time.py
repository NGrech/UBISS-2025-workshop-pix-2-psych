import numpy as np
import pandas as pd


#screen status, one of the following: 0=off, 1=on, 2=locked, 3=unlocked
def screen_executor(screen_df, app_df):
    """
    From tables 'screen' and 'applications_foreground' in csv, extract app usage in format:
    10:00-11:00: Instagram 15min\n11:00-12:00: Facebook 25min\n14:00-15:00: Instagram 45min
    Assumes passed csv files contains a day of data.
    :param screen_df:  dataframe containing the 'screen' table
    :param app_df:  dataframe containing the 'applications_foreground' table
    """
    #Sort and reset index
    app_df.sort_values(by=['timestamp'], inplace=True)
    app_df.reset_index(inplace=True)
    screen_df.sort_values(by=['timestamp'], inplace=True)
    screen_df.reset_index(inplace=True)

    # Convert to datetime and add column
    app_df['datetime'] = pd.to_datetime(app_df['timestamp'], unit='ms')
    app_df["date"] = app_df["datetime"].dt.date
    app_df["time"] = app_df["datetime"].dt.time

    screen_df['datetime'] = pd.to_datetime(screen_df['timestamp'], unit='ms')
    screen_df["date"] = screen_df["datetime"].dt.date
    screen_df["time"] = screen_df["datetime"].dt.time

    #LEave only relevant screen events: 0=off and  2=locked
    data = find_stop_time(app_df, screen_df[screen_df["screen_status"].isin([0, 2])])

    # Want format: app_usage_summary = "10:00-11:00: Instagram 15min\n11:00-12:00: Facebook 25min\n14:00-15:00: Instagram 45min"
    app_summary = ""
    for key, value in data.items():
        app_name = app_df[["application_name"]].iloc[key].values[0] #System UI
        dates = pd.to_datetime(value, unit="ms")
        diff_minutes = round((dates[1] - dates[0]).total_seconds() / 60, 2)
        app_summary+=f"{dates[0].strftime('%H:%M')}-{dates[1].strftime('%H:%M')}: {app_name} {diff_minutes}min\n"
    #print(app_summary)
    return app_summary


def find_stop_time(app_df, screen_df):
    """
    For each df1 row finds the closest timestamp that indicates a stopped execution of it, such as
    lock screen, screen-off, or switch to another app. Assumes ascent order by timestamp
    :param app_df: pandas dataframe of the applications_foreground table
    :param screen_df: pandas dataframe of the screen table
    :return: dict { K : [START, END] } where K is index of df1 and START, END are the start and end timestamps
    """
    # Get lengths
    df2_len = len(screen_df)
    df1_len = len(app_df)
    data = dict()
    for index, row in app_df.iterrows():
        # Ignore last entry
        if index == df1_len - 1:
            continue
        cur_timestamp = row["timestamp"]
        data[index] = [cur_timestamp,cur_timestamp ]
        next_timestamp = app_df.iloc[index+1]["timestamp"]
        data[index][1] = next_timestamp
        # O(n^2) ç_ç
        for i in range(0, df2_len-1):
            row2 = screen_df.iloc[i]
            timestamp_difference = cur_timestamp - row2["timestamp"]
            if  timestamp_difference < 0:
                if data[index][1] > row2["timestamp"]:
                    data[index][1] = row2["timestamp"]
                break

    return (data)