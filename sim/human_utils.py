
import sim

def cook_feedback():
    from human_agent import clientID
    cook_feedback = sim.simxGetInt32Signal(clientID,'cook_feedback',sim.simx_opmode_blocking)
    return cook_feedback

def roburner_state():
    from robot_agent import roboclientID
    robo_burner_state1 = sim.simxGetInt32Signal(roboclientID,'burner_state1',sim.simx_opmode_blocking)
    robo_burner_state2 = sim.simxGetInt32Signal(roboclientID,'burner_state2',sim.simx_opmode_blocking)
    robo_burner_state3 = sim.simxGetInt32Signal(roboclientID,'burner_state3',sim.simx_opmode_blocking)
    robo_burner_state4 = sim.simxGetInt32Signal(roboclientID,'burner_state4',sim.simx_opmode_blocking)
    return robo_burner_state1,robo_burner_state2,robo_burner_state3,robo_burner_state4

def burner_state():
    from human_agent import clientID
    burner_state1 = sim.simxGetInt32Signal(clientID,'burner_state1',sim.simx_opmode_blocking)
    burner_state2 = sim.simxGetInt32Signal(clientID,'burner_state2',sim.simx_opmode_blocking)
    burner_state3 = sim.simxGetInt32Signal(clientID,'burner_state3',sim.simx_opmode_blocking)
    burner_state4 = sim.simxGetInt32Signal(clientID,'burner_state4',sim.simx_opmode_blocking)
    return burner_state1,burner_state2,burner_state3,burner_state4

def putdown_obj():
    from robot_agent import roboclientID
    putdown_cook_obj_pan = sim.simxGetInt32Signal(roboclientID,'cookable_obj_putdown_pan',sim.simx_opmode_blocking)
    putdown_cook_obj_metal_pot = sim.simxGetInt32Signal(roboclientID,'cookable_obj_putdown_metal_pot',sim.simx_opmode_blocking)
    return putdown_cook_obj_pan,putdown_cook_obj_metal_pot 