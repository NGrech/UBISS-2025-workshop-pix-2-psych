# run_eval_multiday.py

from openai import OpenAI
from dotenv import dotenv_values
from prompt import SYSTEM_PROMPT, build_user_feedback_prompt
import data_simulation as ds
import time
import os

# Load OpenAI API key from .env
config = dotenv_values(".env")
client = OpenAI(api_key=config['OPENAI_API_KEY'])

# Make sure logs directory exists
os.makedirs("logs", exist_ok=True)

# Define multi-day test cases
MULTIDAY_TEST_CASES = [
    # User 1 - good day
    {
        "name": "User1_Day1_Good",
        "day_record_fn": ds.good_daily_record,
        "narrator_fn": ds.narrator_summary_full_day_positive,
        "app_usage_fn": ds.low_app_usage_summary,
        "step_counts_fn": ds.high_step_count_summary
    },
    # User 1 - bad day
    {
        "name": "User1_Day2_Bad",
        "day_record_fn": ds.bad_daily_record,
        "narrator_fn": ds.narrator_summary_full_day_negative,
        "app_usage_fn": ds.high_app_usage_summary,
        "step_counts_fn": ds.low_step_count_summary
    },
    # User 2 - good day 1
    {
        "name": "User2_Day1_Good",
        "day_record_fn": ds.good_daily_record,
        "narrator_fn": ds.narrator_summary_full_day_positive,
        "app_usage_fn": ds.low_app_usage_summary,
        "step_counts_fn": ds.high_step_count_summary
    },
    # User 2 - good day 2
    {
        "name": "User2_Day2_Good",
        "day_record_fn": ds.good_daily_record,
        "narrator_fn": ds.narrator_summary_full_day_positive,
        "app_usage_fn": ds.low_app_usage_summary,
        "step_counts_fn": ds.high_step_count_summary
    }
]

def run_test_case(case):
    print(f"\n--- Running Multi-Day Test Case: {case['name']} ---")

    day_record = case['day_record_fn']()
    narrator_summary = case['narrator_fn']()
    app_usage_summary = case['app_usage_fn']()
    step_counts_summary = case['step_counts_fn']()

    user_message = build_user_feedback_prompt(
        day_record,
        narrator_summary,
        app_usage_summary,
        step_counts_summary
    )

    # Send to GPT
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )

    # Print and log result
    reply = response.choices[0].message.content
    print(reply)

    # Save to log file
    filename = f"logs/test_result_multiday_{case['name']}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"=== Multi-Day Test Case: {case['name']} ===\n\n")
        f.write("=== User Message ===\n\n")
        f.write(user_message + "\n\n")
        f.write("=== GPT Response ===\n\n")
        f.write(reply)

    print(f"Result saved to {filename}\n")

if __name__ == "__main__":
    print("Starting multi-day evaluation...\n")

    for case in MULTIDAY_TEST_CASES:
        run_test_case(case)
        # Small delay between calls to avoid hitting rate limits
        time.sleep(1)

    print("\nMulti-day evaluation complete. Results saved to 'logs/' folder.")
