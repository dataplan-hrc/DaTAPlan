import sim 
import sys
import numpy as np
import cv2
import time
import math
import matplotlib.pyplot as plt
from re import split
from pose_data import update_pose, connection
from shared_point import stop

# Initialization
pddl_struct_data=[]
action = []
obj =[]
receptacle=[]
centroids =[]
trackID = 0
poseID = 0
human_handle,robot_handle =0,0
robo_init_radius,init_radius =0,0
blob = 1
dist = 25
stop="False"
flag=0

bgr_values,hsv_values,lower_color,upper_color,mask = [],[],[],[],[]


# Circles Intersection check (the future predicted smaller circles of the trajectory)
def circles_intersect(circle1, circle2):
    # Circle format: (center_x, center_y, radius)
    center1, radius1 = circle1[:2], 10
    center2, radius2 = circle2[:2], 10
    distance = np.linalg.norm(np.array(center1) - np.array(center2))
    return distance < (radius1 + radius2)

# Main circles intersection check (large circles indicating human and agent)
def main_circles_intersect(circle1, circle2):
    # Circle format: (center_x, center_y, radius)
    center1, radius1 = circle1[:2], circle1[2]
    center2, radius2 = circle2[:2], circle2[2]
    distance = np.linalg.norm(np.array(center1) - np.array(center2))
    return distance < (radius1 + radius2)

# Circles Intersection check (a large with smaller of the other entity)
def main_and_small_circle_intersect(circle1, circle2):
    center1, radius1 = circle1[:2], 10
    center2, radius2 = circle2[:2], circle2[2]
    distance = np.linalg.norm(np.array(center1) - np.array(center2))
    return distance < (radius1 + radius2)


