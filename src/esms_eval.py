# esm_processing.py

import csv
import pandas as pd
from datetime import datetime
import json
from collections import defaultdict

QUESTION_MAP = {
        1: "How do you feel about your progress yesterday",
        2: "What’s one thing you’d like to do differently today?",
        3: "What is your main focus for today?",
        4: "What is one specific goal you want to commit to today?",
        5: "Do you feel you’re staying on track with your goal?",
        6: "How satisfied are you with your progress so far?",
        7: "Have you noticed anything making it easier or harder to stick to your goal?",
        8: "How successful were you in sticking to your goal today?",
        9: "How happy are you with your progress today?",
        10: "What helped you sticking to your goal? What didn’t help?"
    }


def parse_esm_csv(csv_path):
    import json
    df = pd.read_csv(
        csv_path,
        sep=',',
        quotechar='"',
        encoding='utf-8',
        on_bad_lines='warn'  
    )

    # Convert timestamp to date
    df['date'] = pd.to_datetime(df['double_esm_user_answer_timestamp'], unit='ms').dt.date
    df['time'] = pd.to_datetime(df['double_esm_user_answer_timestamp'], unit='ms').dt.strftime('%H:%M')

    # Now parse esm_json into a dict column
    df['esm_json_dict'] = df['esm_json'].apply(lambda x: json.loads(x) if pd.notnull(x) else {})

    # Group by date
    grouped = df.groupby('device_id')

    parsed_data = {}

    for deviceId, group in grouped:
        day_record = {
            "progress_yesterday": None,            # Q1 → Likert
            "improvement_plan": "",                # Q2 → Free text
            "goal_main_focus": [],                 # Q3 → Checkboxes
            "goal_text": "",                       # Q4 → Free text
            "checkins": [],                        # Q5-Q7 → list of dicts
            "reflection_success": None,            # Q8 → Likert
            "reflection_happiness": None,          # Q9 → Likert
            "reflection_comment": ""               # Q10 → Free text
        }

        for _, row in group.iterrows():
            qid = row['esm_json_dict'].get('id', None)
            trigger = row['esm_json_dict'].get('esm_trigger', None)
            time = row['time']

            # Extract all possible answer fields consistently
            answer_text = row.get('esm_user_answer_text', None)
            answer_label = row.get('esm_user_answer', None) or row.get('esm_user_answer_label', None)
            answer_number = row.get('esm_user_answer_number', None)

            # Process according to qid
            if qid == 1:
                # Q1 → Progress yesterday → Likert number
                day_record['progress_yesterday'] = answer_number
            elif qid == 2:
                # Q2 → What to do differently → Free text
                day_record['improvement_plan'] = answer_text
            elif qid == 3:
                # Q3 → "What is your main focus for today?" → checkboxes
                if pd.notna(answer_text):
                    if answer_text.startswith('['):
                        try:
                            day_record['goal_main_focus'] = json.loads(answer_text)
                        except:
                            day_record['goal_main_focus'] = []
                    else:
                        day_record['goal_main_focus'] = [item.strip() for item in answer_text.split(';') if item.strip()]
            elif qid == 4:
                # Q4 → "One specific goal" → free text
                day_record['goal_text'] = answer_text
            elif qid in [5, 6, 7]:
                # Hourly check-in (Q5, Q6, Q7)
                checkin_entry = None
                # Check if we're continuing the last check-in (same timestamp)
                if day_record['checkins'] and day_record['checkins'][-1]['time'] == time:
                    checkin_entry = day_record['checkins'][-1]
                else:
                    checkin_entry = {
                        "time": time,
                        "trigger": trigger,
                        "on_track": None,
                        "satisfaction": None,
                        "comment": ""
                    }
                    day_record['checkins'].append(checkin_entry)

                if qid == 5:
                    # Q5 → Radio Yes/No → use label
                    checkin_entry['on_track'] = answer_label
                elif qid == 6:
                    # Q6 → Likert satisfaction → use number
                    checkin_entry['satisfaction'] = answer_number
                elif qid == 7:
                    # Q7 → Free text comment
                    checkin_entry['comment'] = answer_text
            elif qid == 8:
                # Q8 → Reflection success (Likert)
                day_record['reflection_success'] = answer_number
            elif qid == 9:
                # Q9 → Reflection happiness (Likert)
                day_record['reflection_happiness'] = answer_number
            elif qid == 10:
                # Q10 → Reflection free text
                day_record['reflection_comment'] = answer_text

            parsed_data[(str(deviceId), row['timestamp'])] = day_record
        return parsed_data


if __name__ == "__main__":
    csv_path = "./phone_esms_raw.csv"
    parsed_data = parse_esm_csv(csv_path)
    for date, record in parsed_data.items():
        print(f"Date: {date}")
        print(record)