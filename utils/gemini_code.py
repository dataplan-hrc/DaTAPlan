import json
import os

import google.generativeai as genai
from .json_files.master_task import master_tasks
from .keyconfig import gemini_api

from .misc_utils import write_file
from .prompts import inp1, inp2, op1_cot, op2_cot

genai.configure(api_key=gemini_api)
cur_dir = os.path.dirname(os.path.abspath(__file__))
print(cur_dir)

user_work = 'The user has an urgent meeting' # Sentence that relates to what the user is currently performing

f = open(cur_dir+"/json_files/object_2.json", "r")
objects = json.load(f)
f.close()

f = open(cur_dir+"/json_files/receptacle.json", "r")
receptacles = json.load(f)
f.close()

f = open(cur_dir+"/json_files/task.json", "r")
task_sample_space = json.load(f)
f.close()

f = open(cur_dir+"/json_files/sequence_1.json", "r")
sequences = json.load(f)
f.close()

f = open(cur_dir+"/json_files/food.json", "r")
food = json.load(f)
f.close()

op1_nocot = """
{
    'tasks' = [
        "clean the room (kitchen)",
        "clean the room (living_room)",
        "set up the office table",
        "serve a drink"
    ],
}
"""
op2_nocot = """
{
    'tasks' = [
        "throw away leftover food"
        "prepare food",
        "serve the food",
        "prepare medicines",
    ],
}
"""


def prompt_gemini(task, dirname, icl=True, cot=True, user=1):
    if icl == False or cot == False:
        del sequences["user 1"]["description"]
        prompt = f"""
# The following tasks are possible in the household
tasks_sample_space = {master_tasks}

# The following tasks were done by **User 1** previously:
user_tasks = {sequences}

{task}
    
Answer only as a valid python dictionary, with a key: 'tasks'. Number of tasks should be 4! Keep tasks from the sample space.
"""
    else:
        prompt = f"""
# The following tasks are possible in the household
tasks_sample_space = {master_tasks}

# The following tasks were done by **User 1** previously:
user_tasks = {sequences}

{task}
    
Answer only as a valid python dictionary, with a key: 'tasks'. Number of tasks should be 4! Keep tasks from the sample space.
"""

    model = genai.GenerativeModel("gemini-1.0-pro-latest")
    if icl == True:
        if cot == True:
            convo = model.start_chat(
                history=[
                    {"role": "user", "parts": [inp1]},
                    {"role": "model", "parts": [op1_cot]},
                    {"role": "user", "parts": [inp2]},
                    {"role": "model", "parts": [op2_cot]},
                ]
            )
        elif cot == False:
            convo = model.start_chat(
                history=[
                    {"role": "user", "parts": [inp1]},
                    {"role": "model", "parts": [op1_nocot]},
                    {"role": "user", "parts": [inp2]},
                    {"role": "model", "parts": [op2_nocot]},
                ]
            )

    else:
        convo = model.start_chat(history=[])
    _ = convo.send_message(prompt)

    counter = 0
    while True:
        print(counter)
        counter += 1
        try:
            try:
                op_dict = eval(convo.last.text)
            except:
                op_string = convo.last.text
                start_index = op_string.find("{")
                end_index = op_string.rfind("}") + 1
                dict_string = op_string[start_index:end_index]
                op_dict = eval(dict_string)

            if "tasks" not in op_dict.keys():
                raise Exception("Tasks key not found in output")
            break
        except Exception as e:
            print(e)
            response = convo.send_message(
                "Please provide output only as a valid python dict. When evaluating, we get the following error: "
                + str(e)
            )

    if not os.path.exists(f"llm_cache/{dirname}"):
        os.makedirs(f"llm_cache/{dirname}")

    if icl == True:
        if cot == True:
            write_file(prompt, f"llm_cache/{dirname}/gemini_cot_prompt")
            write_file(convo.last.text, f"llm_cache/{dirname}/gemini_cot_response")
        else:
            write_file(prompt, f"llm_cache/{dirname}/gemini_icl_prompt")
            write_file(convo.last.text, f"llm_cache/{dirname}/gemini_icl_response")
    else:
        write_file(prompt, f"llm_cache/{dirname}/gemini_prompt")
        write_file(convo.last.text, f"llm_cache/{dirname}/gemini_response")

    return op_dict, convo


def main():
    match = False
    while True:
        prompt = f"""
# The following tasks are possible in the household
tasks_sample_space = {master_tasks}

# The following tasks were done by **User 1** and **User 2** previously:
user_tasks = {sequences}

You are serving **USER 1** today.
{user_work}
Anticipate the next 4 tasks for the day.
"""
        model = genai.GenerativeModel("gemini-1.0-pro-latest")
        model2 = genai.GenerativeModel("palm-2")
        convo = model.start_chat(
            history=[
                {"role": "user", "parts": [inp1]},
                {"role": "model", "parts": [op1_cot]},
                # {"role": "user", "parts": [inp2]},
                # {"role": "model", "parts": [op2_cot]},
            ]
        )
        response = convo.send_message(prompt)
        resp_dict = json.loads(convo.last.text)
        tasks_list = resp_dict.get('tasks', [])
        print("INITIAL ONE: ",convo.last.text)
        if len(tasks_list) > 4 or len(tasks_list)<4:
            feedback = "Restructure the sequence of anticipated tasks. Strictly follow the convention and create your anticipated task list of size 4, DON'T EXCEED OR SUBCEED! Provide the anticipated task list in the form of dictionary like for example"+op1_cot
            print("Feedback: ",feedback)
            response = convo.send_message(feedback)
            print("FEEDBACK CONDITION: ",convo.last.text)
        resp_dict = json.loads(convo.last.text)
        print("DICTIONARY AFTER LENGTH CHECK: ",resp_dict)
        tasks_list = resp_dict.get('tasks', [])            
        for i in range(len(tasks_list)):
            for j in range(len(master_tasks)):
                if tasks_list[i] == master_tasks[j]:
                    match = True
                    break
                else:
                    match = False
            if match == False:
                # feedback = "You anticipated tasks related to what the user performs, but the anticipated task list mentions tasks that are out of the tasks_sample_space. Hence, reidentify and restructure the sequence of anticipated tasks and also check the individual task if it relates exactly to the tasks in tasks_sample_space. Always as an output give updated chain-of-thought and tasks in a dictionary"
                feedback = "The anticipated task list includes the task '"+tasks_list[i]+"' that is out of the tasks_sample_space. Hence, correct the particular task and replace it with relevant task in the tasks_sample_space, DON'T HALLUCINATE"
                print("Feedback: ",feedback)
                response = convo.send_message(feedback)
                print("INSIDE CONDITION: ",convo.last.text)
                resp_dict = json.loads(convo.last.text)
                tasks_list = resp_dict.get('tasks', [])  
                i,j=0,0 
            match = False
        # print(resp_dict)
        print("OUTSIDE CONDITION: ",convo.last.text)
        with open(cur_dir+'/json_files/llm_tasks.json','w') as llm_tasks:
            json.dump(resp_dict,llm_tasks,indent=4)
        break
        # feedback = input("Enter feedback: ")
        # while feedback != "exit":
        #     response = convo.send_message(feedback)
        #     print(convo.last.text)
        #     feedback = input("Enter feedback: ")


if __name__ == "__main__":
    main()
