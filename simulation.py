import subprocess
import time

# Run the first Python file
with open("shared_variable.txt", "w") as file:
    file.truncate()
dist_tasks = subprocess.Popen(["python3", "sim/gen_files.py"])
dist_tasks.wait()
process0 = subprocess.Popen(['python3', 'sim/tracking_complete.py'])
process1 = subprocess.Popen(['python3', 'sim/robot_agent.py'])
process2 = subprocess.Popen(['python3', 'sim/human_agent.py'])
