import os
import re
from collections import defaultdict
from datetime import datetime


def summarize_log_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile:
        narrator_log_lines = infile.readlines()
    summary = summarize_narrator_log(narrator_log_lines)
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(summary)

import re
from collections import defaultdict
from datetime import datetime

def parse_narrator_timestamp(line):
    match = re.match(r'(\w+ \w+ \d+ \d+:\d+:\d+)', line)
    if match:
        return datetime.strptime(match.group(1), "%a %b %d %H:%M:%S")
    return None

def get_hour_bin(dt):
    # Return string like '10:00-11:00'
    if dt:
        hour = dt.hour
        return f"{hour:02d}:00-{hour+1:02d}:00"
    else:
        return "Unknown"

def summarize_narrator_log(narrator_log_lines):
    app_usage_by_hour = defaultdict(lambda: defaultdict(int))
    screen_sessions = defaultdict(list)  # hour_bin -> list of (start_time, end_time)
    last_screen_on_time = None
    last_screen_off_time = None
    last_screen_on_timestamp = None

    screen_on_events = []
    app_open_events = []

    for line in narrator_log_lines:
        timestamp = parse_narrator_timestamp(line)
        hour_bin = get_hour_bin(timestamp)

        # Screen events
        if "screen status" in line:
            if "Phone screen turned on" in line:
                last_screen_on_time = timestamp
                last_screen_on_timestamp = timestamp
                screen_on_events.append(timestamp)
            elif "Phone screen turned off" in line and last_screen_on_time:
                # Record session
                session_length = (timestamp - last_screen_on_time).seconds if timestamp else 0
                screen_sessions[hour_bin].append((last_screen_on_time, timestamp, session_length))
                last_screen_on_time = None

        # App usage
        elif "applications" in line:
            m = re.search(r'Opened the app (.+)', line)
            if m:
                app_name = m.group(1).strip()
                app_usage_by_hour[hour_bin][app_name] += 1
                app_open_events.append((timestamp, app_name))

    # Now compute time gaps between screen ON events per hour
    time_gaps_by_hour = defaultdict(list)
    prev_on_time = None
    for on_time in screen_on_events:
        hour_bin = get_hour_bin(on_time)
        if prev_on_time:
            gap_sec = (on_time - prev_on_time).seconds
            time_gaps_by_hour[hour_bin].append(gap_sec)
        prev_on_time = on_time

    # Build summary text
    summary = []

    summary.append("Screen usage sessions by hour:")
    for hour in sorted(screen_sessions.keys()):
        sessions = screen_sessions[hour]
        total_screen_time = sum([s[2] for s in sessions])
        summary.append(f"- {hour}: {len(sessions)} sessions, total screen time ~{total_screen_time // 60} min")
        for start, end, length in sessions:
            summary.append(f"  - Session {start.strftime('%H:%M:%S')} to {end.strftime('%H:%M:%S')} ({length} sec)")

    summary.append("\nApp usage by hour (app opens):")
    for hour in sorted(app_usage_by_hour.keys()):
        app_summary = ", ".join([f"{app}: {count}x" for app, count in app_usage_by_hour[hour].items()])
        summary.append(f"- {hour}: {app_summary}")

    summary.append("\nScreen ON gaps by hour:")
    for hour in sorted(time_gaps_by_hour.keys()):
        gaps = time_gaps_by_hour[hour]
        if gaps:
            min_gap = min(gaps)
            max_gap = max(gaps)
            avg_gap = sum(gaps) / len(gaps)
            summary.append(f"- {hour}: min gap {min_gap}s, max gap {max_gap}s, avg gap {avg_gap:.1f}s")
        else:
            summary.append(f"- {hour}: no gaps (single event)")

    return "\n".join(summary)


if __name__ == "__main__":
    input_path = "narrator_logs/ca904fe8-f242-4306-85dc-0f1182443365/2025-06-12/ca904fe8-f242-4306-85dc-0f1182443365_2025-06-12.txt"
    output_path = os.path.join(
        "narrator_summaries",
        os.path.relpath(input_path, "narrator_logs")
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    summarize_log_file(input_path, output_path)