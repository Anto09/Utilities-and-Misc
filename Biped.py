#!/usr/bin/env python
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import threading
import time
class Biped:
	M = 100.0
	L = 0.65
	D = 0.75
	t = 0.0
	dt = 0.04
	V_fin = 1.00
	V_init = 1.00
	status = 0
	prev_status = 0
 
	com = np.array([0.0, 0.0])
	com_acc = np.array([0.0, 0.0])
	com_vel = np.array([0.0, 0.0])
 
	gravity = np.array([0.0, -9.81])
	grd_frc = np.array([0.0, 0.0])
 
	low_limits = np.array([0.0, 0.0, 0.0])
	up_limits = np.array([0.0, 30.0*np.pi/180.0, 60.0*np.pi/180.0])
 
	prev_l_angles = np.array([0.0, 0.0, 0.0])
	prev_l_vels = np.array([0.0, 0.0, 0.0])
 
	l_angles = np.array([0.0, 0.0, 0.0])
	l_vels = np.array([0.0, 0.0, 0.0])
	l_accs = np.array([0.0, 0.0, 0.0])
	l_torques = np.array([0.0, 0.0, 0.0])
 
	lknee_pos = np.array([0.0, 0.0])
	lfoot_pos = np.array([0.0, 0.0])
 
	prev_r_angles = np.array([0.0, 0.0, 0.0])
	prev_r_vels = np.array([0.0, 0.0, 0.0])
 
	r_angles = np.array([0.0, 0.0, 0.0])
	r_vels = np.array([0.0, 0.0, 0.0])
	r_accs = np.array([0.0, 0.0, 0.0])
	r_torques = np.array([0.0, 0.0, 0.0])
 
	rfoot_pos = np.array([0.0, 0.0])
	rknee_pos = np.array([0.0, 0.0])

	r_angles_bent = np.array([0.0, 0.0])
	l_angles_bent = np.array([0.0, 0.0])
 
	counter = 0.0
 
	def init(self):     
		self.status = 0
		self.t = 0.0
		self.r_angles = np.array([0.0, 0.0, 0.0])
		self.l_angles = np.array([0.0, np.pi/6.0, np.pi/3.0])
		self.com_vel = np.array([1.0, 0.0])
		self.counter = 10.0
 
	def calc_com(self, single = True, right = True):
		if (single):
			if (right):         
				self.com[0] = self.rfoot_pos[0] + self.L*(np.sin(self.r_angles[2] + self.r_angles[1]) + np.sin(self.r_angles[1]))
				self.com[1] = self.L*(np.cos(self.r_angles[2] + self.r_angles[1]) + np.cos(self.r_angles[1]))
			else:
				self.com[0] = self.lfoot_pos[0] + self.L*(np.sin(self.l_angles[2] + self.l_angles[1]) + np.sin(self.l_angles[1]))
				self.com[1] = self.L*(np.cos(self.l_angles[2] + self.l_angles[1]) + np.cos(self.l_angles[1]))
		else:
			if (self.prev_status == 0):
				self.com[0] = self.lfoot_pos[0] - self.L*(np.sin(self.l_angles[1] - self.l_angles[2]) + np.sin(self.l_angles[1]))
				self.com[1] = self.L*(np.cos(self.l_angles[1] - self.l_angles[2]) + np.cos(self.l_angles[1]))
			else:
				self.com[0] = self.rfoot_pos[0] - self.L*(np.sin(self.r_angles[1] - self.r_angles[2]) + np.sin(self.r_angles[1]))
				self.com[1] = self.L*(np.cos(self.r_angles[1] - self.r_angles[2]) + np.cos(self.r_angles[1]))
 
	def calc_com_vel(self, single = True, right = True):
		if (single):
			if (right):
				self.com_vel[0] = self.L*((self.r_vels[2] + self.r_vels[1])*np.cos(self.r_angles[2] + self.r_angles[1]) + self.r_vels[1]*np.cos(self.r_angles[1]))
				self.com_vel[1] = -self.L*((self.r_vels[2] + self.r_vels[1])*np.sin(self.r_angles[2] + self.r_angles[1]) + self.r_vels[1]*np.sin(self.r_angles[1]))     
			else:
				self.com_vel[0] = self.L*((self.l_vels[2] + self.l_vels[1])*np.cos(self.l_angles[2] + self.l_angles[1]) + self.l_vels[1]*np.cos(self.l_angles[1]))
				self.com_vel[1] = -self.L*((self.l_vels[2] + self.l_vels[1])*np.sin(self.l_angles[2] + self.l_angles[1]) + self.l_vels[1]*np.sin(self.l_angles[1]))
		else:
			if (self.prev_status == 0):
				self.com_vel[0] = self.L*((self.l_vels[2] + self.l_vels[1])*np.cos(self.l_angles[2] + self.l_angles[1]) + self.l_vels[1]*np.cos(self.l_angles[1]))
				self.com_vel[1] = -self.L*((self.l_vels[2] + self.l_vels[1])*np.sin(self.l_angles[2] + self.l_angles[1]) + self.l_vels[1]*np.sin(self.l_angles[1]))
			else:
				self.com_vel[0] = self.L*((self.r_vels[2] + self.r_vels[1])*np.cos(self.r_angles[2] + self.r_angles[1]) + self.r_vels[1]*np.cos(self.r_angles[1]))
				self.com_vel[1] = -self.L*((self.r_vels[2] + self.r_vels[1])*np.sin(self.r_angles[2] + self.r_angles[1]) + self.r_vels[1]*np.sin(self.r_angles[1]))
				 
	def calc_com_acc(self, single = True, right = True):
		if (single):
			if (right):
				self.com_acc[0] = self.L*((self.r_accs[2] + self.r_accs[1])*np.cos(self.r_angles[2] + self.r_angles[1]) - (self.r_vels[2] + self.r_vels[1])**2*np.sin(self.r_angles[2] + self.r_angles[1]) + self.r_accs[1]*np.cos(self.r_angles[1]) - self.r_vels[1]**2*np.sin(self.r_angles[1]))
				self.com_acc[1] = -self.L*((self.r_accs[2] + self.r_accs[1])*np.sin(self.r_angles[2] + self.r_angles[1]) - (self.r_vels[2] + self.r_vels[1])**2*np.cos(self.r_angles[2] + self.r_angles[1]) + self.r_accs[1]*np.sin(self.r_angles[1]) + self.r_vels[1]**2*np.cos(self.r_angles[1]))
			else:
				self.com_acc[0] = self.L*((self.l_accs[2] + self.l_accs[1])*np.cos(self.l_angles[2] + self.l_angles[1]) - (self.l_vels[2] + self.l_vels[1])**2*np.sin(self.l_angles[2] + self.l_angles[1]) + self.l_accs[1]*np.cos(self.l_angles[1]) - self.l_vels[1]**2*np.sin(self.l_angles[1]))
				self.com_acc[1] = -self.L*((self.l_accs[2] + self.l_accs[1])*np.sin(self.l_angles[2] + self.l_angles[1]) - (self.l_vels[2] + self.l_vels[1])**2*np.cos(self.l_angles[2] + self.l_angles[1]) + self.l_accs[1]*np.sin(self.l_angles[1]) + self.l_vels[1]**2*np.cos(self.l_angles[1]))		 
		else:
			if (self.prev_status == 0):
				self.com_acc[0] = self.L*((self.l_accs[2] + self.l_accs[1])*np.cos(self.l_angles[2] + self.l_angles[1]) - (self.l_vels[2] + self.l_vels[1])**2*np.sin(self.l_angles[2] + self.l_angles[1]) + self.l_accs[1]*np.cos(self.l_angles[1]) - self.l_vels[1]**2*np.sin(self.l_angles[1]))
				self.com_acc[1] = -self.L*((self.l_accs[2] + self.l_accs[1])*np.sin(self.l_angles[2] + self.l_angles[1]) - (self.l_vels[2] + self.l_vels[1])**2*np.cos(self.l_angles[2] + self.l_angles[1]) + self.l_accs[1]*np.sin(self.l_angles[1]) + self.l_vels[1]**2*np.cos(self.l_angles[1]))		 
			else:
				self.com_acc[0] = self.L*((self.r_accs[2] + self.r_accs[1])*np.cos(self.r_angles[2] + self.r_angles[1]) - (self.r_vels[2] + self.r_vels[1])**2*np.sin(self.r_angles[2] + self.r_angles[1]) + self.r_accs[1]*np.cos(self.r_angles[1]) - self.r_vels[1]**2*np.sin(self.r_angles[1]))
				self.com_acc[1] = -self.L*((self.r_accs[2] + self.r_accs[1])*np.sin(self.r_angles[2] + self.r_angles[1]) - (self.r_vels[2] + self.r_vels[1])**2*np.cos(self.r_angles[2] + self.r_angles[1]) + self.r_accs[1]*np.sin(self.r_angles[1]) + self.r_vels[1]**2*np.cos(self.r_angles[1]))			
	
	def calc_vels(self):
		self.prev_r_vels = np.copy(self.r_vels)
		self.prev_l_vels = np.copy(self.l_vels)
		 
		self.r_vels = np.subtract(self.r_angles, self.prev_r_angles)#/self.dt
		self.l_vels = np.subtract(self.l_angles, self.prev_l_angles)#/self.dt
		 
	def calc_accs(self):
		self.r_accs = np.subtract(self.r_vels, self.prev_r_vels)#/self.dt
		self.l_accs = np.subtract(self.l_vels, self.prev_l_vels)#/self.dt
 
	def calc_knee(self, single = True, right = True):
		if (single):
			if (right): #left leg in swing phase
				#right knee
				self.rknee_pos[0] = self.rfoot_pos[0] + self.L*np.sin(self.r_angles[1] + self.r_angles[2])
				self.rknee_pos[1] = self.L*np.cos(self.r_angles[1] + self.r_angles[2])
				#left knee
				self.lknee_pos[0] = self.com[0] + self.L*np.sin(self.l_angles[1])
				self.lknee_pos[1] = self.com[1] - self.L*np.cos(self.l_angles[1])
			else: #right leg in swing phase
				#left knee
				self.lknee_pos[0] = self.lfoot_pos[0] + self.L*np.sin(self.l_angles[2] + self.l_angles[1])
				self.lknee_pos[1] = self.L*np.cos(self.l_angles[2] + self.l_angles[1])
				#right knee
				self.rknee_pos[0] = self.com[0] + self.L*np.sin(self.r_angles[1])
				self.rknee_pos[1] = self.com[1] - self.L*np.cos(self.r_angles[1])
		else:
			if (self.prev_status == 0):
				#left knee
				self.lknee_pos[0] = self.lfoot_pos[0] - self.L*np.sin(self.l_angles[1] - self.l_angles[2])
				self.lknee_pos[1] = self.L*np.cos(self.l_angles[1] - self.l_angles[2])
				#right knee
				self.rknee_pos[0] = self.com[0] - self.L*np.sin(self.r_angles[1])
				self.rknee_pos[1] = self.com[1] - self.L*np.cos(self.r_angles[1])
			else:
				#right knee
				self.rknee_pos[0] = self.rfoot_pos[0] - self.L*np.sin(self.r_angles[1] - self.r_angles[2])
				self.rknee_pos[1] = self.L*np.cos(self.r_angles[1] - self.r_angles[2])
				#left knee
				self.lknee_pos[0] = self.com[0] - self.L*np.sin(self.l_angles[1])
				self.lknee_pos[1] = self.com[1] - self.L*np.cos(self.l_angles[1])
	 
	def calc_foot(self, single = True, right = True):
		if (single):
			if (right): #right foot position is known
				self.lfoot_pos[0] = self.lknee_pos[0] + self.L*np.sin(self.l_angles[1] - self.l_angles[2])
				self.lfoot_pos[1] = self.lknee_pos[1] - self.L*np.cos(self.l_angles[1] - self.l_angles[2])
				 
			else: #left foot position is known
				self.rfoot_pos[0] = self.rknee_pos[0] + self.L*np.sin(self.r_angles[1] - self.r_angles[2])
				self.rfoot_pos[1] = self.rknee_pos[1] - self.L*np.cos(self.r_angles[1] - self.r_angles[2])
		else:
			if (self.prev_status == 0):
				self.rfoot_pos[0] = self.rknee_pos[0] - self.L*np.sin(self.r_angles[1] + self.r_angles[2])
				self.rfoot_pos[1] = self.rknee_pos[1] - self.L*np.cos(self.r_angles[1] + self.r_angles[2])
			else:
				self.lfoot_pos[0] = self.lknee_pos[0] - self.L*np.sin(self.l_angles[1] + self.l_angles[2])
				self.lfoot_pos[1] = self.lknee_pos[1] - self.L*np.cos(self.l_angles[1] + self.l_angles[2])
 
	def calc_torques(self):
		net_force = np.linalg.norm(self.grd_frc)
		self.r_torques = np.array([net_force*np.sin(self.r_angles[0]),
								   net_force*np.sin(self.r_angles[1]),
								   net_force*np.sin(self.r_angles[2])])
		self.l_torques = np.array([net_force*np.sin(self.l_angles[0]),
								   net_force*np.sin(self.l_angles[1]),
								   net_force*np.sin(self.l_angles[2])])
	 
	def calc_grd_frc(self):
		self.grd_frc = self.M  * np.subtract(self.com_acc, self.gravity)
 
	def calc_all_vals(self, single = True, right = True):
		self.calc_vels()
		self.calc_accs()
		self.calc_torques()
		self.calc_com(single, right)
		self.calc_com_acc(single, right)
		self.calc_com_vel(single, right)
		self.calc_knee(single, right)
		self.calc_foot(single, right)
		self.calc_grd_frc()
 
	def forward_kinematics(self, leg_down = 2):
		#leg_down = 0 -> right foot is down, calculate FK from the right foot as base
		#leg_down = 1 -> left foot is down, calculate FK from the left foot as base
		#leg_down = 2 -> both feet are down
 
		if (leg_down == 0):
			self.calc_com(True, True)
			self.calc_knee(True, True)
			self.calc_foot(True, True)
		elif (leg_down == 1):
			self.calc_com(True, False)
			self.calc_knee(True, False)
			self.calc_foot(True, False)
		else:
			self.calc_com(False, False)
			self.calc_knee(False, False)
			self.calc_foot(False, False)
			 
	def is_planted(self):
		if (self.status == 0):
			return self.lfoot_pos[1] == 0.0
		elif (self.status == 1):
			return self.rfoot_pos[1] == 0.0
		else:
			return self.rfoot_pos[1] == 0.0 and self.lfoot_pos[1] == 0.0
 
	def foot_x_dist(self):
		return np.fabs(self.rfoot_pos[0] - self.lfoot_pos[0])
 
	def grnd_frc_condition(self, right = True, rpst = 1):
		#ensure return values > 0
		if (rpst == 0):
			return self.com_acc[1] + self.gravity[1]
		else:
			if (right):
				return (self.gravity[1]/self.L) - (self.r_accs[2] + self.r_accs[1])*np.sin(self.r_angles[2] + self.r_angles[1]) + (self.r_vels[2] + self.r_vels[1])**2*np.cos(self.r_angles[2] + self.r_angles[1]) + self.r_accs[1]*np.sin(self.r_angles[1]) + self.r_vels[1]**2*np.cos(self.r_angles[1])
			else:
				return (self.gravity[1]/self.L) - (self.l_accs[2] + self.l_accs[1])*np.sin(self.l_angles[2] + self.l_angles[1]) + (self.l_vels[2] + self.l_vels[1])**2*np.cos(self.l_angles[2] + self.l_angles[1]) + self.l_accs[1]*np.sin(self.l_angles[1]) + self.l_vels[1]**2*np.cos(self.l_angles[1])
 
	def kinematic_chain_condition(self):
		#drive both to 0
		cond_1 = (np.cos(self.r_angles[2] + self.r_angles[1]) + np.cos(self.r_angles[1])) - (np.cos(self.l_angles[2] + self.l_angles[1]) + np.cos(self.l_angles[1]))
		cond_2 = (np.sin(self.r_angles[2] + self.r_angles[1]) + np.sin(self.r_angles[1]) - np.sin(self.l_angles[2] + self.l_angles[1]) - np.sin(self.l_angles[1])) - (self.D/self.L)
		return np.array([cond_1, cond_2])
 
	def calc_ZMP(self):
		return np.array([(self.com[0] - (self.grd_frc[0]/self.grd_frc[1])*self.com[1]), 0.0])
 
	def ZMP_condition(self, right = True, rpst = 0):
		if (right):
			if (rpst == 0):
				return self.rfoot_pos[0] - (self.com[0] - (self.grd_frc[0]/self.grd_frc[1])*self.com[1]) #Drive this to 0           
			elif (rpst == 1):
				return (self.com[1]/(self.com[0] - self.rfoot_pos[0])) - ((self.com_acc[1] + self.gravity[1])/self.com_acc[0]) #drive to 0 again
			else:
				lhs = (np.cos(self.r_angles[2] + self.r_angles[1]) + np.cos(self.r_angles[1]))/(np.sin(self.r_angles[2] + self.r_angles[1]) + np.sin(self.r_angles[1]))
				rhs_num = -(self.r_accs[2] + self.r_accs[1])*np.sin(self.r_angles[2] + self.r_angles[1]) - (self.r_vels[2] + self.r_vels[1])**2*np.cos(self.r_angles[2] + self.r_angles[1]) + self.r_accs[1]*np.sin(self.r_angles[1]) + self.r_vels[1]**2*np.cos(self.r_angles[1]) + self.gravity[1]/self.L
				rhs_den = (self.r_accs[2] + self.r_accs[1])*np.cos(self.r_angles[2] + self.r_angles[1]) - (self.r_vels[2] + self.r_vels[1])**2*np.sin(self.r_angles[2] + self.r_angles[1]) + self.r_accs[1]*np.cos(self.r_angles[1]) + self.r_vels[1]**2*np.sin(self.r_angles[1])
				return lhs - (rhs_num/rhs_den) #drive to 0 again
		else: 
			if (rpst == 0):
				return self.lfoot_pos[0] - (self.com[0] - (self.grd_frc[0]/self.grd_frc[1])*self.com[1]) #Drive this to 0           
			elif (rpst == 1):
				return (self.com[1]/(self.com[0] - self.lfoot_pos[0])) - ((self.com_acc[1] + self.gravity[1])/self.com_acc[0]) #drive to 0 again
			else:
				lhs = (np.cos(self.l_angles[2] + self.l_angles[1]) + np.cos(self.l_angles[1]))/(np.sin(self.l_angles[2] + self.l_angles[1]) + np.sin(self.l_angles[1]))
				rhs_num = -(self.l_accs[2] + self.l_accs[1])*np.sin(self.l_angles[2] + self.l_angles[1]) - (self.l_vels[2] + self.l_vels[1])**2*np.cos(self.l_angles[2] + self.l_angles[1]) + self.l_accs[1]*np.sin(self.l_angles[1]) + self.l_vels[1]**2*np.cos(self.l_angles[1]) + self.gravity[1]/self.L
				rhs_den = (self.l_accs[2] + self.l_accs[1])*np.cos(self.l_angles[2] + self.l_angles[1]) - (self.l_vels[2] + self.l_vels[1])**2*np.sin(self.l_angles[2] + self.l_angles[1]) + self.l_accs[1]*np.cos(self.l_angles[1]) + self.l_vels[1]**2*np.sin(self.l_angles[1])
				return lhs - (rhs_num/rhs_den) #drive to 0 again
 
	def ZMP_double_cond(self):
		#both elements of array should be positive
		if (self.status == 0):
			cond_1 = (self.com[0] - (self.grd_frc[0]/self.grd_frc[1])*self.com[1])  - self.rfoot_pos[0]
			cond_2 = self.lfoot_pos[0] - (self.com[0] - (self.grd_frc[0]/self.grd_frc[1])*self.com[1])
			return np.array([cond_1, cond_2])
		else:
			cond_1 = (self.com[0] - (self.grd_frc[0]/self.grd_frc[1])*self.com[1])  - self.lfoot_pos[0]
			cond_2 = self.rfoot_pos[0] - (self.com[0] - (self.grd_frc[0]/self.grd_frc[1])*self.com[1])
			return np.array([cond_1, cond_2])
 
	def draw_biped(self):
		self.forward_kinematics(self.status)
		plt.plot([self.com[0], self.rknee_pos[0], self.rfoot_pos[0]], [self.com[1], self.rknee_pos[1], self.rfoot_pos[1]], 'ro', 
				 [self.com[0], self.rknee_pos[0], self.rfoot_pos[0]], [self.com[1], self.rknee_pos[1], self.rfoot_pos[1]], 'r',
				 [self.com[0], self.lknee_pos[0], self.lfoot_pos[0]], [self.com[1], self.lknee_pos[1], self.lfoot_pos[1]], 'bo',
				 [self.com[0], self.lknee_pos[0], self.lfoot_pos[0]], [self.com[1], self.lknee_pos[1], self.lfoot_pos[1]], 'b')
		plt.draw()
 
	def calc_swing_leg_traj(self):
		if (self.status == 0):
			self.calc_com(True, True)
			self.calc_knee(True, True)
			self.calc_foot(True, True)
			self.calc_grd_frc()
 
			target_pos = np.array([self.com[1], (self.D + self.rfoot_pos[0]) - self.com[0]])
	 
			l = np.linalg.norm(target_pos)
 
			acos = min(1.0, l**2/(2.0*self.L*l))
			theta_g = np.arctan(target_pos[1]/target_pos[0])
			theta_a = np.arccos(acos)
			theta_b = np.arcsin((l*np.sin(theta_a))/self.L)
 
			orig_angles = np.copy(self.l_angles)
			# set angles based on foot position
			self.l_angles[1] += (theta_g + theta_a) * self.dt
			self.l_angles[2] += theta_b * self.dt
			self.calc_knee(True, True)
			self.calc_foot(True, True)
			dt_foot_pos = np.copy(self.lfoot_pos)
 
			self.l_angles[1] = (theta_g + theta_a)
			self.l_angles[2] = theta_b
			self.calc_knee(True, True)
			self.calc_foot(True, True)
			inc_foot_pos = np.copy(self.lfoot_pos)
 
			if (np.fabs(dt_foot_pos[1] - inc_foot_pos[1]) > 0.02 and dt_foot_pos[1] > 0.0):
				self.l_angles[1] = orig_angles[1] + (theta_g + theta_a) * self.dt
				self.l_angles[2] = orig_angles[2] + theta_b * self.dt
 
			self.calc_knee(True, True)
			self.calc_foot(True, True)
 
		elif (self.status == 1):
			self.calc_com(True, False)
			self.calc_knee(True, False)
			self.calc_foot(True, False)
			self.calc_grd_frc()
 
			target_pos = np.array([self.com[1], (self.D + self.lfoot_pos[0]) - self.com[0]])

			l = np.linalg.norm(target_pos)
 
			acos = min(1.0, l**2/(2.0*self.L*l))
			theta_g = np.arctan(target_pos[1]/target_pos[0])
			theta_a = np.arccos(acos)
			theta_b = np.arcsin((l*np.sin(theta_a))/self.L)
 
			orig_angles = np.copy(self.r_angles)
			# set angles based on foot position
			self.r_angles[1] += (theta_g + theta_a) * self.dt
			self.r_angles[2] += theta_b * self.dt
			self.calc_knee(True, False)
			self.calc_foot(True, False)
			dt_foot_pos = np.copy(self.rfoot_pos)
 
			self.r_angles[1] = (theta_g + theta_a)
			self.r_angles[2] = theta_b
			self.calc_knee(True, False)
			self.calc_foot(True, False)
			inc_foot_pos = np.copy(self.rfoot_pos)
 
			if (np.fabs(dt_foot_pos[1] - inc_foot_pos[1]) > 0.02 and dt_foot_pos[1] > 0.0):
				self.r_angles[1] = orig_angles[1] + (theta_g + theta_a) * self.dt
				self.r_angles[2] = orig_angles[2] + theta_b * self.dt
			self.calc_knee(True, False)
			self.calc_foot(True, False)
 
	def finite_differencing(self):
		if (self.status == 0):
			r_knee_orig = self.r_angles[2]
			r_knee_minus = max(0.0, self.r_angles[2] - np.pi/3.0 * self.dt)
			r_knee_plus = min(np.pi/3.0, self.r_angles[2] + np.pi/3.0 * self.dt)
			r_knee_prev_orig = self.prev_r_angles[2]
 
			self.calc_all_vals(True, True)
			self.calc_knee(True, True)
			self.calc_foot(True, True)
			orig_grd_frc = self.grnd_frc_condition()
			orig_ZMP = self.ZMP_condition()
 
			# calculate minus vals
			self.prev_r_angles[2] = r_knee_orig
			self.r_angles[2] = r_knee_minus
			self.calc_all_vals(True, True)
			self.calc_knee(True, True)
			self.calc_foot(True, True)
			minus_grd_frc = self.grnd_frc_condition()
			minus_ZMP = self.ZMP_condition()
			minus_abs_sum = np.fabs(minus_ZMP) + np.fabs(minus_grd_frc)
 
			# calculate plus vals
			self.prev_r_angles[2] = r_knee_orig
			self.r_angles[2] = r_knee_plus
			self.calc_all_vals(True, True)
			self.calc_knee(True, True)
			self.calc_foot(True, True)
			plus_grd_frc = self.grnd_frc_condition()
			plus_ZMP = self.ZMP_condition()
			plus_abs_sum = np.fabs(minus_ZMP) + np.fabs(minus_grd_frc)
 
			if (minus_abs_sum < plus_abs_sum):
				self.r_angles[2] = r_knee_minus
 
			# visualize ZMP point
			self.calc_all_vals(True, True)
			ZMP = self.calc_ZMP()
			plt.plot([ZMP[0]], [ZMP[1]], 'go')
			plt.draw()
 
		elif (self.status == 1):
			l_knee_orig = self.l_angles[2]
			l_knee_minus = max(0.0, self.l_angles[2] - np.pi/3.0 * self.dt)
			l_knee_plus = min(np.pi/3.0, self.l_angles[2] + np.pi/3.0 * self.dt)
			l_knee_prev_orig = self.prev_l_angles[2]
 	
			self.calc_all_vals(True, False)
			self.calc_knee(True, False)
			self.calc_foot(True, False)
			orig_grd_frc = self.grnd_frc_condition()
			orig_ZMP = self.ZMP_condition()
 
			# calculate minus vals
			self.prev_l_angles[2] = l_knee_orig
			self.l_angles[2] = l_knee_minus
			self.calc_all_vals(True, False)
			self.calc_knee(True, False)
			self.calc_foot(True, False)
			minus_grd_frc = self.grnd_frc_condition()
			minus_ZMP = self.ZMP_condition()
			minus_abs_sum = np.fabs(minus_ZMP) + np.fabs(minus_grd_frc)
 
			# calculate plus vals
			self.prev_l_angles[2] = l_knee_orig
			self.l_angles[2] = l_knee_plus
			self.calc_all_vals(True, False)
			self.calc_knee(True, False)
			self.calc_foot(True, False)
			plus_grd_frc = self.grnd_frc_condition()
			plus_ZMP = self.ZMP_condition()
			plus_abs_sum = np.fabs(minus_ZMP) + np.fabs(minus_grd_frc)
 
			if (minus_abs_sum < plus_abs_sum):
				self.l_angles[2] = l_knee_minus
 
			# visualize ZMP point
			self.calc_all_vals(True, False)
			ZMP = self.calc_ZMP()
			plt.plot([ZMP[0]], [ZMP[1]], 'go')
			plt.draw()

		else:
			if (self.prev_status == 0):
				r_knee_orig = self.r_angles[2]
				r_knee_minus = max(0.0, self.r_angles[2] - np.pi/2.0 * self.dt)
				r_knee_plus = min(np.pi/3.0, self.r_angles[2] + np.pi/2.0 * self.dt)
				self.prev_r_angles[2] = r_knee_orig

				#minus vals
				self.r_angles[2] = r_knee_minus
				self.calc_all_vals(False, False)
				self.calc_knee(False, False)
				self.calc_foot(False, False)
				minus_grd_frc = self.grnd_frc_condition()
				minus_ZMP = self.ZMP_double_cond()
				minus_abs_sum = np.fabs(minus_ZMP[0]) + np.fabs(minus_ZMP[1]) + np.fabs(minus_grd_frc)
				minus_foot_pos = np.copy(self.rfoot_pos)

				#plus vals
				self.r_angles[2] = r_knee_plus
				self.calc_all_vals(False, False)
				self.calc_knee(False, False)
				self.calc_foot(False, False)
				plus_grd_frc = self.grnd_frc_condition()
				plus_ZMP = self.ZMP_double_cond()
				plus_abs_sum = np.fabs(plus_ZMP[0]) + np.fabs(plus_ZMP[1]) + np.fabs(plus_grd_frc)
				plus_foot_pos = np.copy(self.rfoot_pos)

				if (plus_foot_pos[1] < 0.0 and minus_foot_pos[1] >= 0.0):
					self.r_angles[2] = r_knee_minus
				elif (minus_ZMP[0] > 0.0 and minus_ZMP[1] > 0.0 and plus_ZMP[0] < 0.0 and plus_ZMP[1] < 0.0):
					self.r_angles[2] = r_knee_minus
				elif (minus_abs_sum < plus_abs_sum):
					self.r_angles[2] = r_knee_minus
	 
				# visualize ZMP point
				self.calc_all_vals(False, False)
				ZMP = self.calc_ZMP()
				plt.plot([ZMP[0]], [ZMP[1]], 'go')
				plt.draw()

	def trajectory(self):
		at_boundary = False
		start_status = self.status
		self.t += self.dt
		self.prev_r_angles = np.copy(self.r_angles)
		self.prev_l_angles = np.copy(self.l_angles)
 
		if (self.status == 0):
			self.r_angles[1] = min(np.pi/3.0, self.r_angles[1] + np.pi/3.0 * self.dt) #increment hip swing
			self.finite_differencing()  
			self.calc_swing_leg_traj()
		elif (self.status == 1):
			self.l_angles[1] = min(np.pi/3.0, self.l_angles[1] + np.pi/3.0 * self.dt) #increment hip swing
			self.finite_differencing()  
			self.calc_swing_leg_traj()
		elif (self.status == 2 and self.prev_status == 0): #still have to fix this
			self.r_angles[1] = max(-self.up_limits[1], self.r_angles[1] + ((-self.up_limits[1] - self.r_angles_bent[1]) / 10.0)) #increment hip swing
			self.r_angles[2] = min(self.up_limits[2], self.r_angles[2] + ((self.up_limits[2] - self.r_angles_bent[2]) / 10.0)) #increment hip swing
			self.l_angles[1] = max(0.0, self.l_angles[1] - self.l_angles_bent[1] / 12.0) #increment hip swing
			self.l_angles[2] = max(0.0, self.l_angles[2] - self.l_angles_bent[2] / 12.0) #increment hip swing
			# if (np.linalg.norm(self.l_angles) > 1e-30):
			self.finite_differencing()
			self.calc_swing_leg_traj()
		elif (self.status == 2 and self.prev_status == 1):
			self.l_angles[1] = max(-self.up_limits[1], self.l_angles[1] + ((-self.up_limits[1] - self.l_angles_bent[1]) / 10.0)) #increment hip swing
			self.l_angles[2] = min(self.up_limits[2], self.l_angles[2] + ((self.up_limits[2] - self.l_angles_bent[2]) / 10.0)) #increment hip swing
			self.r_angles[1] = max(0.0, self.r_angles[1] - self.r_angles_bent[1] / 12.0) #increment hip swing
			self.r_angles[2] = max(0.0, self.r_angles[2] - self.r_angles_bent[2] / 12.0) #increment hip swing
			self.finite_differencing()
			self.calc_swing_leg_traj()

		# print 'com', self.com

		#check state change here	
		if (self.status == 0 and self.lfoot_pos[1] < 1e-6):
			self.status = 2
			self.prev_status = 0
			self.r_angles_bent = np.copy(self.r_angles)
			self.l_angles_bent = np.copy(self.l_angles)
			# 	print 'right leg movement state change'
		elif (self.status == 1 and self.rfoot_pos[1] < 1e-6):
			self.status = 2
			self.prev_status = 1
			self.r_angles_bent = np.copy(self.r_angles)
			self.l_angles_bent = np.copy(self.l_angles)
			# print 'left leg movement state change'
		 
		elif (self.status == 2): #change to 
			if (self.prev_status == 0 and np.linalg.norm(np.subtract(np.fabs(self.r_angles), self.up_limits)) < 1e-24 and np.linalg.norm(self.l_angles) < 1e-30):
				self.status = 1
				self.prev_status = 2
				self.r_angles = np.fabs(self.r_angles)
				# print 'double support phase state change to left leg movement'
			if (self.prev_status == 1 and np.linalg.norm(np.subtract(np.fabs(self.l_angles)	, self.up_limits)) < 1e-24 and np.linalg.norm(self.r_angles) < 1e-30):
				self.status = 0
				self.prev_status = 2
				self.l_angles = np.fabs(self.l_angles)
				# print 'double support phase state change to right  leg movement'
		 
if __name__ == "__main__":
	biped = Biped()
	biped.init()
	biped.draw_biped()
	plt.axis([-5, 5, 0, 5])
	plt.ion()
	plt.show() 
	for i in xrange(100):
		# raw_input('press enter to continue')
		plt.clf()
		plt.axis([-5, 5, -1, 5])
		biped.trajectory()  
		biped.draw_biped()
		time.sleep(0.1)
		# print 'r_angles', biped.r_angles
		# print 'upper up_limits', biped.up_limits
		#raw_input('enter to continue')