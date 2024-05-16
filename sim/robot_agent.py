import sim 
import sys
import numpy as np
import cv2
import os
import time
from re import split
from human_utils import cook_feedback

# Initialization
robo_pddl_struct_data=[]
roboaction = []
robolocation1 = []
robolocation2 = []
roboobj =[]
roboobjchanged =[]
roboreceptacle=[]
roboimmobilereceptacle1=[]
roboimmobilereceptacle2=[]
robo_burner_state = ""
roboclientID=0
directory = os.path.dirname(os.path.abspath(__file__))

# Starting API Connection for robot agent
def robo_sim_start():
    global roboclientID
    sim.simxFinish(-1)

    roboclientID = sim.simxStart('127.0.0.1',19991,True,True,5000,5)

    if roboclientID!= -1:
        print("Connected to ROBOT Remote API Server")
    else:
        print("Connection failed")
        sys.exit('Could not reconnect')
        
# Decomposing different robot actions from PDDL plan outcome
def robo_read():
    global roboclientID
    robo_pddl_file = open(directory+"/agent_tasks.txt","r")
    robo_pddl_op = robo_pddl_file.readlines()
    for i in range(len(robo_pddl_op)):
        robo_sp = robo_pddl_op[i].split('(')
        robo_sp1 = robo_sp[1].split(')') 
        robo_parse = split("\W+",robo_sp1[0])
            
        robo_pddl_struct_data.append(robo_parse)
    for i in range(len(robo_pddl_struct_data)):
        robo_act = robo_pddl_struct_data[i][0].split('_')
        if robo_act[1] == "moves":
            roboobj.append('')
            roboobjchanged.append('')
            roboreceptacle.append('')
            roboimmobilereceptacle1.append(robo_pddl_struct_data[i][1])
            roboimmobilereceptacle2.append(robo_pddl_struct_data[i][2])
            robolocation1.append(robo_pddl_struct_data[i][3])
            robolocation2.append(robo_pddl_struct_data[i][4])
        elif robo_act[1] == "picks" or robo_act[1] == "pickup":
            roboobj.append(robo_pddl_struct_data[i][1])
            roboobjchanged.append('')
            roboreceptacle.append('')
            roboimmobilereceptacle1.append(robo_pddl_struct_data[i][2])
            roboimmobilereceptacle2.append('')
            robolocation1.append(robo_pddl_struct_data[i][3])
            robolocation2.append('')
        elif robo_act[1] == "picksup":
            roboobj.append('')
            roboobjchanged.append('')
            roboreceptacle.append(robo_pddl_struct_data[i][1])
            roboimmobilereceptacle1.append(robo_pddl_struct_data[i][2])
            roboimmobilereceptacle2.append('')
            robolocation1.append(robo_pddl_struct_data[i][3])
            robolocation2.append('')
        elif robo_act[1] == "putdown":
            roboobj.append(robo_pddl_struct_data[i][1])
            roboobjchanged.append('')
            roboreceptacle.append(robo_pddl_struct_data[i][2])
            roboimmobilereceptacle1.append(robo_pddl_struct_data[i][3])
            roboimmobilereceptacle2.append('')
            robolocation1.append(robo_pddl_struct_data[i][4])
            robolocation2.append('')
        elif robo_act[1] == "putsdown":
            roboobj.append('')
            roboobjchanged.append('')
            roboreceptacle.append(robo_pddl_struct_data[i][1])
            roboimmobilereceptacle1.append(robo_pddl_struct_data[i][2])
            roboimmobilereceptacle2.append('')
            robolocation1.append(robo_pddl_struct_data[i][3])
            robolocation2.append('')
        elif robo_act[1] == "switcheson":
            roboobj.append(robo_pddl_struct_data[i][1])
            roboobjchanged.append('')
            roboreceptacle.append('')
            roboimmobilereceptacle1.append(robo_pddl_struct_data[i][2])
            roboimmobilereceptacle2.append('')
            robolocation1.append(robo_pddl_struct_data[i][3])
            robolocation2.append('')
        elif robo_act[1] == "putdowns":
            roboobj.append(robo_pddl_struct_data[i][1])
            roboobjchanged.append('')
            roboreceptacle.append('')
            roboimmobilereceptacle1.append(robo_pddl_struct_data[i][2])
            roboimmobilereceptacle2.append('')
            robolocation1.append(robo_pddl_struct_data[i][3])
            robolocation2.append('')
        elif robo_act[1] == "switcheson":
            roboobj.append(robo_pddl_struct_data[i][1])
            roboobjchanged.append('')
            roboreceptacle.append(robo_pddl_struct_data[i][2])
            roboimmobilereceptacle1.append(robo_pddl_struct_data[i][3])
            roboimmobilereceptacle2.append('')
            robolocation1.append('')
            robolocation2.append('')
        elif robo_act[1] == "boils" or robo_act[1] == "cooks":
            roboobj.append(robo_pddl_struct_data[i][1])
            roboobjchanged.append(robo_pddl_struct_data[i][2])
            roboreceptacle.append('')
            roboimmobilereceptacle1.append('')
            roboimmobilereceptacle2.append('')
            robolocation1.append('')
            robolocation2.append('')
        elif robo_act[1] == "cleans":
            roboobj.append('')
            roboobjchanged.append('')
            roboreceptacle.append('')
            roboimmobilereceptacle1.append(robo_pddl_struct_data[i][1])
            roboimmobilereceptacle2.append('')
            robolocation1.append(robo_pddl_struct_data[i][2])
            robolocation2.append('')
        roboaction.append(robo_act[1])
        
