import json


def main():
    with open("llm_tasks.json","r") as llm_tasks:
        anticipated_tasks = json.load(llm_tasks)
    
if __name__=='__main__':
    main()