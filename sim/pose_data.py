import sim
import time
import threading

human_position, human_orientation, robot_position, robot_orientation = [], [], [], []
update_lock = threading.Lock()
exit_flag = False

def connection():
    global human_position, human_orientation, robot_position, robot_orientation, update_lock, exit_flag
    posedataID = sim.simxStart('127.0.0.1', 19993, True, True, 5000, 5)

    if posedataID != -1:
        print("Connected to remote API server")
    else:
        print("Connection failed")
        
    return posedataID
        
def update_pose(posedataID):

    # Get the handle of the object whose pose you want to track
    _, human_handle = sim.simxGetObjectHandle(posedataID, './human', sim.simx_opmode_blocking)
    _, robot_handle = sim.simxGetObjectHandle(posedataID, './robot', sim.simx_opmode_blocking)

    if human_handle != -1 and robot_handle != -1:
        # Get the object's pose (position and orientation)
        _, human_position = sim.simxGetObjectPosition(posedataID, human_handle, -1, sim.simx_opmode_streaming)
        _, human_orientation = sim.simxGetObjectOrientation(posedataID, human_handle, -1, sim.simx_opmode_streaming)
        _, robot_position = sim.simxGetObjectPosition(posedataID, robot_handle, -1, sim.simx_opmode_streaming)
        _, robot_orientation = sim.simxGetObjectOrientation(posedataID, robot_handle, -1, sim.simx_opmode_streaming)

        time.sleep(0.5) 

    else:
        print("Failed to retrieve object handle")
        
    return human_position, human_orientation, robot_position, robot_orientation
        


if __name__ == '__main__':
    poseID = connection()
    while sim.simxGetConnectionId(poseID) != -1:
        update_pose()