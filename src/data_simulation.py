import random



def generate_day_record_header(goal_text, reflection_success, reflection_comment):
    return {
        "progress_yesterday": 4,
        "improvement_plan": "Avoid using phone in afternoon.",
        "goal_main_focus": ["Reduce smartphone usage"],
        "goal_text": goal_text,
        "checkins": [],  # You will fill this separately
        "reflection_success": reflection_success,
        "reflection_happiness": reflection_success,  # For simplicity
        "reflection_comment": reflection_comment
    }

def generate_checkins(checkins_list):
    checkin_times = ["10:00", "12:00", "14:00", "16:00"]
    checkins = []
    for i, (on_track, satisfaction, comment) in enumerate(checkins_list):
        time = checkin_times[i] if i < len(checkin_times) else f"{10 + 2*i}:00"
        checkins.append({
            "time": time,
            "trigger": "Hourly check in",
            "on_track": on_track,
            "satisfaction": satisfaction,
            "comment": comment
        })
    return checkins

def good_daily_record():
    return {
        "progress_yesterday": 4,
        "improvement_plan": "Avoid using phone in afternoon.",
        "goal_main_focus": ["Reduce smartphone usage"],
        "goal_text": "Reduce smartphone usage to 3 hour per day.",
        "checkins": [
            {"time": "10:00", "trigger": "Hourly check in", "on_track": True, "satisfaction": 5, "comment": "Feeling good about my progress."},
            {"time": "12:00", "trigger": "Hourly check in", "on_track": True, "satisfaction": 4, "comment": "Staying on track."},
            {"time": "14:00", "trigger": "Hourly check in", "on_track": True, "satisfaction": 4, "comment": "Struggled against distractions."},
            {"time": "16:00", "trigger": "Hourly check in", "on_track": True, "satisfaction": 5, "comment": "Great end to the day!"}
        ],
        "reflection_success": 4,
        "reflection_happiness": 4,
        "reflection_comment": "I did well but could improve in the afternoon."
    }

def bad_daily_record():
    return {
        "progress_yesterday": 2,
        "improvement_plan": "Need to set stricter limits on phone usage.",
        "goal_main_focus": ["Reduce smartphone usage"],
        "goal_text": "Limit social media use to 2 hours today.",
        "checkins": [
            {"time": "10:00", "trigger": "Hourly check in", "on_track": False, "satisfaction": 2, "comment": "Struggled with distractions."},
            {"time": "12:00", "trigger": "Hourly check in", "on_track": False, "satisfaction": 3, "comment": "Used phone more than planned."},
            {"time": "14:00", "trigger": "Hourly check in", "on_track": False, "satisfaction": 2, "comment": "Lost track of time."},
            {"time": "16:00", "trigger": "Hourly check in", "on_track": False, "satisfaction": 1, "comment": "Very disappointed with my progress."}
        ],
        "reflection_success": 2,
        "reflection_happiness": 1,
        "reflection_comment": "I did not meet my goal and need to improve."
    }

def mixed_daily_record():
    return {
        "progress_yesterday": 3,
        "improvement_plan": "Focus on reducing afternoon phone usage.",
        "goal_main_focus": ["Reduce smartphone usage"],
        "goal_text": "Reduce smartphone usage to 2 hour per day.",
        "checkins": [
            {"time": "10:00", "trigger": "Hourly check in", "on_track": True, "satisfaction": 4, "comment": "Good start to the day."},
            {"time": "12:00", "trigger": "Hourly check in", "on_track": False, "satisfaction": 2, "comment": "Used phone more than expected."},
            {"time": "14:00", "trigger": "Hourly check in", "on_track": True, "satisfaction": 3, "comment": "Managed to reduce usage."},
            {"time": "16:00", "trigger": "Hourly check in", "on_track": True, "satisfaction": 4, "comment": "Feeling better about my progress."}
        ],
        "reflection_success": 3,
        "reflection_happiness": 3,
        "reflection_comment": "Mixed feelings about my progress today."
    }

def generate_app_usage_summary(usage_blocks):
    summary_lines = [f"{block}: {app} {minutes}min" for block, app, minutes in usage_blocks]
    return "\n".join(summary_lines)

def low_app_usage_summary():
    return generate_app_usage_summary([
        ("10:00-11:00", "Instagram", 15),
        ("11:00-12:00", "Facebook", 25),
        ("14:00-15:00", "Instagram", 45)
    ])