# Contour generating function
def contour_gen(flip_img,mask_image):
    global bgr_values,hsv_values,lower_color,upper_color,mask,trackID,poseID,blob,dist,centroids,stop,flag,robo_init_radius,init_radius

    hp,ho,rp,ro = update_pose(poseID)

    image = flip_img  
    bw_image = mask_image
    
    rgb_values = np.array([[0.16, 0.41, 0.16], [0.37,0.46,0.74]])

    for i in range(len(rgb_values)):
        rgb_values[i] *= 255
        rgb_values[i] = np.round(rgb_values[i]).astype(np.uint8)

        bgr_values.append(np.array([rgb_values[i][2], rgb_values[i][1], rgb_values[i][0]]))

        hsv_values.append(cv2.cvtColor(np.uint8([[bgr_values[i]]]), cv2.COLOR_BGR2HSV)[0][0])

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        if i ==0:
            lower_color.append(np.array([hsv_values[i][0]-40, hsv_values[i][1]-40, hsv_values[i][2]-40]))  
            upper_color.append(np.array([hsv_values[i][0]+10, hsv_values[i][1]+10, hsv_values[i][2]+10]))  
        else:
            lower_color.append(np.array([hsv_values[i][0]-70, hsv_values[i][1]-70, hsv_values[i][2]-70]))  
            upper_color.append(np.array([hsv_values[i][0]+10, hsv_values[i][1]+10, hsv_values[i][2]+10]))  

        mask.append(cv2.inRange(hsv_image, lower_color[i], upper_color[i]))
        i=i+1
    i=0
    contour_image = image.copy()
    
    for i in range(len(rgb_values)):
        contours, _ = cv2.findContours(mask[i], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if i == 0:
            cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2) 
        else:
            cv2.drawContours(contour_image, contours, -1, (255, 0, 0), 2) 

        largest_contour = max(contours, key=cv2.contourArea)

        M = cv2.moments(largest_contour)
        centroid_x = int(M['m10'] / M['m00'])
        centroid_y = int(M['m01'] / M['m00'])
        max_distance = max(np.linalg.norm(point[0] - (centroid_x, centroid_y)) for point in largest_contour)

        radius = int(1.5 * max_distance) 
        if i ==0:
            if flag ==0:
                robo_init_radius = radius
                flag =1
        else:
            if flag ==1:
                init_radius = radius
                flag =2
        centroids.append((centroid_x,centroid_y,radius))        

        # RED -> X-axis , BLACK -> Y-axis
        if i ==0:
            major_axis_vector = (int(centroid_x + 30 * np.cos(ro[2])),
                                    int(centroid_y - 30 * np.sin(ro[2])))
            minor_axis_vector = (int(centroid_x - 30 * np.sin(ro[2])),
                                    int(centroid_y - 30 * np.cos(ro[2])))
            rit=[]
            x=0
            while x<blob:
                rit.append((int(centroid_x + dist*(x+2) * np.cos(ro[2])), int(centroid_y - dist*(x+2) * np.sin(ro[2]))))
                cv2.circle(image, rit[x], 13, (0, 255, 0), -1)  
                cv2.circle(bw_image, rit[x], 13, (0, 255, 0), -1) 
                x=x+1
            x=0

            cv2.circle(image, (centroid_x, centroid_y), robo_init_radius, (0, 255, 0), -1)  
            cv2.circle(bw_image, (centroid_x, centroid_y), robo_init_radius, (0, 255, 0), -1) 
            cv2.arrowedLine(image, (centroid_x, centroid_y), major_axis_vector, (0,0,0), 2)
            cv2.arrowedLine(image, (centroid_x, centroid_y), minor_axis_vector, (0,0,255), 2)
            cv2.arrowedLine(bw_image, (centroid_x, centroid_y), major_axis_vector, (0,0,255), 2)
            cv2.arrowedLine(bw_image, (centroid_x, centroid_y), minor_axis_vector, (0,0,0), 2)  
        else:
            major_axis_vector = (int(centroid_x + 30 * np.cos(ho[2])),
                                    int(centroid_y - 30 * np.sin(ho[2])))
            minor_axis_vector = (int(centroid_x - 30 * np.sin(ho[2])),
                                    int(centroid_y - 30 * np.cos(ho[2])))
            hit=[]
            y=0
            while y<blob:
                hit.append((int(centroid_x + dist*(y+2) * np.cos(ho[2])), int(centroid_y - dist*(y+2) * np.sin(ho[2]))))
                cv2.circle(image, hit[y], 13, (255, 0, 0), -1) 
                cv2.circle(bw_image, hit[y], 13, (255, 0, 0), -1) 
                y=y+1
            y=0
            cv2.circle(image, (centroid_x, centroid_y), init_radius, (255, 0, 0), -1)  
            cv2.circle(bw_image, (centroid_x, centroid_y), init_radius, (255, 0, 0), -1)  
            cv2.arrowedLine(image, (centroid_x, centroid_y), major_axis_vector, (0,0,0), 2)
            cv2.arrowedLine(image, (centroid_x, centroid_y), minor_axis_vector, (0,0,255), 2)
            cv2.arrowedLine(bw_image, (centroid_x, centroid_y), major_axis_vector, (0,0,255), 2)
            cv2.arrowedLine(bw_image, (centroid_x, centroid_y), minor_axis_vector, (0,0,0), 2) 

            
        i = i+1
    i=0
    for x in range(len(hit)):
        for y in range(len(rit)):
            if circles_intersect(rit[y], hit[x]) or main_and_small_circle_intersect(rit[y], centroids[1]) or main_circles_intersect(centroids[0], centroids[1]):
                stop = "True"
                with open("shared_variable.txt", "w") as file:
                    file.write(stop)
                break
                print(f"Circles {x} and {y} intersect!")  
            else:
                stop = "False"
                with open("shared_variable.txt", "w") as file:
                    file.write(stop)    
        if stop == "True":
            break
        else:
            continue                  
       
    bgr_values,hsv_values,lower_color,upper_color,mask,centroids = [],[],[],[],[],[]
    return bw_image

# Masking the image
def masking(flip_img,depth_img):
    rgb_image = flip_img  
    depth_image = depth_img  
    depth_threshold = 122  
    result_image = np.zeros_like(rgb_image, dtype=np.uint8)
    obstacle_mask = (depth_image <= depth_threshold).astype(np.uint8) * 255  
    free_space_mask = 255 - obstacle_mask
    result_image[np.where((free_space_mask == 255))] = [255, 255, 255]
    return result_image


