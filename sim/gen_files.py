from re import split
import random
import os

directory = os.path.dirname(os.path.abspath(__file__))
pddl_struct_data=[]

# Reading the text file generated from pddl and using it as the list of tasks
def read():
    with open(directory+"/../loc.txt","r") as location:
        agent_human_init = location.readlines()
    files = directory+"/../pddl/"+agent_human_init[0]+"/"
    sorted_files = sorted(os.listdir(files))    
    pddl_file = open(files+sorted_files[-1],"r")
    pddl_op = pddl_file.readlines()
    for i in range(len(pddl_op)):
        sp = pddl_op[i].split('(')
        sp1 = sp[1].split(')') 
        parse = split("\W+",sp1[0])
        pddl_struct_data.append(parse)
    write(pddl_op)

def write(pddl_op):
    human_file = open(directory+"/human_tasks.txt","w")
    agent_file = open(directory+"/agent_tasks.txt","w")
    for i in range(len(pddl_struct_data)):
        sp = pddl_struct_data[i][0].split('_')
        if sp[0] == 'human':
            human_file.write(pddl_op[i])
        elif sp[0] == 'agent':
            agent_file.write(pddl_op[i])
    human_file.close()
    agent_file.close()

if __name__ == "__main__":
    read()