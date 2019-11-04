#!/usr/bin/env python
import rospy
import numpy as np
import matplotlib.pyplot as plt

'''
line format: 34-angle time activity change

angle mapping:
0 = neck_x
1 = neck_y
2 = neck_z
3 = trunk_x
4 = trunk_y
5 = trunk_z
6 = l_hip_x
7 = l_hip_y
8 = l_hip_z
9 = l_knee_x
10 = l_ankle_x
11 = l_ankle_y
12 = l_ankle_z
13 = r_hip_x
14 = r_hip_y
15 = r_hip_z
16 = r_knee_x
17 = r_ankle_x
18 = r_ankle_y
19 = r_ankle_z
20 = l_shoulder_x 
21 = l_shoulder_y
22 = l_shoulder_z
23 = l_elbow_x
24 = l_wrist_x 
25 = l_wrist_y
26 = l_wrist_z
27 = r_shoulder_x 
28 = r_shoulder_y
29 = r_shoulder_z
30 = r_elbow_x
31 = r_wrist_x 
32 = r_wrist_y
33 = r_wrist_z

'''

body_score_table = np.array([1,1,1,2,3,3,4,5,6,7,7,7],
							[1,2,2,3,4,4,5,6,6,7,7,8],
							[2,3,3,3,4,5,6,7,7,8,8,8],
							[3,4,4,4,5,6,7,8,9,9,9,9],
							[4,4,4,5,6,7,8,8,9,9,9,9],
							[6,6,6,7,8,8,9,9,10,10,10,10],
							[7,7,7,8,9,9,9,10,10,11,11,11],
							[8,8,8,9,10,10,11,11,11,12,12,12],
							[9,9,9,10,10,10,11,11,11,12,12,12],
							[10,10,10,11,11,11,11,12,12,12,12,12],
							[11,11,11,11,12,12,12,12,12,12,12,12],
							[12,12,12,12,12,12,12,12,12,12,12,12])

def score_neck(neck_angles):
	score = 0
	if (neck_angles[0] <= 10.0 or neck_angles[0] >= 20.0):
		score = 2
	elif(neck_angles[0] >= 10.0):
		score = 1
	if (neck_angles[1] != 0.0):
		score += 1
	if (neck_angles[2] != 0.0):
		score += 1
	return score

def score_trunk(trunk_angles):
	score = 1
	if (trunk_angles[0] <= 0.0 or trunk_angles[0]):
		score = 2
	elif (trunk_angles[0] <= 60.0):
		score = 3
	else:
		score = 4

def score_leg(leg_angles):
	score = 0
	if (leg_angles[0] > 60.0 or leg_angles[3] >= 60.0 or leg_angles[3] >= 60.0):
		score = 2
	elif (leg_angles[0] > 30.0 or leg_angles[3] >= 30.0 or leg_angles[3] >= 30.0):

def score_legs(leg_angles):
	diff_score = 1
	for i in xrange(7):
		if (np.fabs(leg_angles[i] - leg_angles[i+7]) < 1e-4):
			diff_score = 2
			break

	l_score = score_leg(leg_angles[0:7])
	r_score = score_leg(leg_angles[7:14])

	return diff_score + max(l_score, r_score)

def score_body_posture(body_angles):
	neck_score = score_neck(body_angles[0:3])
	trunk_score = score_trunk(body_angles[3:6])
	legs_score = score_legs(body_angles[6:20])

	final_score = 0
	if (neck_score == 1):
		if (legs_score == 1):
			if (trunk_score == 1):
				final_score = 1
			elif (trunk_score == 2):
				final_score = 2
			elif (trunk_score == 3):
				final_score = 2
			elif (trunk_score == 4):
				final_score = 3
			else:
				final_score = 4
		elif (legs_score == 2):
			if (trunk_score == 1):
				final_score = 2
			elif (trunk_score == 2):
				final_score = 3
			elif (trunk_score == 3):
				final_score = 4
			elif (trunk_score == 4):
				final_score = 5
			else:
				final_score = 6
		elif (legs_score == 3):
			if (trunk_score == 1):
				final_score = 3
			elif (trunk_score == 2):
				final_score = 4
			elif (trunk_score == 3):
				final_score = 5
			elif (trunk_score == 4):
				final_score = 6
			else:
				final_score = 7
		else:
			if (trunk_score == 1):
				final_score = 4
			elif (trunk_score == 2):
				final_score = 5
			elif (trunk_score == 3):
				final_score = 6
			elif (trunk_score == 4):
				final_score = 7
			else:
				final_score = 8
	elif (neck_score == 2):
		if (legs_score == 1):
			if (trunk_score == 1):
				final_score = 1
			elif (trunk_score == 2):
				final_score = 3
			elif (trunk_score == 3):
				final_score = 4
			elif (trunk_score == 4):
				final_score = 5
			else:
				final_score = 6
		elif (legs_score == 2):
			if (trunk_score == 1):
				final_score = 2
			elif (trunk_score == 2):
				final_score = 4
			elif (trunk_score == 3):
				final_score = 5
			elif (trunk_score == 4):
				final_score = 6
			else:
				final_score = 7
		elif (legs_score == 3):
			if (trunk_score == 1):
				final_score = 3
			elif (trunk_score == 2):
				final_score = 5
			elif (trunk_score == 3):
				final_score = 6
			elif (trunk_score == 4):
				final_score = 7
			else:
				final_score = 8
		else:
			if (trunk_score == 1):
				final_score = 4
			elif (trunk_score == 2):
				final_score = 6
			elif (trunk_score == 3):
				final_score = 7
			elif (trunk_score == 4):
				final_score = 8
			else:
				final_score = 9
	else:	
		if (legs_score == 1):
			if (trunk_score == 1):
				final_score = 3
			elif (trunk_score == 2):
				final_score = 4
			elif (trunk_score == 3):
				final_score = 5
			elif (trunk_score == 4):
				final_score = 6
			else:
				final_score = 7
		elif (legs_score == 2):
			if (trunk_score == 1):
				final_score = 3
			elif (trunk_score == 2):
				final_score = 5
			elif (trunk_score == 3):
				final_score = 6
			elif (trunk_score == 4):
				final_score = 7
			else:
				final_score = 8
		elif (legs_score == 3):
			if (trunk_score == 1):
				final_score = 5
			elif (trunk_score == 2):
				final_score = 6
			elif (trunk_score == 3):
				final_score = 7
			elif (trunk_score == 4):
				final_score = 8
			else:
				final_score = 9
		else:
			if (trunk_score == 1):
				final_score = 6
			elif (trunk_score == 2):
				final_score = 7
			elif (trunk_score == 3):
				final_score = 8
			elif (trunk_score == 4):
				final_score = 9
			else:
				final_score = 9

	return final_score