# Creating map and displaying it
def create_occupancy_grid(combined_img):
    plt.ion()
    width_meters = 12.5
    height_meters = 12.5
    cell_size_meters = 0.0125 
    image = combined_img
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    width_cells = int(width_meters / cell_size_meters)
    height_cells = int(height_meters / cell_size_meters)

    image = cv2.resize(image, (width_cells, height_cells))
    flipped_img = np.flip(image,axis=0)
    _, binary_image = cv2.threshold(flipped_img, 20, 255, cv2.THRESH_BINARY)
    plt.imshow(binary_image, cmap='gray', origin='lower', interpolation='nearest')
    plt.title('Occupancy Grid Map')
    plt.xlabel('Grid Cells (x-axis)')
    plt.ylabel('Grid Cells (y-axis)')
    plt.pause(0.0001)

# Starting API connection with the simulator
def sim_start():
    global trackID,human_handle,robot_handle,poseID
    sim.simxFinish(-1)

    trackID = sim.simxStart('127.0.0.1',19992,True,True,5000,5)
    poseID = connection()
    if trackID!= -1:
        print("Connected to Vision Remote API Server")
        try:    
            _, vision_sensor_handle = sim.simxGetObjectHandle(trackID, 'house_view', sim.simx_opmode_blocking)

            while sim.simxGetConnectionId(trackID) != -1:
                
                if vision_sensor_handle != -1:
                    _, resolution, image = sim.simxGetVisionSensorImage(trackID, vision_sensor_handle, 0, sim.simx_opmode_blocking)
                    _, resolution, depth_buffer = sim.simxGetVisionSensorDepthBuffer(trackID, vision_sensor_handle, sim.simx_opmode_blocking)

                    normalized_image = (image - np.min(image)) / (np.max(image) - np.min(image))

                    scaled_image = (normalized_image * 255).astype(np.uint8)
                    matrix = np.ones(resolution) 
                    op_matrix = matrix.reshape(resolution[0],resolution[1],1)
                    resulting_matrix = np.tile(op_matrix, (1, 1, 3))
                    resulting_tuple = tuple(resulting_matrix.shape)
                    nil_matrix = np.ones(resulting_tuple)  * 255
                    flat_array = nil_matrix.flatten()
                    shifted_image = np.add(flat_array,image)

                    if _ == sim.simx_return_ok:
                        img = np.array(shifted_image, dtype=np.uint8)
                        img.resize([resolution[0], resolution[1], 3])
                        flip_img =np.flip(img,axis=0)
                        flip_img = cv2.cvtColor(flip_img,cv2.COLOR_BGR2RGB)

                        depth_image = np.array(depth_buffer).reshape(resolution[::-1])
                        depth_flip_img =np.flip(depth_image,axis=0)
                        
                        normalized_depth_image = (depth_flip_img - np.min(depth_flip_img)) / (np.max(depth_flip_img) - np.min(depth_flip_img))

                        equalized_depth_image = (cv2.equalizeHist((normalized_depth_image * 255).astype(np.uint8)) / 255).astype(np.float32)

                        cv2.imwrite('equalized_depth_image.png', (equalized_depth_image * 255).astype(np.uint8))
                        cv2.imwrite('depth_image.png',(depth_flip_img * 255).astype(np.uint8))
                        eq_depth_image = (equalized_depth_image * 255).astype(np.uint8)
                        depth_img = (depth_flip_img * 255).astype(np.uint8)
                        mask_image = masking(flip_img,depth_img)
                        combined_img = contour_gen(flip_img,mask_image)
                        create_occupancy_grid(combined_img)
                        

                    else:
                        print('Failed to get image from the vision sensor.')

                else:
                    print('Vision sensor not found.')
                
        except Exception as e:
            print(f"Exception(tracking_code): {e}")
        finally:
            # Disconnect from CoppeliaSim
            sim.simxFinish(trackID)
            trackID = -1
            print('Connection closed.')

    else:
        print("Connection failed")
        sys.exit('Could not reconnect')
        
    

if __name__ == '__main__': 
    sim_start()
