inp1 = """It is morning time, the user has prepared his breakfast
You see the user perform the task:  
* serve the food *
What do you anticipate to be the next 4 tasks?
Requirement: The kitchen is very dirty            
"""

op1_cot = """{
    "chain-of-thought": "Let us go through the requirements step by step. The user usually prepares and serves food. Since 'serve the food' has already been done, so we think after that. The kitchen is dirty, so the user will first clean the kitchen. The requirements in the morning are: prepare breakfast, prepare office clothes, charge electronic devices, prepare the office bag. Since the user has already prepared the breakfast, we can eliminate that. The next task is 'prepare office clothes'. Checking if the clothes are clean. Since the clothes are clean, the user can directly prepare office clothes. The next task is 'charge electronic devices'. The user charges electronic devices. The next task is 'prepare the office bag'. The user prepares the office bag.",
    "tasks": [
        "clean the room (kitchen)",
        "prepare office clothes",
        "charge the electronic devices",
        "prepare the office bag"
    ]
}
"""

inp2 = """It is the evening time, and user has not eaten dinner yet.
You see the user perform the task:  
*prepare casual clothes*
What do you anticipate to be the next 4 tasks?
Requirement: Spoiled food needs to be thrown
*Rice is not available*
"""

op2_cot = """
{
    "chain-of-thought": "Let us go through the requirements step by step. The user has already prepared casual clothes so we can think after that. We can anticipate that the user will first finish the requirement by throwing away the leftover food. We know that on evenings the user eats dinner and takes medicines. Checking if the user has eaten the food. The user has not eaten yet, so they will first prepare and serve their dinner. Since the user takes their medicine after food in the evening, we can anticipate that the user will prepare medicines. We know that the spoiled food needs to be thrown, so the user will throw away leftover food. We see that the user has prepared casual clothes, so they will prepare a casual and fun dinner. Hence we can anticipate the user eating pizza.",
    "tasks": [
        "throw away leftover food",
        "prepare food",
        "serve the food",
        "prepare medicines"
    ]
}
"""
