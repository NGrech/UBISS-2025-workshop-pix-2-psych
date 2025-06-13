from datetime import datetime
import re
import glob
import os

def generate_html_report(parsed_agent_response, day_record, step_counts_summary, app_usage_summary, narrator_summary, group="Group 6", output_path="daily_feedback_report.html"):
    # Load template
    with open("src/agent_report_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    # Fill in placeholders
    filled = template.replace("{{date}}", datetime.today().strftime("%Y-%m-%d"))
    filled = filled.replace("{{group}}", group)
    filled = filled.replace("{{goal_text}}", day_record.get("goal_text", "N/A"))
    filled = filled.replace("{{reflection_success}}", str(day_record.get("reflection_success", "N/A")))
    filled = filled.replace("{{reflection_comment}}", day_record.get("reflection_comment", "N/A"))

    filled = filled.replace("{{agent_evaluation}}", parsed_agent_response.get("agent_evaluation", "N/A"))
    filled = filled.replace("{{case_identified}}", parsed_agent_response.get("case_identified", "N/A"))
    filled = filled.replace("{{feedback_message}}", parsed_agent_response.get("feedback_message", "N/A"))
    filled = filled.replace("{{suggested_strategies}}", parsed_agent_response.get("suggested_strategies", "N/A"))
    filled = filled.replace("{{goal_quality_feedback}}", parsed_agent_response.get("goal_quality_feedback", "N/A"))

    filled = filled.replace("{{step_counts_summary}}", step_counts_summary)
    filled = filled.replace("{{app_usage_summary}}", app_usage_summary)
    filled = filled.replace("{{narrator_summary}}", narrator_summary)

    # Write to output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(filled)

    print(f"HTML report generated: {output_path}")


def parse_test_result_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split User Message and GPT Response
    user_msg_match = re.search(r"=== User Message ===\n\n(.*?)\n=== GPT Response ===", content, re.DOTALL)
    gpt_resp_match = re.search(r"=== GPT Response ===\n\n(.*)", content, re.DOTALL)

    user_msg = user_msg_match.group(1) if user_msg_match else ""
    gpt_resp = gpt_resp_match.group(1) if gpt_resp_match else ""

    # Parse User Message
    goal_text = re.search(r"### User Goal:\s*(.*?)\n\s*###", user_msg, re.DOTALL)
    reflection_rating = re.search(r"Success rating:\s*(\d+)/5", user_msg)
    reflection_comment = re.search(r"Comment:\s*(.*?)\n\s*###", user_msg, re.DOTALL)
    app_usage_summary = re.search(r"### App Usage \(by hour\):\s*(.*?)\n\s*###", user_msg, re.DOTALL)
    step_counts_summary = re.search(r"### Step Counts \(by hour\):\s*(.*?)\n\s*###", user_msg, re.DOTALL)
    narrator_summary = re.search(r"### Narrator Summary:\s*(.*)", user_msg, re.DOTALL)

    # Parse GPT Response sections
    agent_eval_block = re.search(r"### 1\. Agent Evaluation\s*(.*?)\n###", gpt_resp, re.DOTALL)
    feedback_message_block = re.search(r"### 2\. Feedback Message\s*(.*?)\n###", gpt_resp, re.DOTALL)
    suggested_strategies_block = re.search(r"### 3\. Suggested Strategies\s*(.*?)\n(?:###|$)", gpt_resp, re.DOTALL)
    goal_quality_feedback_block = re.search(r"### 4\. Goal Quality Feedback\s*(.*?)\n(?:###|$)", gpt_resp, re.DOTALL)

    # Extract Agent Evaluation and Case Identified separately
    agent_eval_text = agent_eval_block.group(1).strip() if agent_eval_block else ""
    agent_eval_match = re.search(r"(User was successful|User was not successful)", agent_eval_text)
    case_identified_match = re.search(r"This is a case of \*(.*?)\*", agent_eval_text)

    # Return as dict
    return {
        "goal_text": goal_text.group(1).strip() if goal_text else "",
        "reflection_success": reflection_rating.group(1).strip() if reflection_rating else "",
        "reflection_comment": reflection_comment.group(1).strip() if reflection_comment else "",
        "app_usage_summary": app_usage_summary.group(1).strip() if app_usage_summary else "",
        "step_counts_summary": step_counts_summary.group(1).strip() if step_counts_summary else "",
        "narrator_summary": narrator_summary.group(1).strip() if narrator_summary else "",

        "agent_evaluation": agent_eval_match.group(1) if agent_eval_match else "",
        "case_identified": case_identified_match.group(1) if case_identified_match else "",
        "feedback_message": feedback_message_block.group(1).strip() if feedback_message_block else "",
        "suggested_strategies": suggested_strategies_block.group(1).strip() if suggested_strategies_block else "",
        "goal_quality_feedback": goal_quality_feedback_block.group(1).strip() if goal_quality_feedback_block else ""
    }


import glob
import os

if __name__ == "__main__":
    # Get all test_result_*.txt files in logs/
    test_files = glob.glob("logs/test_result_*.txt")

    print(f"Found {len(test_files)} test result files.")

    for test_file in test_files:
        print(f"\nProcessing {test_file} ...")
        parsed_data = parse_test_result_file(test_file)

        # Determine output HTML filename
        html_filename = test_file.replace(".txt", ".html")

        # Generate HTML report
        generate_html_report(
            parsed_agent_response={
                "agent_evaluation": parsed_data["agent_evaluation"],
                "case_identified": parsed_data["case_identified"],
                "feedback_message": parsed_data["feedback_message"],
                "suggested_strategies": parsed_data["suggested_strategies"],
                "goal_quality_feedback": parsed_data["goal_quality_feedback"]
            },
            day_record={
                "goal_text": parsed_data["goal_text"],
                "reflection_success": parsed_data["reflection_success"],
                "reflection_comment": parsed_data["reflection_comment"]
            },
            step_counts_summary=parsed_data["step_counts_summary"],
            app_usage_summary=parsed_data["app_usage_summary"],
            narrator_summary=parsed_data["narrator_summary"],
            output_path=html_filename
        )

        print(f"Generated HTML: {html_filename}")

    print("\nDone! All HTML reports generated.")
