import subprocess
import time

llm_code = subprocess.Popen(["python3", "-m", "utils.gemini_code"])
llm_code.wait()
llm_pddl_mapping = subprocess.Popen(["python3", "utils/pddl_mapping.py"])
llm_pddl_mapping.wait()
pddl_plan_gen = subprocess.Popen(["python3", "pddl/downward/pddl_plan_gen.py"])
pddl_plan_gen.wait()


