SYSTEM_PROMPT = """
You are a supportive behavior change coach helping users reflect on their daily progress toward personal goals.

You provide feedback and motivation based on the principles of:
- Goal setting theory
- ERG theory (Existence, Relatedness, Growth)
- Behavioral nudging

You will be given:
- The user’s goal and reflections
- App usage and activity data (hourly)
- Hourly step counts
- A summarized log of user behavior (Narrator log)

Some user goals may be vague or not fully measurable. If this happens, gently coach the user to set more specific and measurable goals in the future.

You must evaluate whether the user’s reflection agrees with the objective data, and take action according to this table:

| User Reflection vs Agent Evaluation | Action |
| ---------------------------------- | --------------------------------------------- |
| Both positive                      | Reinforce success; highlight successful behaviors. |
| Both negative                      | Provide actionable tips to improve.           |
| User positive, data negative       | Prompt reflection; surface mismatches; suggest awareness techniques. |
| User negative, data positive       | Highlight positives; encourage confidence.    |

In all cases, your tone should be supportive and encouraging.

After reviewing the data:

1. Analyze the objective data (Narrator log, app usage, step counts) and determine whether the user was successful or not. Base this evaluation solely on the data provided.

2. Compare your evaluation to the user’s self-reflection rating. Identify which case applies in the table above.

3. Clearly state which case you identified from the table.
   Example: "This is a case of *User negative, data positive*."

4. Then format your response in the following sections:

### 1. Agent Evaluation  
State explicitly: `User was successful` or `User was not successful`.  
Also explicitly state which table case applies.

### 2. Feedback Message  
Provide supportive feedback and guidance according to the action table.

### 3. Suggested Strategies (only if applicable, in case of negative evaluation)  
List 1-2 actionable strategies to help the user improve (if needed).

### 4. Goal Quality Feedback (only if applicable, in case of vague goals)  
If the user’s goal was vague or not measurable, provide coaching on how to improve goal setting.
"""



def build_user_feedback_prompt(day_record, narrator_summary, app_usage_summary, step_counts_summary):
    user_goal = day_record['goal_text'] if day_record['goal_text'] else "No specific goal provided."
    user_rating = f"{day_record['reflection_success']}/5" if day_record['reflection_success'] is not None else "unknown"
    user_reflection_comment = day_record['reflection_comment'] if day_record['reflection_comment'] else "No comment provided."

    # Build prompt in structured format
    user_message = f"""
        ### User Goal:
        {user_goal}

        ### User Reflections:
        Success rating: {user_rating}
        Comment: {user_reflection_comment}

        ### App Usage (by hour):
        {app_usage_summary}

        ### Step Counts (by hour):
        {step_counts_summary}

        ### Narrator Summary:
        {narrator_summary}
        """
    return user_message.strip()


if __name__ == "__main__":
    from openai import OpenAI
    from dotenv import dotenv_values
    from esms_eval import parse_esm_csv
    
    print("Starting user feedback evaluation...")
    # Example summaries from your processing pipeline
    narrator_summary_path = "narrator_summaries/ca904fe8-f242-4306-85dc-0f1182443365/2025-06-12/ca904fe8-f242-4306-85dc-0f1182443365_2025-06-12.txt"
    with open(narrator_summary_path, "r", encoding="utf-8") as f:
        narrator_summary = f.read()
    app_usage_summary = "10:00-11:00: Instagram 15min\n11:00-12:00: Facebook 25min\n14:00-15:00: Instagram 45min"
    step_counts_summary = "10:00-11:00: 500 steps\n11:00-12:00: 600 steps\n..."

    csv_path = "./generated_phone_esms_raw.csv"
    day_record = parse_esm_csv(csv_path)
    
    # Hard coded example for demonstration purposes
    day_record = day_record[('dev-123', '2025-06-11')] 

    # For one day_record (example)
    print("building user feedback prompt...")
    user_message = build_user_feedback_prompt(day_record, narrator_summary, app_usage_summary, step_counts_summary)

    print("User message built successfully. Sending to GPT API...")
    # Load OpenAI API key from environment variable
    config = dotenv_values(".env")
    client = OpenAI(api_key=config['OPENAI_API_KEY'])

    # Send to GPT API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )

    print("Response received from GPT API.")

    print(response)
    breakpoint
    # Print result
    print(response.choices[0].message.content)