def high_app_usage_summary():
    return generate_app_usage_summary([
        ("10:00-11:00", "Instagram", 60),
        ("11:00-12:00", "Facebook", 90),
        ("14:00-15:00", "Instagram", 120),
        ("15:00-16:00", "YouTube", 30)
    ])

def late_night_app_usage_summary():
    return generate_app_usage_summary([
        ("22:00-23:00", "Instagram", 30),
        ("23:00-00:00", "YouTube", 45),
        ("00:00-01:00", "Twitter", 20)
    ])

def generate_step_count_summary(step_blocks):
    summary_lines = [f"{block}: {steps} steps" for block, steps in step_blocks]
    return "\n".join(summary_lines)

def low_step_count_summary():
    return generate_step_count_summary([
        ("10:00-11:00", 500),
        ("11:00-12:00", 600),
        ("14:00-15:00", 700)
    ])

def high_step_count_summary():
    return generate_step_count_summary([
        ("10:00-11:00", 1200),
        ("11:00-12:00", 1500),
        ("14:00-15:00", 1800),
        ("15:00-16:00", 2000)
    ])

def narrator_summary_full_day_example():
    return """Screen usage sessions by hour:
    - 08:00-09:00: 1 session, total screen time ~3 min
    - Session 08:15:02 to 08:18:21 (199 sec)
    - 09:00-10:00: 2 sessions, total screen time ~5 min
    - Session 09:05:12 to 09:07:45 (153 sec)
    - Session 09:45:30 to 09:47:12 (102 sec)
    - 10:00-11:00: 3 sessions, total screen time ~8 min
    - Session 10:13:02 to 10:16:39 (217 sec)
    - Session 10:30:15 to 10:32:42 (147 sec)
    - Session 10:50:01 to 10:52:03 (122 sec)
    - 11:00-12:00: 2 sessions, total screen time ~3 min
    - Session 11:15:17 to 11:16:48 (91 sec)
    - Session 11:48:22 to 11:50:31 (129 sec)
    - 12:00-13:00: 1 session, total screen time ~2 min
    - Session 12:25:09 to 12:27:20 (131 sec)
    - 13:00-14:00: 4 sessions, total screen time ~15 min
    - Session 13:10:05 to 13:15:47 (342 sec)
    - Session 13:25:31 to 13:29:10 (219 sec)
    - Session 13:45:02 to 13:47:56 (174 sec)
    - Session 13:55:20 to 13:58:41 (201 sec)
    - 14:00-15:00: 3 sessions, total screen time ~10 min
    - Session 14:12:15 to 14:16:30 (255 sec)
    - Session 14:33:50 to 14:36:29 (159 sec)
    - Session 14:50:02 to 14:52:30 (148 sec)
    - 15:00-16:00: 1 session, total screen time ~5 min
    - Session 15:20:14 to 15:25:32 (318 sec)
    - 16:00-17:00: 2 sessions, total screen time ~4 min
    - Session 16:10:03 to 16:12:44 (161 sec)
    - Session 16:50:11 to 16:53:12 (181 sec)
    - 17:00-18:00: 2 sessions, total screen time ~6 min
    - Session 17:15:20 to 17:18:31 (191 sec)
    - Session 17:40:01 to 17:43:42 (221 sec)
    - 18:00-19:00: 1 session, total screen time ~2 min
    - Session 18:25:17 to 18:27:58 (161 sec)
    - 19:00-20:00: 1 session, total screen time ~3 min
    - Session 19:33:09 to 19:36:12 (183 sec)

    App usage by hour (app opens):
    - 08:00-09:00: WhatsApp: 2x, Email: 1x
    - 09:00-10:00: Chrome: 1x, WhatsApp: 2x
    - 10:00-11:00: WhatsApp: 3x, Instagram: 2x
    - 11:00-12:00: Email: 1x, Calendar: 1x
    - 12:00-13:00: Instagram: 1x
    - 13:00-14:00: Instagram: 5x, Facebook: 2x
    - 14:00-15:00: Instagram: 3x
    - 15:00-16:00: WhatsApp: 1x
    - 16:00-17:00: YouTube: 2x
    - 17:00-18:00: WhatsApp: 2x
    - 18:00-19:00: Messages: 1x
    - 19:00-20:00: Netflix: 1x

    Screen ON gaps by hour:
    - 08:00-09:00: min gap 543s, max gap 543s, avg gap 543.0s
    - 09:00-10:00: min gap 231s, max gap 2412s, avg gap 1321.5s
    - 10:00-11:00: min gap 115s, max gap 1203s, avg gap 659.0s
    - 11:00-12:00: min gap 763s, max gap 1834s, avg gap 1298.5s
    - 12:00-13:00: min gap 2645s, max gap 2645s, avg gap 2645.0s
    - 13:00-14:00: min gap 95s, max gap 786s, avg gap 420.5s
    - 14:00-15:00: min gap 103s, max gap 1176s, avg gap 639.5s
    - 15:00-16:00: min gap 1536s, max gap 1536s, avg gap 1536.0s
    - 16:00-17:00: min gap 721s, max gap 2411s, avg gap 1566.0s
    - 17:00-18:00: min gap 1243s, max gap 1243s, avg gap 1243.0s
    - 18:00-19:00: min gap 3152s, max gap 3152s, avg gap 3152.0s
    - 19:00-20:00: min gap 2673s, max gap 2673s, avg gap 2673.0s"""

