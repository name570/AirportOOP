from Classes import *
import random
airplanes = ["Boeing737", "Boeing747", "Boeing747-8", "A320", "A380", "A300", "TU-154"]
target = ["Up", "Down"]
start_time = Time("7:30")
steps = ["0:00", "0:01", "0:02", "0:03", "0:04", "0:05", "0:06", "0:07", "0:08", "0:09", "0:10"]
finish_time = Time("23:20")
curr_time = start_time
schedule = open("schedule.txt", "w")
while (curr_time < finish_time):
    random_time = Time(random.choice(steps))
    curr_time = curr_time + random_time
    random_airplane = random.choice(airplanes)
    random_target = random.choice(target)
    tmp_str = str(curr_time) + " " + random_airplane + " " + random_target + "\n"
    schedule.write(tmp_str)
schedule.close()
