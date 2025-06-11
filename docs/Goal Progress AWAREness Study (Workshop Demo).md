This project explores the difference between **daily goal intentions** and how users **perceive their progress** toward those goals, using a combination of:

- **Morning goal setting**
- **Passive sensor data collection**
- **ESM-based progress check-ins**
- **End-of-day reflection**
- **Automated feedback and reflection loop** using Aware Narrator + LLM processing.

The goal is to help users develop **greater self-awareness** and **adaptive self-regulation strategies** by surfacing where their perceptions and actual behaviors align or diverge.

---

## Study Flow

### Morning

- User is prompted to start their day by setting **goals**.
- For this demo, we focus on:
  - **Phone usage goals** (e.g., spend less than 1 hour on social media)
  - **Physical activity goals** (e.g., take at least 5,000 steps)

- The goal-setting prompt will also include a **link to the previous day's summary**.

### During the Day (Until ~6PM)

- Passive **sensor data collection** via AWARE:
  - App usage (time spent on social media apps, screen unlocks, etc.)
  - Physical activity data (step count, mobility patterns, etc.)
  - Location/mobility patterns if relevant.

- **Hourly ESM check-ins**:
  - One progress-related question per hour.
  - Questions will vary across the day to avoid fatigue.
  - Example question pool:
    - "Do you feel you are on track with your goal so far?" (Yes/No/Unsure)
    - "How satisfied are you with your progress today?" (1–5 Likert)
    - "Have you noticed anything making it easier or harder to stick to your goal today?" (short text)

- **Aware Narrator** runs hourly to generate structured descriptions of user activity and progress.

- Optional: if Narrator detects that a user is significantly **off track**, a **push intervention** can be sent via Pushbullet (or similar):
  - Encouragement if doing well → no intervention.
  - Gentle reminder if off track → nudge message.

### Evening (~8PM)

- **End-of-day ESM prompt**:
  - Reflection on goal progress:
    - "How successful were you today in sticking to your goal?" (0–100% slider)
    - "How happy are you with your progress today?" (0–100% slider or Likert)
    - "Anything you want to note about your experience today?" (optional text)

- **Partial report** shown to user:
  - Example: "You spent X minutes on social media today."
  - Positive message reinforcing effort.

### Next Morning (Before Goal Setting)

- Triggered process compiles the **full day summary** from the previous day:
  - All Narrator logs.
  - User goal and end-of-day self-rating.
  - Passive data summary.
  - ESM responses.

- LLM pipeline generates:
  1. **Automated analysis of goal adherence** based on data and Narrator logs.
  2. **Comparison of user’s self-rating and data-derived rating**.
  3. **Self-reflection questions** if discrepancies are detected.
  4. **Motivational message and behavior-specific feedback** based on the combined reflection.

- Morning goal-setting prompt includes **link to previous day’s feedback report**.

---

## Example Scenario

### User Goal (Morning):

*"Spend less than 1 hour on social media today."*

### During the Day:

- User receives hourly ESMs, responds positively — believes they are doing well.
- Aware data shows actual **2h15min spent on social media**.
- Narrator logs include:
  - "Prolonged usage of Instagram between 13:00–14:00"
  - "Frequent checking of Facebook between 17:00–18:00"

### End of Day:

- User rates themselves as **80% successful**.
- Narrative logs and data suggest a **clear mismatch**.

### LLM Processing:

- Determines **disagreement** between self-rating and data.
- Generates reflection prompt:
  > "You rated yourself as having done quite well today on limiting social media use. However, your data shows that you spent about 2h15min on social media apps. Can you think of any reasons why you might have perceived your progress differently?"

- Generates feedback message:
  > "You showed good focus during the morning hours. In the afternoon, social media usage increased. Try scheduling a short intentional check-in time and avoiding unplanned browsing."

### Final Reflection Cases:

| User Reflection vs Data | Action |
|-------------------------|--------|
| Both positive | Reinforce successful behavior; surface examples of success. |
| Both negative | Provide actionable tips to improve. |
| User positive, data negative | Prompt reflection, surface mismatches, suggest awareness techniques. |
| User negative, data positive | Highlight positive behaviors and encourage confidence. |

---

## Backend Processing Pipeline

### Steps:

1. **Pull data from SQL server**:
    - User goals
    - ESM responses
    - Sensor data (app usage, steps, Narrator logs)

2. **Run Aware Narrator**:
    - Hourly logs during the day.
    - Full day summary compiled at ~8PM.

3. **LLM pipeline**:

    **Step 1: Analyze adherence**
    - Inputs: user goal, end-of-day reflection, Narrator logs.
    - Output: objective rating of goal adherence (0–100%).

    **Step 2: Compare user reflection vs objective analysis**
    - Generate comparison messages and flag mismatches.

    **Step 3: Generate reflection prompts**
    - If mismatch detected, prompt user for reflection.
    - If aligned, reinforce success or provide supportive tips.

    **Step 4: Generate feedback report**
    - Combine all elements into a concise, user-friendly summary.
    - Include behavior-specific examples drawn from the data.

4. **Deliver report**:
    - Link to report in next morning's goal-setting prompt.

---

## Example LLM Prompt Templates

### For adherence analysis:

```text
Based on the following goal: "[USER GOAL]"
And the following Narrator logs: [NARRATOR LOGS]
And the following app usage data: [APP USAGE DATA]

Please provide a score from 0–100 on how well the user adhered to their goal today. Justify your score in 1–2 sentences.
```

For reflection questions (if mismatch):

```text
The user rated their goal success as [USER RATING]%.
The data analysis rated their goal success as [LLM RATING]%.

Please write 1 reflection question that helps the user think about why this difference might have occurred.
```

For behaviour feedback messages:

```text
Given the user goal, "[USER GOAL]" and activity log, write a short positive message highlighting successful behaviors the user should continue.

If the user struggled, write a supportive message suggesting 1–2 concrete strategies they could try tomorrow.
```


## To Do List
 - [ ] Research psychological scales and theories to inform ESM design.
 - [ ] Update study configuration to reflect the final flow.
 - [ ] Configure Aware Narrator for hourly runs and design push intervention logic.
 - [ ] Implement evening compilation of Narrator logs and daily summary pipeline.
	 - [ ] Define LLM prompts for each stage.
	 - [ ] Implement LLM integration and backend processing.
	 - [ ] Design frontend feedback report (simple visuals + narrative).


## References
- [23 Ways to Nudge: A Review of Technology-Mediated Nudging in Human-Computer Interaction](https://dl.acm.org/doi/pdf/10.1145/3290605.3300733)
- [AWARE Narrator and the Utilization of Large Language Models to Extract Behavioral Insights from Smartphone Sensing Data](https://arxiv.org/pdf/2411.04691v1)