def narrator_summary_full_day_positive():
    return """Screen usage sessions by hour:
- 08:00-09:00: 1 session, total screen time ~3 min
  - Session 08:15:02 to 08:18:21 (199 sec)
- 09:00-10:00: 1 session, total screen time ~2 min
  - Session 09:45:30 to 09:47:12 (102 sec)
- 10:00-11:00: 1 session, total screen time ~4 min
  - Session 10:30:15 to 10:34:42 (267 sec)
- 11:00-12:00: 1 session, total screen time ~2 min
  - Session 11:48:22 to 11:50:31 (129 sec)
- 12:00-13:00: 0 sessions
- 13:00-14:00: 1 session, total screen time ~3 min
  - Session 13:25:31 to 13:28:41 (190 sec)
- 14:00-15:00: 1 session, total screen time ~2 min
  - Session 14:50:02 to 14:52:30 (148 sec)
- 15:00-16:00: 0 sessions
- 16:00-17:00: 1 session, total screen time ~2 min
  - Session 16:10:03 to 16:12:44 (161 sec)
- 17:00-18:00: 1 session, total screen time ~3 min
  - Session 17:15:20 to 17:18:31 (191 sec)
- 18:00-19:00: 0 sessions
- 19:00-20:00: 1 session, total screen time ~2 min
  - Session 19:33:09 to 19:36:12 (183 sec)

App usage by hour (app opens):
- 08:00-09:00: WhatsApp: 1x
- 09:00-10:00: Email: 1x
- 10:00-11:00: WhatsApp: 1x, Calendar: 1x
- 11:00-12:00: Email: 1x
- 13:00-14:00: Calendar: 1x
- 14:00-15:00: WhatsApp: 1x
- 16:00-17:00: YouTube: 1x (short)
- 17:00-18:00: Messages: 1x
- 19:00-20:00: Netflix: 1x

Screen ON gaps by hour:
- 08:00-09:00: min gap 543s, max gap 543s, avg gap 543.0s
- 09:00-10:00: min gap 2732s, max gap 2732s, avg gap 2732.0s
- 10:00-11:00: min gap 1643s, max gap 1643s, avg gap 1643.0s
- 11:00-12:00: min gap 2134s, max gap 2134s, avg gap 2134.0s
- 12:00-13:00: no sessions
- 13:00-14:00: min gap 4532s, max gap 4532s, avg gap 4532.0s
- 14:00-15:00: min gap 1862s, max gap 1862s, avg gap 1862.0s
- 15:00-16:00: no sessions
- 16:00-17:00: min gap 2267s, max gap 2267s, avg gap 2267.0s
- 17:00-18:00: min gap 1345s, max gap 1345s, avg gap 1345.0s
- 18:00-19:00: no sessions
- 19:00-20:00: min gap 2431s, max gap 2431s, avg gap 2431.0s"""