# Sending all the action, state parameters to the simulation environment
def robo_data(i):
    sim.simxSetStringSignal(roboclientID,"robot_action", roboaction[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(roboclientID,"robot_objects", roboobj[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(roboclientID,"robot_objects_changed", roboobjchanged[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(roboclientID,"robot_receptacle", roboreceptacle[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(roboclientID,"robot_immobilereceptacle1", roboimmobilereceptacle1[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(roboclientID,"robot_immobilereceptacle2", roboimmobilereceptacle2[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(roboclientID,"robot_location1", robolocation1[i],sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(roboclientID,"robot_location2", robolocation2[i],sim.simx_opmode_oneshot)
    with open(directory+"/shared_variable.txt", "r") as file:
        shared_variable = file.read()
    sim.simxSetStringSignal(roboclientID,"collision", shared_variable,sim.simx_opmode_oneshot)

# Updating the action once completed
def robo_perform():
    global roboclientID
    global cook_feedback, roburner_state, putdown_obj, cook_obj, rbs
    rbs,i=0,0
    sim.simxClearInt32Signal(roboclientID,"robot_feedback",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(roboclientID,"robot_action",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(roboclientID,"robot_objects",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(roboclientID,"robot_objects_changed",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(roboclientID,"robot_receptacle",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(roboclientID,"robot_immobilereceptacle1",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(roboclientID,"robot_immobilereceptacle2",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(roboclientID,"robot_location1",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(roboclientID,"robot_location2",sim.simx_opmode_oneshot)
    sim.simxClearStringSignal(roboclientID,"collision",sim.simx_opmode_oneshot)
    while i<len(robo_pddl_struct_data):        
        cook_feed = cook_feedback()
        if cook_feed[1] ==1 and roboaction[i] == 'pickup' and roboreceptacle[i] == 'pan':
            sim.simxSetInt32Signal(roboclientID,'cook_feedback',cook_feed[1],sim.simx_opmode_oneshot)
        elif cook_feed[1] ==0 and roboaction[i] == 'pickup' and roboreceptacle[i] == 'pan':
            continue
        robo_data(i)
        robofeedback = sim.simxGetInt32Signal(roboclientID,'robot_feedback',sim.simx_opmode_blocking)
        
        if robofeedback[1] == 1:
            i = i+1
            sim.simxClearInt32Signal(roboclientID,"robot_feedback",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(roboclientID,"robot_action",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(roboclientID,"robot_objects",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(roboclientID,"robot_objects_changed",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(roboclientID,"robot_receptacle",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(roboclientID,"robot_immobilereceptacle1",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(roboclientID,"robot_immobilereceptacle2",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(roboclientID,"robot_location1",sim.simx_opmode_oneshot)
            sim.simxClearStringSignal(roboclientID,"robot_location2",sim.simx_opmode_oneshot)
            
        else:
            continue       
        
if __name__ == "__main__":
    robo_sim_start()
    robo_read()
    robo_perform()
