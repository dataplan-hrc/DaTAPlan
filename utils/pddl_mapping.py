######################### THIS SCRIPT IS TO MAP LLM TASKS TO PDDL GOAL STATES ###################################

import json
import os

cur_dir = os.path.dirname(os.path.abspath(__file__))

# Mapping LLM tasks to PDDL Goal states and storing it in a file for later access
def goal_mapping():
    with open(cur_dir+"/json_files/llm_tasks.json","r") as goals:
        llm_tasks = json.load(goals)
    goals.close()
    
    with open(cur_dir+"/json_files/task_goal_mapping.json","r") as mapping:
        pddl_goals = json.load(mapping)
        with open(cur_dir+"/../pddl/downward/extracted_goals.txt","w") as writing_goals:
            for i in range(len(llm_tasks['tasks'])):
                writing_goals.write(pddl_goals[llm_tasks['tasks'][i]])
                writing_goals.write(" ")
        
if __name__ == '__main__':
    goal_mapping()