def score_upper_arm(upper_arm_angles):
	score = 0
	#shoulder
	if (arm_angles[0] <= 20.0 and arm_angles[0] >= -20.0):
		score = 1
	elif (arm_angles[0] <= -20.0 or arm_angles[0] <= 45.0):
		score = 2
	elif (arm_angles[0] <= 90.0):
		score = 3
	else:
		score = 4

	if (arm_angles[2] > 0.0):
		score += 1
	if (np.fabs(arm_angles[1]) > 0.0):
		score += 1

	return score

def score_elbow(elbow_angle):
	#elbow
	score = 0
	if (elbow_angles <= 100.0 and elbow_angles >= 60.0):
		score = 1
	else:
		score = 2
	return score

def score_wrist(wrist_angles):
	#wrist
	score = 0
	if (wrist_angles[1] >= -15.0 and wrist_angles[1] <= 15.0):
		score = 1
	else:
		score = 2
	if (np.fabs(wrist_angles[0]) > 0.0 or np.fabs(wrist_angles[2]) > 0.0):
		score += 1
	return score

def score_arm_posture(u_arm_score, elbow_score, wrist_score):
	score = 0
	if (elbow_score == 1):
		if (wrist_score == 1):
			if (u_arm_score == 1):
				score = 1
			elif (u_arm_score == 2):
				score = 1
			elif (u_arm_score == 3):
				score = 3
			elif (u_arm_score == 4):
				score = 4
			elif (u_arm_score == 5):
				score = 6
			else:
				score = 7
		elif (wrist_score == 2):
			if (u_arm_score == 1):
				score = 2
			elif (u_arm_score == 2):
				score = 2
			elif (u_arm_score == 3):
				score = 4
			elif (u_arm_score == 4):
				score = 5
			elif (u_arm_score == 5):
				score = 7
			else:
				score = 8
		else:
			if (u_arm_score == 1):
				score = 2
			elif (u_arm_score == 2):
				score = 3
			elif (u_arm_score == 3):
				score = 5
			elif (u_arm_score == 4):
				score = 5
			elif (u_arm_score == 5):
				score = 8
			else:
				score = 8
	else:
		if (wrist_score == 1):
			if (u_arm_score == 1):
				score = 1
			elif (u_arm_score == 2):
				score = 2
			elif (u_arm_score == 3):
				score = 4
			elif (u_arm_score == 4):
				score = 5
			elif (u_arm_score == 5):
				score = 7
			else:
				score = 8
		elif (wrist_score == 2):
			if (u_arm_score == 1):
				score = 2
			elif (u_arm_score == 2):
				score = 3
			elif (u_arm_score == 3):
				score = 5
			elif (u_arm_score == 4):
				score = 6
			elif (u_arm_score == 5):
				score = 8
			else:
				score = 9
		else:
			if (u_arm_score == 1):
				score = 3
			elif (u_arm_score == 2):
				score = 4
			elif (u_arm_score == 3):
				score = 5
			elif (u_arm_score == 4):
				score = 7
			elif (u_arm_score == 5):
				score = 8
			else:
				score = 9

	return score

def score_arms(arm_angles):
	r_u_arm_score = score_upper_arm(arm_angles[0:3])
	r_elbow_score = score_elbow(arm_angles[3])
	r_wrist_score = score_wrist(arm_angles[4:7])

	l_u_arm_score = score_upper_arm(arm_angles[7:10])
	l_elbow_score = score_elbow(arm_angles[10])
	l_wrist_score = score_wrist(arm_angles[11:14])

	r_score = score_arm_posture(r_u_arm_score, r_elbow_score, r_wrist_score)
	l_score = score_arm_posture(l_u_arm_score, l_elbow_score, l_wrist_score)

	return max(r_score, l_score)

def give_reba_score(line):
	f = open(line, 'a')
	data = w.split(' ')
	angles = []
	for i in xrange(34):
		angles.append(float(data[i]))
	time = float(data[34])
	activity = int(data[35])
	change = int(data[36])

	body_posture_score = score_body_posture(angles[0:20])
	arm_posture_score = score_arm_posture(angles[20:, len(angles)])
	
	return body_score_table[body_posture_score-1][arm_posture_score-1]


def read_file(r):
	f = open(r, 'r')
	for line in f:
		data = f.readline()
		reba_score = give_reba_score(data)

if __name__ == '__main__':
	r_filename = raw_input('Enter file to open')
	w_filename = raw_input('Enter file to write to')
	read_file(r_filename)