import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
COLNAMES = ["double_values_0", "double_values_1", "double_values_2"]

'''
One-in-all code that, given gravity and accelerometer data (note:stripped of gravity), to detect steps.
Flow:
    * Read acceleration & gravity data
    * Filter acceleration
    * Sync them by aligning to the closest timestamp in a +- 10microseconds range
    * Extract vertical movement using dot product
    * Compute steps according to this paper -> "FootPath: Accurate Map-based Indoor Navigation  Using Smartphones"
    
Filtering and step detection parameters can be tuned
'''

def step_executor(linear_acc_df, gravity_df, plot=False):
    """
    Calls other functions, basically executes the flow. Takes in input dataframe of linear acceleration & gravity,
    divided by day and user. Works otherwise, but output becomes unreliable
    :param linear_acc_df: csv file of linear acceleration data
    :param gravity_df:  csv file of gravity
    :param plot: whether to plot or not at the end of the step detection process
    """
    # Sorting --- ---
    linear_acc_df.sort_values(by=['timestamp'], inplace = True)
    gravity_df.sort_values(by=['timestamp'], inplace=True)
    # Reset indexes
    linear_acc_df.reset_index(inplace = True)
    gravity_df.reset_index(inplace=True)
    # --- --- --- ---
    linear_acc_df.rename(columns={"double_values_0": "x", "double_values_1": "y", "double_values_2": "z"}, inplace=True)
    gravity_df.rename(columns={"double_values_0": "x", "double_values_1": "y", "double_values_2": "z"}, inplace=True)
    # Sync here ---
    # for each record take one that is close in time stamp by less than 10 milliseconds (still not good but whatever)
    synced_df = sync_df(linear_acc_df, gravity_df)
    #Convert to vector
    linear_acc_vector = synced_df[["xacceleration","yacceleration","zacceleration"]].to_numpy()
    gravity_vector = synced_df[["xgravity","ygravity","zgravity"]].to_numpy()

    #Count steps
    print("counting steps..")
    step_list, step_count = acc_gravity_to_steps(linear_acc_vector, gravity_vector)

    #Step list is in form [ xxx 1 000 1 xxx], where 1s border the steps
    #step_counts_summary = "10:00-11:00: 500 steps\n11:00-12:00: 600 steps\n..."
    data = dict()
    for index in range(0, len(step_list)):
        if step_list[index] == 1:
            cur_timestamp = linear_acc_vector.iloc[index]["timestamp"]
            data[cur_timestamp] = data.get(cur_timestamp, 0) + 1

    hourly_data = dict()
    for ts_ms, steps in data.items():
        dt = datetime.fromtimestamp(ts_ms / 1000)  # convert ms to seconds
        hour_key = dt.replace(minute=0, second=0, microsecond=0)  # round down to the hour
        hourly_data[hour_key] = hourly_data.get(hour_key, 0) + steps

    result = sorted(hourly_data.items())

    return result



def acc_gravity_to_steps(linar_acceleration, gravity):
    """
    Perform preliminary steps and calls the step detection function. Preliminary steps include:
    filtering the acceleration data, and computing the vertical movement component
    :param linar_acceleration: pandas dataframe containing acceleration data
    :param gravity: andas dataframe containing gravity data
    """
    filtered_acceleration = highpass(0.1, 0.8, linar_acceleration)
    # Normalize gravity
    gravity = normalize_v(gravity)
    # Let's assume axis direction is alright...
    # Glorified dot product
    vertical_movement = np.einsum('ij,ij->i', filtered_acceleration, gravity)
    step_list, step_count = footpath_detector(vertical_movement)

    return(step_list, step_count)

def normalize_v(vector):
    """
    Util function to normalize a vector
    :param vector: vector to normalize
    :return: normalized vector
    """
    v_norm = np.linalg.norm(vector)
    if v_norm == 0:
        return None
    elif abs(v_norm - 1) <= 0.003:
        return vector
    else:
        return (vector / v_norm)


# Filter -----------------------


