import sim 
import sys
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
import os
from re import split
from human_utils import cook_feedback, roburner_state, putdown_obj, burner_state

# Initialization
pddl_struct_data=[]
action = []
obj =[]
objchanged =[]
receptacle=[]
immobilereceptacle1=[]
immobilereceptacle2=[]
location1=[]
location2=[]
clientID = 0
directory = os.path.dirname(os.path.abspath(__file__))

# Starting the Remote API of Simulation and connecting to the human agent
def sim_start():
    global clientID
    sim.simxFinish(-1)

    clientID = sim.simxStart('127.0.0.1',19990,True,True,5000,5)
    if clientID!= -1:
        print("Connected to HUMAN Remote API Server")
    else:
        print("Connection failed")
        sys.exit('Could not reconnect')
    
# Decomposing PDDL actions for simulation
def read():
    global clientID
    pddl_file = open(directory+"/human_tasks.txt","r")
    pddl_op = pddl_file.readlines()
    for i in range(len(pddl_op)):
        sp = pddl_op[i].split('(')
        sp1 = sp[1].split(')') 
        parse = split("\W+",sp1[0])
        pddl_struct_data.append(parse)
    for i in range(len(pddl_struct_data)):
        act = pddl_struct_data[i][0].split('_')
        if act[1] == "moves":
            obj.append('')
            objchanged.append('')
            receptacle.append('')
            immobilereceptacle1.append(pddl_struct_data[i][1])
            immobilereceptacle2.append(pddl_struct_data[i][2])
            location1.append(pddl_struct_data[i][3])
            location2.append(pddl_struct_data[i][4])
        elif act[1] == "picks":
            obj.append(pddl_struct_data[i][1])
            objchanged.append('')
            receptacle.append('')
            immobilereceptacle1.append(pddl_struct_data[i][2])
            immobilereceptacle2.append('')
            location1.append(pddl_struct_data[i][3])
            location2.append('')
        elif act[1] == "picksup" and act[2]=="freceptacle":
            obj.append('')
            objchanged.append('')
            receptacle.append(pddl_struct_data[i][1])
            immobilereceptacle1.append(pddl_struct_data[i][2])
            immobilereceptacle2.append('')
            location1.append(pddl_struct_data[i][3])
            location2.append('')
        elif act[1] == "picksup" and act[2]=="object":
            obj.append('')
            objchanged.append('')
            receptacle.append(pddl_struct_data[i][1])
            immobilereceptacle1.append(pddl_struct_data[i][2])
            immobilereceptacle2.append('')
            location1.append('')
            location2.append('')
        elif act[1] == "putdown":
            obj.append(pddl_struct_data[i][1])
            objchanged.append('')
            receptacle.append(pddl_struct_data[i][2])
            immobilereceptacle1.append(pddl_struct_data[i][3])
            immobilereceptacle2.append('')
            location1.append(pddl_struct_data[i][4])
            location2.append('')
        elif act[1] == "switcheson":
            obj.append(pddl_struct_data[i][1])
            objchanged.append('')
            receptacle.append('')
            immobilereceptacle1.append(pddl_struct_data[i][2])
            immobilereceptacle2.append('')
            location1.append(pddl_struct_data[i][3])
            location2.append('')
        elif act[1] == "putdowns":
            obj.append(pddl_struct_data[i][1])
            objchanged.append('')
            receptacle.append('')
            immobilereceptacle1.append(pddl_struct_data[i][2])
            immobilereceptacle2.append('')
            location1.append(pddl_struct_data[i][3])
            location2.append('')
        elif  act[1] == "putsdown" and act[2]=="freceptacle":
            obj.append('')
            objchanged.append('')
            receptacle.append(pddl_struct_data[i][1])
            immobilereceptacle1.append(pddl_struct_data[i][2])
            immobilereceptacle2.append('')
            location1.append(pddl_struct_data[i][3])
            location2.append('')
        elif  act[1] == "putsdown" and act[2]=="object":
            obj.append('')
            objchanged.append('')
            receptacle.append(pddl_struct_data[i][1])
            immobilereceptacle1.append(pddl_struct_data[i][2])
            immobilereceptacle2.append('')
            location1.append('')
            location2.append('')
        elif act[1] == "switcheson":
            obj.append(pddl_struct_data[i][1])
            objchanged.append('')
            receptacle.append(pddl_struct_data[i][2])
            immobilereceptacle1.append(pddl_struct_data[i][3])
            immobilereceptacle2.append('')
            location1.append('')
            location2.append('')
        elif act[1] == "boils" or act[1] == "cooks":
            obj.append(pddl_struct_data[i][1])
            objchanged.append(pddl_struct_data[i][2])
            receptacle.append('')
            immobilereceptacle1.append('')
            immobilereceptacle2.append('')
            location1.append('')
            location2.append('')        
        elif act[1] == "cleans":
            obj.append('')
            objchanged.append('')
            receptacle.append('')
            immobilereceptacle1.append(pddl_struct_data[i][1])
            immobilereceptacle2.append('')
            location1.append(pddl_struct_data[i][2])
            location2.append('')        
        action.append(act[1])