def narrator_summary_full_day_negative():
    return """Screen usage sessions by hour:
- 08:00-09:00: 1 session, total screen time ~3 min
  - Session 08:15:02 to 08:18:21 (199 sec)
- 09:00-10:00: 2 sessions, total screen time ~6 min
  - Session 09:05:12 to 09:07:45 (153 sec)
  - Session 09:45:30 to 09:49:42 (252 sec)
- 10:00-11:00: 3 sessions, total screen time ~10 min
  - Session 10:13:02 to 10:18:39 (337 sec)
  - Session 10:30:15 to 10:34:42 (267 sec)
  - Session 10:50:01 to 10:53:43 (222 sec)
- 11:00-12:00: 2 sessions, total screen time ~5 min
  - Session 11:15:17 to 11:17:48 (151 sec)
  - Session 11:48:22 to 11:52:31 (249 sec)
- 12:00-13:00: 2 sessions, total screen time ~6 min
  - Session 12:25:09 to 12:28:20 (191 sec)
  - Session 12:45:31 to 12:49:00 (209 sec)
- 13:00-14:00: 5 sessions, total screen time ~20 min
  - Session 13:10:05 to 13:17:47 (462 sec)
  - Session 13:25:31 to 13:31:10 (339 sec)
  - Session 13:35:02 to 13:39:56 (294 sec)
  - Session 13:45:20 to 13:49:41 (261 sec)
  - Session 13:55:30 to 13:58:52 (202 sec)
- 14:00-15:00: 4 sessions, total screen time ~18 min
  - Session 14:12:15 to 14:17:30 (315 sec)
  - Session 14:23:50 to 14:28:29 (279 sec)
  - Session 14:33:50 to 14:37:29 (219 sec)
  - Session 14:50:02 to 14:54:30 (268 sec)
- 15:00-16:00: 2 sessions, total screen time ~10 min
  - Session 15:20:14 to 15:25:32 (318 sec)
  - Session 15:45:01 to 15:48:42 (221 sec)
- 16:00-17:00: 2 sessions, total screen time ~8 min
  - Session 16:10:03 to 16:13:44 (221 sec)
  - Session 16:40:11 to 16:44:12 (241 sec)
- 17:00-18:00: 3 sessions, total screen time ~9 min
  - Session 17:15:20 to 17:19:31 (251 sec)
  - Session 17:40:01 to 17:43:42 (221 sec)
  - Session 17:55:11 to 17:58:32 (201 sec)

App usage by hour (app opens):
- 08:00-09:00: WhatsApp: 1x
- 09:00-10:00: Chrome: 2x, WhatsApp: 1x
- 10:00-11:00: Instagram: 3x
- 11:00-12:00: Instagram: 2x
- 12:00-13:00: Instagram: 2x
- 13:00-14:00: Instagram: 5x, Facebook: 3x
- 14:00-15:00: Instagram: 4x
- 15:00-16:00: YouTube: 2x
- 16:00-17:00: Instagram: 2x
- 17:00-18:00: Instagram: 3x

Screen ON gaps by hour:
- 08:00-09:00: min gap 543s, max gap 543s, avg gap 543.0s
- 09:00-10:00: min gap 231s, max gap 1203s, avg gap 717.0s
- 10:00-11:00: min gap 115s, max gap 563s, avg gap 339.0s
- 11:00-12:00: min gap 263s, max gap 1923s, avg gap 1093.0s
- 12:00-13:00: min gap 543s, max gap 964s, avg gap 753.5s
- 13:00-14:00: min gap 95s, max gap 386s, avg gap 245.5s
- 14:00-15:00: min gap 103s, max gap 476s, avg gap 289.5s
- 15:00-16:00: min gap 1536s, max gap 1536s, avg gap 1536.0s
- 16:00-17:00: min gap 721s, max gap 2411s, avg gap 1566.0s
- 17:00-18:00: min gap 543s, max gap 964s, avg gap 753.5s"""

#low screen/app usage — test "good behavior" even if user reflects negatively
def narrator_summary_full_day_sparse():
    return """Screen usage sessions by hour:
- 08:00-09:00: 1 session, total screen time ~2 min
  - Session 08:45:02 to 08:47:21 (139 sec)
- 11:00-12:00: 1 session, total screen time ~2 min
  - Session 11:48:22 to 11:50:31 (129 sec)
- 14:00-15:00: 1 session, total screen time ~2 min
  - Session 14:50:02 to 14:52:30 (148 sec)
- 17:00-18:00: 1 session, total screen time ~2 min
  - Session 17:33:09 to 17:35:12 (123 sec)

App usage by hour (app opens):
- 08:00-09:00: WhatsApp: 1x
- 11:00-12:00: Email: 1x
- 14:00-15:00: WhatsApp: 1x
- 17:00-18:00: Messages: 1x

Screen ON gaps by hour:
- 08:00-09:00: min gap 543s, max gap 543s, avg gap 543.0s
- 11:00-12:00: min gap 2134s, max gap 2134s, avg gap 2134.0s
- 14:00-15:00: min gap 4132s, max gap 4132s, avg gap 4132.0s
- 17:00-18:00: min gap 5342s, max gap 5342s, avg gap 5342.0s"""