def highpass(dt, RC, x):
    """
    Highpass filter implemented as it is described on wikipedia: https://en.wikipedia.org/wiki/High-pass_filter
    :param dt:
    :param RC:
    :param x:
    :return:
    """
    lenx = len(x)
    y = np.zeros_like(x)
    a = RC / (RC + dt)
    y[0] = x[0]
    for i in range(1, lenx):
        y[i] = a * y[i - 1] + a * (x[i] - x[i - 1])
    return y


# Steps --------------------------


def footpath_detector(filtered_z, step_acc=2, window_size=210, timeout=333):
    """
    Step detector implemented as "FootPath: Accurate Map-based Indoor Navigation Using Smartphones" paper
    returned step_list is a vector like  [  0 0 0 1 0 0 0 1 3 3 3 0 0 1 0 0 1 3 3 3 0 ]
    where 1s enclose a step, and 3 indicate timeout time.
    Each value is a point in time of the given vertical acceleration dataframe.
    :param filtered_z: A vertical acceleration component that is reasonably smoothed
    :param step_acc: acceleration as in m/s^2 that will serve as threshold to recognize steps
    :param window_size: window in which acceleration is analyzed to see if it drops below step_acc
    :param timeout: amount of time to wait before detecting a step again
    :return: step count, step list as a vector
    """
    len_z = len(filtered_z)

    step_list = np.zeros(len_z)
    window_size = window_size // 100  # it is expressed in ms originally, we have a s/100 sample rate (10ms)
    timeout = timeout // 100
    i = 0
    step_count = 0

    while i + window_size < len(filtered_z):
        window_list = np.array(
            filtered_z[i:i + window_size])  # <- 0-n indexing if the input is a df slice instead of np array
        drop = 0

        for x in range(window_size - 1):
            # if  window_list[x + 1] < window_list[x]:

            drop += window_list[x] - window_list[x + 1]  # window_list[x] - window_list[x + 1]
        zorder = 3
        if drop >= step_acc:
            # Step mark
            step_list[i] = 1
            step_list[i + window_size] = 1
            step_count += 1
            # Cooldown
            if i + window_size + 1 < len_z:
                step_list[i + window_size + 1] = 3
            if i + window_size + timeout - 1 < len_z:
                step_list[i + window_size + timeout - 1] = 3

            i = i + window_size + timeout
        else:
            i += 1
    return step_list, step_count


# Sync ------------

def sync_df(df1, df2):
    """
    Sync of linear acceleration and gravity datasets by pairing timestamps no more distant than 10 ms.
    Is not very smart, you may want to use something more scientific
    :param df1: first dataframe to align
    :param df2: second dataframe to align
    :return: new dataframe with aligned rows (each row 
    """
    # Assume ascent order by timestamp
    index1 = 0
    index2 = 0
    pairs = []
    df2_len = len(df2)
    for index, row in df1.iterrows():
        cur_pair = (index1, -1)
        cur_timestamp = row["timestamp"]
        row2 = df2.iloc[index2]
        timestamp_difference = cur_timestamp - row2["timestamp"]
        if timestamp_difference <= 10 and timestamp_difference >= -10:
            cur_pair = (index1, index2)
            index2 += 1
        else:
            for i in range(index2, min(index2 + 1001, df2_len-1)):
                row2 = df2.iloc[i]
                timestamp_difference = cur_timestamp - row2["timestamp"]
                if timestamp_difference <= 10 and timestamp_difference >= -10:
                    cur_pair = (index1, index2)
                    index2 += 1
                    break
                elif timestamp_difference <= -1000:  # No good fit, index2 getting too big anyway
                    cur_pair = (index1, -1)
                    break

        index1 += 1
        pairs.append(cur_pair)

    merged_rows = []
    for pair in pairs:
        # Drop unmatched timestamps
        if pair[1] != -1:
            row1 = df1.iloc[[pair[0]]].reset_index(drop=True)  # note double brackets to keep DataFrame shape
            row2 = df2.iloc[[pair[1]]].reset_index(drop=True)
            merged = row1.merge(row2, left_index=True, right_index=True, suffixes=('acceleration', 'gravity'))
            merged_rows.append(merged)

    newdf = pd.concat(merged_rows, axis=0)
    return (newdf)