# Sending all the action, state parameters to the simulation environment
def data(i):
    global clientID
    sim.simxSetStringSignal(clientID,"action", action[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(clientID,"objects", obj[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(clientID,"changed_objects", objchanged[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(clientID,"receptacle", receptacle[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(clientID,"immobilereceptacle1", immobilereceptacle1[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(clientID,"immobilereceptacle2", immobilereceptacle2[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(clientID,"location1", location1[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(clientID,"location2", location2[i],sim.simx_opmode_oneshot)

# Updating the action once completed
def perform():
    global clientID
    global cook_feedback, roburner_state, putdown_obj
    i=0
    sim.simxClearInt32Signal(clientID,"feedback",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(clientID,"action",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(clientID,"objects",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(clientID,"changed_objects",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(clientID,"receptacle",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(clientID,"immobilereceptacle1",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(clientID,"immobilereceptacle2",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(clientID,"location1",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(clientID,"location2",sim.simx_opmode_oneshot)
    while i<len(pddl_struct_data):       
        rbs1,rbs2,rbs3,rbs4 = roburner_state()             
        hbs1,hbs2,hbs3,hbs4 = burner_state()             
        cook_obj_pan,cook_obj_pot = putdown_obj()
        if action[i] == 'cooks' and ((rbs1==1 or hbs1==1 ) and (cook_obj_pan==1 or cook_obj_pot==1 )):
            sim.simxSetInt32Signal(clientID,'burner_state1',rbs1,sim.simx_opmode_oneshot)
            if cook_obj_pot == 1:
                sim.simxSetInt32Signal(clientID,'cookable_obj_putdown_metal_pot',cook_obj_pot,sim.simx_opmode_oneshot)
            else:
                sim.simxSetInt32Signal(clientID,'cookable_obj_putdown_pan',cook_obj_pan,sim.simx_opmode_oneshot)
        elif action[i] == 'cooks' and ((rbs2==1 or hbs2==1 ) and (cook_obj_pan==1 or cook_obj_pot==1 ) ):
            sim.simxSetInt32Signal(clientID,'burner_state2',rbs2,sim.simx_opmode_oneshot)
            if cook_obj_pot == 1:
                sim.simxSetInt32Signal(clientID,'cookable_obj_putdown_metal_pot',cook_obj_pot,sim.simx_opmode_oneshot)
            else:
                sim.simxSetInt32Signal(clientID,'cookable_obj_putdown_pan',cook_obj_pan,sim.simx_opmode_oneshot)
        elif action[i] == 'cooks' and ((rbs3==1 or hbs3==1 ) and (cook_obj_pan==1 or cook_obj_pot==1 ) ):
            sim.simxSetInt32Signal(clientID,'burner_state3',rbs3,sim.simx_opmode_oneshot)
            if cook_obj_pot == 1:
                sim.simxSetInt32Signal(clientID,'cookable_obj_putdown_metal_pot',cook_obj_pot,sim.simx_opmode_oneshot)
            else:
                sim.simxSetInt32Signal(clientID,'cookable_obj_putdown_pan',cook_obj_pan,sim.simx_opmode_oneshot)
        elif action[i] == 'cooks' and ((rbs4==1 or hbs4==1 ) and (cook_obj_pan==1 or cook_obj_pot==1 ) ):
            sim.simxSetInt32Signal(clientID,'burner_state4',rbs4,sim.simx_opmode_oneshot)
            if cook_obj_pot == 1:
                sim.simxSetInt32Signal(clientID,'cookable_obj_putdown_metal_pot',cook_obj_pot,sim.simx_opmode_oneshot)
            else:
                sim.simxSetInt32Signal(clientID,'cookable_obj_putdown_pan',cook_obj_pan,sim.simx_opmode_oneshot)
        elif action[i] == 'cooks' and ((rbs1==0 and hbs1 == 0) or (cook_obj_pan==0 or cook_obj_pot==0 )):
            continue
        elif action[i] == 'cooks' and ((rbs2==0 and hbs2 == 0) or (cook_obj_pan==0 or cook_obj_pot==0 )):
            continue
        elif action[i] == 'cooks' and ((rbs3==0 and hbs3 == 0) or (cook_obj_pan==0 or cook_obj_pot==0 )):
            continue
        elif action[i] == 'cooks' and ((rbs4==0 and hbs4 == 0) or (cook_obj_pan==0 or cook_obj_pot==0 )):
            continue
        data(i)
        feedback = sim.simxGetInt32Signal(clientID,'feedback',sim.simx_opmode_blocking)

        cook_feed = cook_feedback()
        if feedback[1] == 1:
            i = i+1
            sim.simxClearInt32Signal(clientID,"feedback",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(clientID,"action",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(clientID,"objects",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(clientID,"changed_objects",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(clientID,"receptacle",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(clientID,"immobilereceptacle1",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(clientID,"immobilereceptacle2",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(clientID,"location1",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(clientID,"location2",sim.simx_opmode_oneshot)
            
        else:
            continue

if __name__ == '__main__': 
    sim_start()
    read()
    perform()
