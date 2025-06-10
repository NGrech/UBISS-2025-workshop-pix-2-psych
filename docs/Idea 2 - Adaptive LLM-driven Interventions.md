
> [!NOTE] **Description:**
> 
> - Uses smartphone data (screen usage, app usage, activity, location) to detect moments where an intervention may be helpful.
>     
> - LLM generates intervention messages dynamically, based on user context and past feedback.
>     
> - Reflective narrative reports summarize behavior and intervention effectiveness over time, adapting future interventions.
>     

| Dimension                     | Evaluation                                                                                                                                                                                                                               |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Feasibility**               | **Moderate**.  <br>- AWARE sensors support relevant data collection.  <br>- LLM integration is feasible (cloud or lightweight on-device). <br>- Feedback parsing + adaptive learning adds moderate complexity.                           |
| **Novelty**                   | **High**. <br>Not a lot of systems/RPs seem to implement something like this or close the loop on the feedback system. it all seems to go one way                                                                                        |
| **Data Availability**         | **Moderate**. <br>[StudentLife](https://studentlife.cs.dartmouth.edu/dataset.html), <br>[ExtraSensory](http://extrasensory.ucsd.edu), <br>[TILES](https://tiles-data.isi.edu)<br><br>feedbacks  would need to be collected or simulated. |
| **Implementation Complexity** | **High**.                                                                                                                                                                                                                                |


**High novelty**, excellent opportunity to show cutting-edge capability with manageable risk if simplified in the first version.

## Variations for novelty

### 2A. Adaptive Intervention with Feedback Dashboard

- LLM-generated interventions
- User feedback on tone/style
- Visual feedback trends (e.g. tone preferences over time)

### 2B. Predictive Feedback Loop

- Predict user tone preference before intervention
- Compare prediction vs actual feedback
- Adaptive tuning of LLM prompts

### 2C. Intervention Narrative Reports

- Weekly/daily LLM-generated narrative summaries
- Reflect on behavior and intervention effectiveness
- Suggest future improvements

---

## Additional sources from ChatGPT

### 📚 Core Source on LLM-Driven Contextual Interventions

- **MindShift: Leveraging Large Language Models for Mental‑States‑Based Problematic Smartphone Use Intervention**  
    Demonstrates LLM-based adaptive messaging triggered by real-time smartphone sensor context and user state.  
    [dl.acm.org](https://dl.acm.org/doi/10.1145/3613904.3642790)
    

---

### 📚 On-Device LLM for Contextual Personalization

- **AWARE Narrator / AutoJournaling** (Zhang et al., UbiComp 2024)  
    Uses LLMs to generate reflective summaries from smartphone sensor data — highly aligned with reflective narrative reports variation.  
    dl.acm.org
    

---

### 📚 Just-In-Time Adaptive Intervention Systems

- **Time2Stop: Adaptive and Explainable Human-AI Loop for Smartphone Overuse**  
    Adaptive trigger logic + user feedback loop + explainable AI framework — parallels proposed adaptive intervention flow.  
    [arxiv.org](https://arxiv.org/abs/2403.05584)
    

---

### 📚 LLM Personalization with User Feedback

- **Neupane et al., CHI EA 2025**  
    Study on using wearable-triggered LLM interventions with human feedback loops to improve personalization — direct parallel to Idea 2 structure.  
    dl.acm.org
    

---

### 🧭 Summary Table

|**Aspect**|**Supporting Study**|
|---|---|
|**LLM-driven contextual messaging**|_MindShift_, _AWARE Narrator_|
|**Reflective narrative reports**|_AutoJournaling_|
|**JIT adaptive intervention framework**|_Time2Stop_|
|**User feedback loop & personalization**|_Neupane et al._, _MindShift_|
|**Sensor-based behavior context**|StudentLife, ExtraSensory, TILES datasets|