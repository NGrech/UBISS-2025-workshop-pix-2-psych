> [!NOTE] **Description:**
> - Uses smartphone data (activity, GPS) to detect unhealthy behaviors (sedentary patterns, frequent visits to unhealthy locations like bars/fast food) and recommends alternative activities.
> - Tracks user follow-up and habit formation over time

| Dimension                     | Evaluation                                                                                                                                                                      |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Feasibility**               | **High**. <br>Standard smartphone sensors are supported in AWARE directly. <br>A simple dashboard visualization is can possibly be taken form an existing project and modified. |
| **Novelty**                   | **Moderate/Low**. <br>Digital wellbeing dashboards tracking activity/location are common and exist as commercial apps.                                                          |
| **Data Availability**         | **High**. <br><br>[StudentLife](https://studentlife.cs.dartmouth.edu/dataset.html), <br>[ExtraSensory](http://extrasensory.ucsd.edu)                                            |
| **Implementation Complexity** | **Moderate/low**.                                                                                                                                                               |


High implementation feasibility for within  the workshop but **low** novelty, the addition of gamification and adaptive features like real time habit support will increase that. 
## Variations for novelty 

### 1A. Contextually-Aware Habit Interventions

- Detect inactivity / unhealthy location visits
- Trigger LLM-generated interventions in context
- Simple user feedback

### 1B. Gamified Behavioral Dashboard

- Track habits: activity, location diversity
- Display streaks, badges
- Adaptive LLM motivational messages

### 1C. Reflective Behavioral Journaling

- Auto-generate daily summaries of behavior
- LLM reflective journal entries
- Promote user self-awareness

## Additional sources from ChatGPT

### 📚 Core Source on LLM-Driven Contextual Interventions

- **MindShift: Leveraging Large Language Models for Mental‑States‑Based Problematic Smartphone Use Intervention**  
    Describes a system that uses LLMs to adaptively generate context-aware motivational messages based on physical context, mental states, app usage, and user goals—closely aligned with our proposed intervention model [dl.acm.org+8dl.acm.org+8arxiv.org+8](https://dl.acm.org/doi/10.1145/3613904.3642790?utm_source=chatgpt.com)[medium.com+3catalyzex.com+3researchgate.net+3](https://www.catalyzex.com/paper/mindshift-leveraging-large-language-models?utm_source=chatgpt.com).
    

---

### 📚 Digital Behavior Change & Habit Formation

- **Digital Behavior Change Intervention Designs for Habit Formation**  
    A comprehensive survey on how mobile systems support physical activity through habit-supporting designs, including prompts and goal-setting strategies [pmc.ncbi.nlm.nih.gov+1sciencedirect.com+1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11161714/?utm_source=chatgpt.com)[arxiv.org](https://arxiv.org/abs/1702.07437?utm_source=chatgpt.com).
    
- **An Exploratory Study of Health Habit Formation Through Gamification**  
    Examines the impact of gamified app interactions (e.g. badges, challenges) on motivating healthy behavior changes—relevant to our gamified dashboard variant [pmc.ncbi.nlm.nih.gov+7arxiv.org+7sciencedirect.com+7](https://arxiv.org/abs/1708.04418?utm_source=chatgpt.com).
    

---

### 📚 Gamification Impact on Physical Activity

- **A field experiment on gamification of physical activity – Effects on motivation and perceived usefulness**  
    Explores how gamified elements like streaks and rewards improve physical activity engagement and user motivation [sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S1071581923002148?utm_source=chatgpt.com).
    
- **How Gamification Affects Physical Activity: Large‑Scale Analysis of Walking Challenges**  
    Analyzes large dataset of walking challenges, showing that competitions and challenges can boost step counts by ~23%—demonstrating strong potential for gamification mechanisms [dl.acm.org+15arxiv.org+15sciencedirect.com+15](https://arxiv.org/abs/1702.07437?utm_source=chatgpt.com).
    

---

### 📚 Smartphone Sensor-Based Activity Recognition

- **Fusion of Smartphone Motion Sensors for Physical Activity Recognition**  
    Demonstrates how smartphones’ accelerometer and gyroscope data accurately infer physical activities—a key foundation for detecting user habits [ubicomp.org+4mdpi.com+4researchgate.net+4](https://www.mdpi.com/1424-8220/14/6/10146?utm_source=chatgpt.com).
    
- **Activity Recognition Using Smartphone Sensors**  
    A research application that automatically tracks physical activities and provides feedback using smartphone sensors—supporting our core sensing pipeline [pmc.ncbi.nlm.nih.gov+4researchgate.net+4medium.com+4](https://www.researchgate.net/publication/261056239_Activity_recognition_using_smartphone_sensors?utm_source=chatgpt.com).
    

---

### 📚 Just-In-Time Adaptive Intervention Systems

- **Time2Stop: Adaptive and Explainable Human-AI Loop for Smartphone Overuse**  
    Presents a JITAI system with real-time triggers, user feedback loops, and adaptation—offering a parallel in adaptive user-facing systems [arxiv.org+1researchgate.net+1](https://arxiv.org/html/2403.05584v1?utm_source=chatgpt.com).
    

---

### 🧭 Summary Table

|**Aspect**|**Supporting Study**|
|---|---|
|**LLM-driven contextual messaging**|_MindShift_ [dl.acm.org+4dl.acm.org+4arxiv.org+4](https://dl.acm.org/doi/10.1145/3613904.3642790?utm_source=chatgpt.com)|
|**Habit-gamification theory**|_Digital Behavior Change Intervention_, _Health Habit Formation_|
|**Gamification effectiveness**|Physical activity gamification study, walking challenges|
|**Sensor-driven activity detection**|Fusion of smartphone sensors, activity recognition app|
|**Adaptive intervention design**|_Time2Stop_ JITAI system|