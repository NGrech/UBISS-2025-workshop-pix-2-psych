import json

JSON_CONFIG_PTH = r"resources\studyConfig.json"
MAPPING = {
    "phone_usage": r"resources\phone_usage.json",
    "sleep": r"resources\sleep.json",
    "physical_activity": r"resources\physical_activity.json",
    "reach_out": r"resources\reach_out.json"
}


def insert_questions_into_json_cfg(questions, user_id, json_path=JSON_CONFIG_PTH):

    with open(JSON_CONFIG_PTH, 'r', encoding='utf-8') as f:
        study_cfg = json.load(f)

    for i, q in enumerate(questions):
        fragment = None
        with open(MAPPING[q], 'r', encoding='utf-8') as f:
            fragment = json.load(f)
            fragment['id'] = i+1

        if fragment:
            study_cfg['questions'].append(fragment)
            if questions != 'sleep':
                study_cfg['schedules'][0]["questions"].append(i+1)
            else:
                study_cfg['schedules'][1]["questions"].append(i+1)
    
    new_cfg_pth = f"resources\\user_cfg\\{user_id}_studyConfig.json"

    with open(new_cfg_pth, 'w', encoding='utf-8') as f:
        json.dump(study_cfg, f, indent=4, ensure_ascii=False)
    
    return new_cfg_pth


if __name__ == "__main__":
    # Example usage
    insert_questions_into_json_cfg(['reach_out'], 'user123',)
    print(f"Samples inserted into {JSON_CONFIG_PTH}")