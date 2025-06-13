# run_eval.py

from openai import OpenAI
from dotenv import dotenv_values
from prompt import SYSTEM_PROMPT, build_user_feedback_prompt
import data_simulation as ds
import time

# Load OpenAI API key from .env
config = dotenv_values(".env")
client = OpenAI(api_key=config['OPENAI_API_KEY'])

# Define test cases
TEST_CASES = [
    {
        "name": "Both Positive",
        "day_record_fn": ds.good_daily_record,
        "narrator_fn": ds.narrator_summary_full_day_positive,
        "app_usage_fn": ds.low_app_usage_summary,
        "step_counts_fn": ds.high_step_count_summary
    },
    {
        "name": "Both Negative",
        "day_record_fn": ds.bad_daily_record,
        "narrator_fn": ds.narrator_summary_full_day_negative,
        "app_usage_fn": ds.high_app_usage_summary,
        "step_counts_fn": ds.low_step_count_summary
    },
    {
        "name": "User Positive, Data Negative",
        "day_record_fn": ds.good_daily_record,
        "narrator_fn": ds.narrator_summary_full_day_negative,
        "app_usage_fn": ds.high_app_usage_summary,
        "step_counts_fn": ds.low_step_count_summary
    },
    {
        "name": "User Negative, Data Positive",
        "day_record_fn": ds.bad_daily_record,
        "narrator_fn": ds.narrator_summary_full_day_positive,
        "app_usage_fn": ds.low_app_usage_summary,
        "step_counts_fn": ds.high_step_count_summary
    }
]

def run_test_case(case):
    print(f"\n--- Running Test Case: {case['name']} ---")

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

    # save to file
    filename = f"logs/test_result_{case['name'].replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"=== Test Case: {case['name']} ===\n\n")
        f.write("=== User Message ===\n\n")
        f.write(user_message + "\n\n")
        f.write("=== GPT Response ===\n\n")
        f.write(reply)

    print(f"Result saved to {filename}\n")

if __name__ == "__main__":
    print("Starting evaluation of test cases...\n")

    for case in TEST_CASES:
        run_test_case(case)
        # Small delay between calls to avoid hitting rate limits
        time.sleep(1)

    print("\nEvaluation complete. Results saved to 'logs/' folder.")
