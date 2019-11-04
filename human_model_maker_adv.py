#!/usr/bin/env python
import rospy
import numpy as np
import matplotlib.pyplot as plt

#head height, head width
head_inputs = np.zeros(2)
#left and right: arm length & circumference, forearm length & circumference, hand length, width, & height, finger length, width, & height, thumb length, width, & height
arm_inputs = np.zeros(13) #apply for both left and right (assume symmetry)
#pelvis circumference & height, torso circumference & height, chest length, width & height, neck circumference & height
torso_inputs = np.zeros(9)
#unified leg: (multiply values by 2) upper femur circumference & height, lower femur circumference & height, tibia circumference & height, foot length width and height,
leg_inputs = np.zeros(9)

#sample input vectors (comment later)
head_inputs = np.array([0.11, 0.11])
torso_inputs = np.array([0.1295*2.0*np.pi, 0.30, 0.1295*2.0*np.pi, 0.257, 0.20, 0.10, 0.075, 0.073*2.0*np.pi, 0.126])
arm_inputs = np.array([0.053*2.0*np.pi, 0.2475, 0.053*2.0*np.pi, 0.281, 0.0688, 0.048, 0.0275, 0.04515, 0.04935, 0.0152, 0.0447, 0.0124, 0.0156])
leg_inputs = np.array([0.13065*np.pi, 0.18, 0.1005*np.pi, 0.2149, 0.10275*np.pi, 0.3498, 0.1116/2.0, 0.164/2.0, 0.063/2.0])

#default measurement vectors
head_defaults = np.array([0.11, 0.11])
torso_defaults = np.array([0.1295*2.0*np.pi, 0.30, 0.1295*2.0*np.pi, 0.257, 0.20, 0.10, 0.075, 0.073*2.0*np.pi, 0.126])
arm_defaults = np.array([0.053*2.0*np.pi, 0.2475, 0.053*2.0*np.pi, 0.281, 0.0688, 0.048, 0.0275, 0.04515, 0.04935, 0.0152, 0.0447, 0.0124, 0.0156])
leg_defaults = np.array([0.13065*np.pi, 0.18, 0.1005*np.pi, 0.2149, 0.10275*np.pi, 0.3498, 0.1116/2.0, 0.164/2.0, 0.063/2.0])

#calculated traslations
pelvis_body_trans_1_calc = np.array([0.0, 0.0, 0.0])

torso_dummyX_trans_calc = np.array([0.0, 0, 0.0]) #apply to main TorsoDummyX geometry

torso_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to main Torso geometry
torso_1_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to first cylinder subgeometry under Torso
torso_2_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to box subgeometry under Torso
torso_3_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to second cylinder subgeometry under Torso

heady_dummyZ_trans_calc = np.array([0.0, 0, 0.0]) #apply to main HeadDummyZ geometry
head_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to sphere subgeometry in Head

r_shoulder_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to rShoulderDummyX main geometry
l_shoulder_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to rShoulderDummyX main geometry

humerus_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to r/lHumerus cylinder subgeometry
elbow_dummy_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to r/lElbowDummy main geometry
radius_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to r/lRadius cylinder subgeometry
wrist_dummyX_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to r/lWristDummyX main geometry
hand_1_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to r/lHand first box subgeometry
hand_2_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to r/lHand second box subgeometry
hand_3_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to r/lHand third box subgeometry

hip_dummyX_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to HipDummyX main geometry
femur_1_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to femure firrst cylinder subgeometry
femur_2_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to femur second cylinder subgeometry
tibia_trans_calc = np.array([0.0,  0.0, 0.0]) #apply to Tibia main geometry
tibia_1_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to Tibia cylinder subgeometry
ankle_dummyX_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to AnkleDummyX main geometry
foot_1_trans_calc = np.array([0.0, 0.0, 0.0]) #apply to box Foot subgeometry 

#translation vectors
pelvis_body_trans_1 = np.array([0.0, 0.0, -0.05]) #might not be needed, apply to cylinder sub-geometry under PelvisBody

torso_dummyX_trans = np.array([0.037432, 0.0, -0.041749]) #apply to main TorsoDummyX geometry

torso_trans = np.array([0.0, -0.08, 0.0]) #apply to main Torso geometry
torso_1_trans = np.array([-0.026786, 0.0, 0.10]) #apply to first cylinder subgeometry under Torso
torso_2_trans = np.array([-0.026786, 0.0, 0.307613]) #apply to box subgeometry under Torso
torso_3_trans = np.array([-0.026786, 0.0, 0.400478]) #apply to second cylinder subgeometry under Torso

heady_dummyZ_trans = np.array([-0.026786, 0.0, 0.454217]) #apply to main HeadDummyZ geometry
head_trans = np.array([0.034094, 0.0, 0.088688]) #apply to sphere subgeometry in Head

r_shoulder_trans = np.array([-0.048632, -0.23982, 0.288822]) #apply to rShoulderDummyX main geometry
l_shoulder_trans = np.array([-0.048632, 0.23982, 0.288822]) #apply to rShoulderDummyX main geometry

humerus_trans = np.array([0.0, 0.08, 0.0]) #apply to r/lHumerus cylinder subgeometry
elbow_dummy_trans = np.array([0.004167, 0.206608, 0.001653]) #apply to r/lElbowDummy main geometry
radius_trans = np.array([0.010577, 0.129127, 0.001946]) #apply to r/lRadius cylinder subgeometry
wrist_dummyX_trans = np.array([0.002774, 0.250572, 0.004556]) #apply to r/lWristDummyX main geometry
hand_1_trans = np.array([-0.006131, 0.056806, 0.01241]) #apply to r/lHand first box subgeometry
hand_2_trans = np.array([-0.006131, 0.160954, 0.037292]) #apply to r/lHand second box subgeometry
hand_3_trans = np.array([-0.06748, 0.08632, 0.002815]) #apply to r/lHand third box subgeometry

hip_dummyX_trans = np.array([0.022487, 0.0, -0.086017]) #apply to HipDummyX main geometry
femur_1_trans = np.array([0.001611, 0.0, -0.19619]) #apply to femure firrst cylinder subgeometry
femur_2_trans = np.array([-0.012441, 0.0, -0.390045]) #apply to femur second cylinder subgeometry
tibia_trans = np.array([-0.024908,  0.0, -0.468294]) #apply to Tibia main geometry
tibia_1_trans = np.array([-0.010975, 0.0, -0.205403]) #apply to Tibia cylinder subgeometry
ankle_dummyX_trans = np.array([-0.013991, 0.0, -0.388599]) #apply to AnkleDummyX main geometry
foot_1_trans = np.array([0.079913, 0.0, -0.049723]) #apply to box Foot subgeometry 

def calculate_values():
	pelvis_body_trans_calc[2] = pelvis_body_trans[2] + (0.5 * torso_inputs[1])
		 


def print_model(mode = 0):
	print ('<!-- Exported at: 10/6/2012 6:01:17 PM -->\n<robot name="human_model" >\n<kinbody name="human_kinbody">')
	print ('\n    <modelsdir>models</modelsdir>\n')

	#print base
	print ('	<body name="Base">')
	print ('		<!--Body_Torso Parent Center of Mass to Base -->')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print pelvis dummy trans x
	print ('	<body name="PlevisDummyTransX">')
	print ('		<offsetfrom>Base</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print pelvis dummy trans y
	print ('	<body name="PlevisDummyTransY">')
	print ('		<offsetfrom>PlevisDummyTransX</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print pelvis dummy trans z
	print ('	<body name="PlevisDummyTransZ">')
	print ('		<offsetfrom>PlevisDummyTransY</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('		</geom>')
	print ('	</body>\n')

	#print pelvis dummy rot x
	print ('	<body name="PlevisDummyRotX">')
	print ('		<offsetfrom>PlevisDummyTransZ</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('		</geom>')
	print ('	</body>\n')

	#print pelvis dummy rot y
	print ('	<body name="PlevisDummyRotY">')
	print ('		<offsetfrom>PlevisDummyRotX</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('		</geom>')
	print ('	</body>\n')

	#print pelvis body
	print ('	<body name="PelvisBody">')
	print ('		<!--Body_Torso Parent Center of Mass to Base -->')
	print ('		<offsetfrom>PlevisDummyRotY</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="cylinder">')
	# print ('			<translation>0 0 -0.05</translation>')
	pelvis_body_trans_1_calc[2] = pelvis_body_trans_1[2] + 0.5*(torso_inputs[1] - torso_defaults[1])
	print ('			<translation>0 0 %.4f</translation>' %pelvis_body_trans_1_calc[2])
	print ('			<rotationaxis>1 0 0 90</rotationaxis>')
	print ('			<radius>%.4f</radius>' %(torso_inputs[0] / (2.0 * np.pi)))
	print ('			<height>%.4f</height>' %torso_inputs[1])
	print ('			<diffuseColor>0.3 0.3 0.3</diffuseColor>')
	print ('		</geom>')
	print ('	</body>\n')

	#print torso components
	print ('	<!-- ******************* Torso ********************************** -->')
	print ('	<!-- *********************************************************** -->')

	#print torso dummy x
	torso_trans_calc[2] = 0.5*(torso_inputs[1] - torso_defaults[1]) + torso_dummyX_trans[2]
	print ('	<body name="TorsoDummyX">')
	print ('		<offsetfrom>PelvisBody</offsetfrom>')
	# print ('		<translation>0.037432 0 -0.041749</translation>')
	print ('		<translation>0.037432 0 %.4f</translation>' %torso_trans_calc[2])
	print ('		<rotationaxis>1 0 0 90</rotationaxis>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print torso dummy y
	print ('	<body name="TorsoDummyY">')
	print ('		<offsetfrom>TorsoDummyX</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print torso dummy z
	print ('	<body name="TorsoDummyZ">')
	print ('		<offsetfrom>TorsoDummyY</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('		</geom>')
	print ('	</body>\n')

	#print torso dummy trans x
	print ('	<body name="TorsoDummyTransX">')
	print ('		<offsetfrom>TorsoDummyZ</offsetfrom>')
	print ('		<translation>0.037432 0 -0.041749</translation>')
	print ('		<rotationaxis>1 0 0 90</rotationaxis>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print torso dummy trans y
	print ('	<body name="TorsoDummyTransY">')
	print ('		<offsetfrom>TorsoDummyTransX</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print torso dummy trans z
	print ('	<body name="TorsoDummyTransZ">')
	print ('		<offsetfrom>TorsoDummyTransY</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print torso
	print ('	<body name="Torso">')
	print ('		<offsetfrom>TorsoDummyZ</offsetfrom>')
	print ('		<translation>0 -0.08 0</translation>')
	print ('		<rotationaxis>1 0 0 -90</rotationaxis>\n')

	print ('		<geom type="cylinder">')
	print ('			<!-- <translation>0 -.01 .10</translation> -->')
	# print ('			<translation>-0.026786 0.0 .10</translation>')
	torso_1_trans_calc[2] = 0.5*(torso_inputs[3]-torso_defaults[3]) + torso_1_trans[2]
	print ('			<translation>-0.026786 0.0 %.4f</translation>' %torso_1_trans_calc[2])
	print ('			<rotationaxis>1 0 0 90</rotationaxis>')
	print ('			<radius>%.4f</radius>' %(torso_inputs[2] / (2.0 * np.pi)))
	print ('			<height>%.4f</height>' %torso_inputs[3])
	print ('			<diffuseColor>0.800 0.000 0.0100</diffuseColor>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('		<geom type="box">')
	print ('			<!-- <translation>-0.026786 -0.004374 0.307613</translation> -->')
	# print ('			<translation>-0.026786 0.0 0.307613</translation>')
	torso_2_trans_calc[2] = (torso_inputs[6]-torso_defaults[6]) + torso_2_trans[2]
	print ('			<translation>-0.026786 0.0 %.4f</translation>' %torso_2_trans_calc[2])
	print ('			<rotationaxis>0 0 1 90</rotationaxis>')
	print ('			<!-- <extents>0.20 0.10 0.075</extents> -->')
	print ('			<!-- <extents>0.24 0.10 0.065</extents> -->')
	print ('			<extents>%.4f %.4f %.4f</extents>' %(torso_inputs[4], torso_inputs[5], torso_inputs[6]))
	print ('			<diffuseColor>0.800 0.000 0.0100</diffuseColor>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('		<geom type="cylinder">')
	print ('			<!-- <translation>-0.02359 -0.004374 0.400478</translation> -->')
	print ('			<!-- <translation>-0.026786 -0.004374 0.400478</translation> -->')
	# print ('			<translation>-0.026786 0.0 0.400478</translation>')
	torso_3_trans_calc[2] = 0.5*(torso_inputs[8]-torso_defaults[8]) + torso_3_trans[2]
	print ('			<translation>-0.026786 0.0 %.4f</translation>' torso_3_trans_calc[2])
	print ('			<rotationaxis>1 0 0 90</rotationaxis>')
	print ('			<radius>%.4f</radius>' %(torso_inputs[7] / (2.0 * np.pi)))
	print ('			<height>%.4f</height>' %torso_inputs[8])
	print ('			<diffuseColor>0.901961 0.772549 0.694118</diffuseColor>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('	</body>')

	#print head components
	print ('	<!-- ******************* Head ********************************** -->')
	print ('	<!-- *********************************************************** -->')

	#print head dummy z
	print ('	<body name="HeadDummyZ">')
	print ('		<offsetfrom>Torso</offsetfrom>')
	# print ('		<translation>-0.026786 0 0.454217</translation>')
	heady_dummyZ_trans_calc[2] = 0.5*(torso_inputs[8]) +torso_3_trans_calc[2] + heady_dummyZ_trans[2]
	print ('		<translation>-0.026786 0 %.4f</translation>' heady_dummyZ_trans_calc[2])
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print head dummy y
	print ('	<body name="HeadDummyY">')
	print ('		<offsetfrom>HeadDummyZ</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print head 
	print ('	<body name="Head">')
	print ('		<offsetfrom>HeadDummyY</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	# print ('			<translation>0.034094 0.0 0.088688</translation>')
	head_trans_calc[2] = head_inputs[1] + head_trans[2]
	print ('			<translation>0.034094 0.0 %.4f</translation>' head_trans_calc[2])
	print ('			<!-- original y = 0.004925 -->')
	print ('			<radius>%.4f</radius>' %(np.max(head_inputs)))
	print ('			<diffuseColor>0.901961 0.772549 0.694118</diffuseColor>')
	print ('			<transparency>0.5</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print right arm
	print('		<!-- ******************* RIGHT ARM ***************************** -->')
	print('		<!-- *********************************************************** -->')

	#print rShoulderDummyX
	print ('	<body name="rShoulderDummyX">')
	print ('		<offsetfrom>Torso</offsetfrom>')
	print ('		<rotationaxis>1 0 0 -90</rotationaxis>')
	# print ('		<translation>-0.048632 -0.23982 0.288822</translation>')
	r_shoulder_trans_calc[1] = -(torso_inputs[6] - torso_defaults[6]) + r_shoulder_trans[1]
	r_shoulder_trans_calc[2] = (torso_2_trans_calc[2] - torso_2_trans[2]) + r_shoulder_trans[2]
	print ('		<translation>-0.048632 %.4f %.4f</translation>' %(r_shoulder_trans_calc[1], r_shoulder_trans_calc[2]))
	print ('		<rotationaxis>0 0 1 180</rotationaxis>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print rShoulderDummyZ
	print ('	<body name="rShoulderDummyZ">')
	print ('		<offsetfrom>rShoulderDummyX</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print rHumerus
	print ('	<body name="rHumerus">')
	print ('		<offsetfrom>rShoulderDummyZ</offsetfrom>')
	print ('		<translation>0 0 0</translation>')
	print ('		<geom type="cylinder">')
	# print ('			<translation>0 .08 0</translation>')
	humerus_trans_calc[2] = 0.5*(arm_inputs[1] - arm_defaults[1]) + humerus_trans[2]
	print ('			<translation>0 .08 %.4f</translation>' %humerus_trans_calc[2])
	print ('			<radius>%.4f</radius>' %(arm_inputs[0] / (2.0 * np.pi)))
	print ('			<height>%.4f</height>' %arm_inputs[1])
	print ('			<diffuseColor>0.800 0.000 0.0100</diffuseColor>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print rElbowDummy
	print ('	<body name="rElbowDummy">')
	print ('		<offsetfrom>rHumerus</offsetfrom>')
	# print ('		<translation>0.004167 0.206608 0.001653</translation>')
	elbow_dummy_trans_calc[1] = (arm_inputs[1] - arm_defaults[1]) + elbow_dummy_trans[1]
	print ('		<translation>0.004167 %.4f 0.001653</translation>' elbow_dummy_trans_calc[1])
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print rRadius
	print ('	<body name="rRadius">')
	print ('		<offsetfrom>rElbowDummy</offsetfrom>')
	print ('		<translation>0 0 0</translation>')
	print ('		<geom type="cylinder">')
	# print ('			<translation>0.010577 0.129127 0.001946</translation>')
	radius_trans_calc[1] = 0.5*(arm_inputs[3] - arm_defaults[3]) + radius_trans[1]
	print ('			<translation>0.010577 %.4f 0.001946</translation>' radius_trans_calc[1])
	print ('			<radius>%.4f</radius>' %(arm_inputs[2] / (2.0 * np.pi)))
	print ('			<height>%.4f</height>' %arm_inputs[3])
	print ('			<diffuseColor>0.901961 0.772549 0.694118</diffuseColor>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print rWristDummyX
	print ('	<body name="rWristDummyX">')
	print ('		<offsetfrom>rRadius</offsetfrom>')
	# print ('		<translation>0.002774 0.250572 0.004556</translation>')
	wrist_dummyX_trans_calc[2] = 0.5*(arm_inputs[3] - arm_defaults[3]) + wrist_dummyX_trans[2]
	print ('		<translation>0.002774 0.250572 %.4f</translation>' %wrist_dummyX_trans_calc[2])
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print rWristDummyY
	print ('	<body name="rWristDummyY">')
	print ('		<offsetfrom>rWristDummyX</offsetfrom>')
	print ('		<translation>0 0 0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('	</body>\n')
	
	#print rhand
	print ('	<body name="rHand">')
	print ('		<offsetfrom>rWristDummyY</offsetfrom>')
	print ('		<geom type="box">')
	# print ('			<translation>-0.006131 0.056806 0.01241</translation>')
	hand_1_trans_calc[1] = (arm_inputs[4] - arm_defaults[4]) + hand_1_trans[1]
	print ('			<translation>-0.006131 %.4f 0.01241</translation>' %hand_1_trans_calc[1])
	print ('			<rotationaxis>0 0 1 90</rotationaxis>')
	print ('			<extents>%.4f %.4f %.4f</extents>' %(arm_inputs[4], arm_inputs[5], arm_inputs[6]))
	print ('			<diffuseColor>0.901961 0.772549 0.694118</diffuseColor>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('		<geom type="box">    ')
	# print ('			<translation>-0.006131 0.160954 0.037292</translation>')
	hand_2_trans_calc[1] = (hand_1_trans_calc[1] - hand_1_trans[1]) + (arm_inputs[7] - arm_defaults[7]) + hand_2_trans[1]
	print ('			<translation>-0.006131 %.4f 0.037292</translation>' %hand_2_trans_calc[1])
	print ('			<rotationaxis>0 0 1 90</rotationaxis>')
	print ('			<extents>%.4f %.4f %.4f</extents>' %(arm_inputs[7], arm_inputs[8], arm_inputs[9]))
	print ('			<diffuseColor>0.901961 0.772549 0.694118</diffuseColor>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('		<geom type="box">    ')
	# print ('			<translation>-0.06748 0.08632 0.002815</translation>')
	hand_3_trans_calc[1] = (hand_1_trans_calc[1] - hand_1_trans[1]) + (arm_inputs[10] - arm_defaults[10]) + hand_3_trans[1]
	print ('			<translation>-0.06748 %.4f 0.002815</translation>' %hand_3_trans_calc[1])
	print ('			<rotationaxis>0 0 1 90</rotationaxis>')
	print ('			<extents>%.4f %.4f %.4f</extents>' %(arm_inputs[10], arm_inputs[11], arm_inputs[12]))
	print ('			<diffuseColor>0.901961 0.772549 0.694118</diffuseColor>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('	</body>\n')



	#print left arm
	print ('		<!-- ******************* LEFT ARM ***************************** -->')
	print ('		<!-- *********************************************************** -->')

	#print lShoulderDummyX
	print ('	<body name="lShoulderDummyX">')
	print ('		<offsetfrom>Torso</offsetfrom>')
	print ('		<rotationaxis>1 0 0 -90</rotationaxis>')
	# print ('		<translation>-0.048632  0.23982 0.288822</translation>')
	l_shoulder_trans_calc[1] = (torso_inputs[6] - torso_defaults[6]) + l_shoulder_trans[1]
	l_shoulder_trans_calc[2] = (torso_2_trans_calc[2] - torso_2_trans[2]) + l_shoulder_trans[2]
	print ('		<translation>-0.048632  %.4f %.4f</translation>' %(l_shoulder_trans_calc[1], l_shoulder_trans_calc[2]))
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>    \n')

	#print lShoulderDummyZ
	print ('	<body name="lShoulderDummyZ">')
	print ('		<offsetfrom>lShoulderDummyX</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print lHumerus
	print ('	<body name="lHumerus">')
	print ('		<offsetfrom>lShoulderDummyZ</offsetfrom>')
	print ('		<translation>0 0 0</translation>')
	print ('		<geom type="cylinder">')
	# print ('			<translation>0 .08 0</translation> <!-- Why ??? ... -->            ')
	print ('			<translation>0 .08 %.4f</translation>' %humerus_trans_calc[2])
	print ('			<!--            <translation>0.0112 -0.428571 0.23982</translation>-->')
	print ('			<radius>%.4f</radius>' %(arm_inputs[0] / (2.0 * np.pi)))
	print ('			<height>%.4f</height>' %arm_inputs[1])
	print ('			<diffuseColor>0.800 0.000 0.0100</diffuseColor>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print lElbowDummy
	print ('	<body name="lElbowDummy">')
	print ('		<offsetfrom>lHumerus</offsetfrom>')
	# print ('		<translation>0.004167 0.206608 0.001653</translation>')
	print ('		<translation>0.004167 %.4f 0.001653</translation>' %elbow_dummy_trans_calc[1])
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')
	
	#print lRadius
	print ('	<body name="lRadius">')
	print ('		<offsetfrom>lElbowDummy</offsetfrom>')
	print ('		<translation>0 0 0</translation>')
	print ('		<geom type="cylinder">')
	# print ('			<translation>0.010577 0.129127 0.001946</translation>')
	print ('			<translation>0.010577 %.4f 0.001946</translation>' radius_trans_calc[1])
	print ('			<!--<rotationaxis>1 0 0 90</rotationaxis> -->')
	print ('			<radius>%.4f</radius>' %(arm_inputs[2] / (2.0 * np.pi)))
	print ('			<height>%.4f</height>' %arm_inputs[3])
	print ('			<diffuseColor>0.901961 0.772549 0.694118</diffuseColor>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print lWristDummyX
	print ('	<body name="lWristDummyX">')
	print ('		<offsetfrom>lRadius</offsetfrom>')
	# print ('		<translation>0.002774 0.250572 0.004556</translation>')
	print ('		<translation>0.002774 0.250572 %.4f</translation>' wrist_dummyX_trans_calc[2])
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('	</body>    \n')

	#print lWristDummyY
	print ('	<body name="lWristDummyY">')
	print ('		<offsetfrom>lWristDummyX</offsetfrom>')
	print ('		<translation>0.0 0.0 0.0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.02</radius>')
	print ('			<transparency>1</transparency>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('	</body>\n')
	
	#print lHand
	print ('	<body name="lHand">')
	print ('		<offsetfrom>lWristDummyY</offsetfrom>')
	print ('		<translation>0 0 0</translation>')
	print ('		<geom type="box">    ')
	# print ('			<translation>0.006131 0.056806 0.01241</translation>')
	print ('			<translation>0.006131 %.4f 0.01241</translation>' %hand_1_trans_calc[1])
	print ('			<rotationaxis>0 0 1 90</rotationaxis>')
	print ('			<extents>%.4f %.4f %.4f</extents>' %(arm_inputs[4], arm_inputs[5], arm_inputs[6]))
	print ('			<diffuseColor>0.901961 0.772549 0.694118</diffuseColor>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('		<geom type="box">    ')
	# print ('			<translation>0.006131 0.160954 0.037292</translation>')
	print ('			<translation>0.006131 %.4f 0.037292</translation>' %hand_2_trans_calc[1])
	print ('			<rotationaxis>0 0 1 90</rotationaxis>')
	print ('			<extents>%.4f %.4f %.4f</extents>' %(arm_inputs[7], arm_inputs[8], arm_inputs[9]))
	print ('			<diffuseColor>0.901961 0.772549 0.694118</diffuseColor>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('		<geom type="box">    ')
	# print ('			<translation>0.06748 0.08632 0.002815</translation>')
	print ('			<translation>0.06748 %.4f 0.002815</translation>' %hand_3_trans_calc[1])
	print ('			<rotationaxis>0 0 1 90</rotationaxis>')
	print ('			<extents>%.4f %.4f %.4f</extents>' %(arm_inputs[12], arm_inputs[11], arm_inputs[12]))
	print ('			<diffuseColor>0.901961 0.772549 0.694118</diffuseColor>')
	print ('			<transparency>0.8</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print unified leg
	print ('	<!-- ******************* UNIFIED LEG ***************************** -->')
	print ('	<!-- *********************************************************** -->\n')

	#print HipDummyX
	print ('	<body name="HipDummyX">')
	print ('		<offsetfrom>PelvisBody</offsetfrom>')
	print ('		<translation>0.022487 0 -0.086017</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.03</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')
	
	#print HipDummyY
	print ('	<body name="HipDummyY">')
	print ('		<offsetfrom>HipDummyX</offsetfrom>')
	print ('		<translation>0 0 0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.03</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print Femur
	print ('	<body name="Femur">')
	print ('		<offsetfrom>HipDummyX</offsetfrom>')
	print ('		<translation>0 0 0</translation>')
	print ('		<geom type="cylinder">')
	# print ('			<translation>0.001611 0 -0.19619</translation>')
	femur_1_trans_calc[2] = (-leg_inputs[1] + leg_defaults[1]) + femur_1_trans[2]
	print ('			<translation>0.001611 0 %.4f</translation>' %femur_1_trans_calc[2])
	print ('			<rotationaxis>1 0 0 90</rotationaxis>')
	print ('			<radius>%.4f</radius>' %(leg_inputs[0]/np.pi))
	print ('			<height>%.4f</height>' %leg_inputs[1])
	print ('			<diffuseColor>0.3 0.3 0.3</diffuseColor>')
	print ('		</geom>')
	print ('		<geom type="cylinder">')
	# print ('			<translation>-0.012441 0 -0.390045</translation>')
	femur_2_trans_calc[2] = (-leg_inputs[3] + leg_defaults[3]) + femur_2_trans[2]
	print ('			<translation>-0.012441 0 %.4f</translation>' %femur_2_trans_calc[2])
	print ('			<rotationaxis>1 0 0 90</rotationaxis>')
	print ('			<radius>%.4f</radius>' %(leg_inputs[2]/np.pi))
	print ('			<height>%.4f</height>' %leg_inputs[3])
	print ('			<diffuseColor>0.3 0.3 0.3</diffuseColor>')
	print ('		</geom>')
	print ('	</body>\n')
	
	#print Tibia
	print ('	<body name="Tibia">')
	print ('		<offsetfrom>Femur</offsetfrom>')
	# print ('		<translation>-0.024908  0 -0.468294</translation>')
	tibia_trans_calc[2] = 0.5*(leg_defaults[3] - leg_inputs[3]) + tibia_trans[2]
	print ('		<translation>-0.024908  0 %.4f</translation>' %tibia_trans_calc[2])
	print ('		<geom type="cylinder">')
	# print ('			<translation>-0.010975 0 -0.205403</translation>')
	tibia_1_trans_calc[2] = 0.5*(leg_defaults[5] - leg_inputs[5]) + tibia_1_trans[2]
	print ('			<translation>-0.010975 0 %.4f</translation>' %tibia_1_trans_calc[2])
	print ('			<rotationaxis>1 0 0 90</rotationaxis>')
	print ('			<radius>%.4f</radius>' %(leg_inputs[4]/np.pi))
	print ('			<height>%.4f</height>' %leg_inputs[5])
	print ('			<diffuseColor>0.3 0.3 0.3</diffuseColor>')
	print ('		</geom>')
	print ('	</body>\n')
 
 	#print AnkleDummyX
	print ('	<body name="AnkleDummyX">')
	print ('		<offsetfrom>Tibia</offsetfrom>')
	# print ('		<translation>-0.013991 0 -0.388599</translation>')
	ankle_dummyX_trans_calc[2] = (leg_defaults[5] - leg_inputs[5]) + ankle_dummyX_trans[2]
	print ('		<translation>-0.013991 0 %.4f</translation>' %ankle_dummyX_trans[2])
	print ('		<geom type="sphere">')
	print ('			<radius>0.03</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>   \n')
	
	#print AnkleDummyY
	print ('	<body name="AnkleDummyY">')
	print ('		<offsetfrom>AnkleDummyX</offsetfrom>')
	print ('		<translation>0 0 0</translation>')
	print ('		<geom type="sphere">')
	print ('			<radius>0.03</radius>')
	print ('			<transparency>1</transparency>')
	print ('		</geom>')
	print ('	</body>\n')

	#print Foot
	print ('	<body name="Foot">')
	print ('		<offsetfrom>AnkleDummyY</offsetfrom>')
	print ('		<translation>0 0 0</translation>')
	print ('		<geom type="box">    ')
	# print ('			<translation>0.079913 0 -0.049723</translation>')
	foot_1_trans_calc[2] = foot_1_trans[2] + (leg_inputs[8] - leg_defaults[8])
	print ('			<translation>0.079913 0 %.4f</translation>' foot_1_trans_calc[2])
	print ('			<rotationaxis>0 0 1 90</rotationaxis>')
	print ('			<extents>%.4f %.4f %.4f</extents>' %(leg_inputs[6]*2.0, leg_inputs[7]*2.0, leg_inputs[8]*2.0))
	print ('			<diffuseColor>0.3 0.3 0.3</diffuseColor>')
	print ('		</geom>')
	print ('	</body>\n')
	
	#print joints
	print ('	<!--*********************************************************************-->')
	print ('	<!--*********************************************************************-->')
	print ('	<!--*********************************************************************-->')
	print ('	<!--*********************************************************************-->')
	print ('	<!--*********************************************************************-->')
	print ('	<!--*********************************************************************-->\n')
 
	print ('	<joint name="PelvisTransX" type="slider">')
	print ('		<body>Base</body>')
	print ('		<body>PlevisDummyTransX</body>')
	print ('		<offsetfrom>PlevisDummyTransX</offsetfrom>')
	print ('		<axis>1 0 0</axis>')
	print ('		<limits>-30 30</limits>')
	print ('	</joint>\n')

	print ('	<joint name="PelvisTransY" type="slider">')
	print ('		<body>PlevisDummyTransX</body>')
	print ('		<body>PlevisDummyTransY</body>')
	print ('		<offsetfrom>PlevisDummyTransY</offsetfrom>')
	print ('		<!--        <anchor>0 0 0</anchor>-->')
	print ('		<axis>0 1 0</axis>')
	print ('		<limits>-30 30</limits>')
	print ('	</joint>\n')

	print ('	<joint name="PelvisTransZ" type="slider">')
	print ('		<body>PlevisDummyTransY</body>')
	print ('		<body>PlevisDummyTransZ</body>')
	print ('		<offsetfrom>PlevisDummyTransZ</offsetfrom>')
	print ('		<!--        <anchor>0 0 0</anchor>-->')
	print ('		<axis>0 0 1</axis>')
	print ('		<limits>-30 30</limits>')
	print ('	</joint>\n')

	
	print ('	<joint name="PelvisRotX" type="hinge">')
	print ('		<body>PlevisDummyTransZ</body>')
	print ('		<body>PlevisDummyRotX</body>')
	print ('		<offsetfrom>PlevisDummyRotX</offsetfrom>')
	print ('		!--        <anchor>0 0 0</anchor>-->')
	print ('		<axis>1 0 0</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')

	print ('	<joint name="PelvisRotY" type="hinge">')
	print ('		<body>PlevisDummyRotX</body>')
	print ('		<body>PlevisDummyRotY</body>')
	print ('		<offsetfrom>PlevisDummyRotY</offsetfrom>')
	print ('		<!--        <anchor>0 0 0</anchor>-->')
	print ('		<axis>0 1 0</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')
	
	print ('	<joint name="PelvisRotZ" type="hinge">')
	print ('		<body>PlevisDummyRotY</body>')
	print ('		<body>PelvisBody</body>')
	print ('		<offsetfrom>PelvisBody</offsetfrom>')
	print ('		<!--        <anchor>0.037432 0 0.139749</anchor>-->')
	print ('		<axis>0 0 1</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')

	print ('	<joint name="TorsoX" type="hinge">')
	print ('		<body>PelvisBody</body>')
	print ('		<body>TorsoDummyX</body>')
	print ('		<offsetfrom>TorsoDummyX</offsetfrom>')
	print ('		<!--        <anchor>0.037432 0 0.139749</anchor>-->')
	print ('		<axis>1 0 0</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')
	
	print ('	<joint name="TorsoZ" type="hinge">')
	print ('		<body>TorsoDummyX</body>')
	print ('		<body>TorsoDummyY</body>')
	print ('		<offsetfrom>TorsoDummyY</offsetfrom>')
	print ('		<!--        <anchor>0.037432 0 0.139749</anchor>-->')
	print ('		<axis>0 0 1</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')
	
	print ('	<joint name="TorsoY" type="hinge">')
	print ('		<body>TorsoDummyY</body>')
	print ('		<body>TorsoDummyZ</body>')
	print ('		<offsetfrom>TorsoDummyZ</offsetfrom>\n')
	print ('		<!--        <anchor>0.037432 0 0.139749</anchor>-->')
	print ('		<axis>0 1 0</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')

	print ('	<joint name="rShoulderTransX" type="slider">')
	print ('		<body>TorsoDummyZ</body>')
	print ('		<body>TorsoDummyTransX</body>')
	print ('		<offsetfrom>TorsoDummyTransX</offsetfrom>')
	print ('		<axis>1 0 0</axis>')
	print ('		<limits>-0.50 0.50</limits>')
	print ('	</joint>\n')
	
	print ('	<joint name="rShoulderTransY" type="slider">')
	print ('		<body>TorsoDummyTransX</body>')
	print ('		<body>TorsoDummyTransY</body>')
	print ('		<offsetfrom>TorsoDummyTransY</offsetfrom>')
	print ('		<axis>0 1 0</axis>')
	print ('		<limits>-0.50 0.50</limits>')
	print ('	</joint>\n')
	
	print ('	<joint name="rShoulderTransZ" type="slider">')
	print ('		<body>TorsoDummyTransY</body>')
	print ('		<body>TorsoDummyTransZ</body>')
	print ('		<offsetfrom>TorsoDummyTransZ</offsetfrom>')
	print ('		<axis>0 0 1</axis>')
	print ('		<limits>-0.50 0.50</limits>')
	print ('	</joint>\n')

	print ('	<joint name="TorsoTrans" type="slider">')
	print ('		<body>TorsoDummyZ</body>')
	print ('		<body>Torso</body>')
	print ('		<offsetfrom>Torso</offsetfrom>')
	print ('		<axis>0 0 1</axis>')
	print ('		<limits>-0.50 0.50</limits>')
	print ('	</joint>\n')
	
	print ('	<joint name="HeadZ" type="hinge">')
	print ('		<body>Torso</body>')
	print ('		<body>HeadDummyZ</body>')
	print ('		<offsetfrom>HeadDummyZ</offsetfrom>')
	print ('		<!--        <anchor>0.023497 0 0.593966</anchor>-->')
	print ('		<axis>0 0 1</axis>')
	print ('		<limitsdeg>-45 45</limitsdeg>')
	print ('	</joint>\n')

	print ('	<joint name="HeadY" type="hinge">')
	print ('		<body>HeadDummyZ</body>')
	print ('		<body>HeadDummyY</body>')
	print ('		<offsetfrom>HeadDummyY</offsetfrom>')
	print ('		<!--        <anchor>0.023497 0 0.593966</anchor>-->')
	print ('		<axis>0 -1 0</axis>')
	print ('		<limitsdeg>-60 30</limitsdeg>')
	print ('	</joint>\n')
	
	print ('	<joint name="HeadX" type="hinge">')
	print ('		<body>HeadDummyY</body>')
	print ('		<body>Head</body>')
	print ('		<offsetfrom>Head</offsetfrom>')
	print ('		<!--        <anchor>0.023497 0 0.593966</anchor>-->')
	print ('		<axis>1 0 0</axis>')
	print ('		<limitsdeg>-45 45</limitsdeg>')
	print ('	</joint>\n')

	print ('	<!--     <joint name="ForeheadC" type="hinge">')
	print ('		<body>Head</body>')
	print ('		<body>forehead</body>')
	print ('		<offsetfrom>Head</offsetfrom>')
	print ('		<axis>1 0 0</axis>')
	print ('		<limitsdeg>-45 45</limitsdeg>')
	print ('	</joint> -->\n')
	
	print ('	<!-- ******************* RIGHT ARM ***************************** -->')
	print ('	<!-- *********************************************************** -->\n')

	print ('	<joint name="rShoulderX" type="hinge">')
	print ('		<body>Torso</body>')
	print ('		<body>rShoulderDummyX</body>')
	print ('		<offsetfrom>rShoulderDummyX</offsetfrom>')
	print ('		<!--        <anchor>-0.0112 0.23982 0.428571</anchor>-->')
	print ('		<axis>1 0 0</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')
	
	print ('	<joint name="rShoulderZ" type="hinge">')
	print ('		<body>rShoulderDummyX</body>')
	print ('		<body>rShoulderDummyZ</body>')
	print ('		<offsetfrom>rShoulderDummyZ</offsetfrom>')
	print ('		<!--        <anchor>-0.0112 0.23982 0.428571</anchor>-->')
	print ('		<axis>0 0 1</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')
	print ('	<joint name="rShoulderY" type="hinge">')
	print ('		<body>rShoulderDummyZ</body>')
	print ('		<body>rHumerus</body>')
	print ('		<offsetfrom>rHumerus</offsetfrom>')
	print ('		<!--        <anchor>-0.0112 0.23982 0.428571</anchor>-->')
	print ('		<axis>0 -1 0</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')

	print ('	<joint name="rArmTrans" type="slider">')
	print ('		<body>rHumerus</body>')
	print ('		<body>rElbowDummy</body>')
	print ('		<offsetfrom>rElbowDummy</offsetfrom>')
	print ('		<!--        <anchor>-0.007033 0.446428 0.430224</anchor>-->')
	print ('		<axis>0 1 0</axis>')
	print ('		<limits>-0.50 0.50</limits>')
	print ('	</joint>\n')
	
	print ('	<joint name="rElbowZ" type="hinge">')
	print ('		<body>rElbowDummy</body>')
	print ('		<body>rRadius</body>')
	print ('		<offsetfrom>rRadius</offsetfrom>')
	print ('		<!--        <anchor>-0.007033 0.446428 0.430224</anchor>-->')
	print ('		<axis>0 0 1</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')
	
	print ('	<joint name="rWristX" type="hinge">')
	print ('		<body>rRadius</body>')
	print ('		<body>rWristDummyX</body>')
	print ('		<offsetfrom>rWristDummyX</offsetfrom>')
	print ('		<!--        <anchor>-0.004259 0.697 0.43478</anchor>-->')
	print ('		<axis>-1 0 0</axis>')
	print ('		<limitsdeg>-90 90</limitsdeg>')
	print ('	</joint>\n')

	print ('	<joint name="rWristY" type="hinge">')
	print ('		<body>rWristDummyX</body>')
	print ('		<body>rWristDummyY</body>')
	print ('		<offsetfrom>rWristDummyY</offsetfrom>')
	print ('		<!--        <anchor>-0.004259 0.697 0.43478</anchor>-->')
	print ('		<axis>0 -1 0</axis>')
	print ('		<limitsdeg>-180 0</limitsdeg>')
	print ('	</joint>\n')
	
	print ('	<joint name="rWristZ" type="hinge">')
	print ('		<body>rWristDummyY</body>')
	print ('		<body>rHand</body>')
	print ('		<offsetfrom>rHand</offsetfrom>')
	print ('		<!--        <anchor>-0.004259 0.697 0.43478</anchor>-->')
	print ('		<axis>0 0 1</axis>')
	print ('		<limitsdeg>-40 40</limitsdeg>')
	print ('	</joint>\n')
	
	print ('	<!-- ******************* LEFT ARM ***************************** -->')
	print ('	<!-- *********************************************************** -->\n')
	
	  
	print ('	<joint name="lShoulderX" type="hinge">')
	print ('		<body>Torso</body>')
	print ('		<body>lShoulderDummyX</body>')
	print ('		<offsetfrom>lShoulderDummyX</offsetfrom>')
	print ('		<!--        <anchor>-0.0112 0.23982 0.428571</anchor>-->')
	print ('		<axis>1 0 0</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')

	print ('	<joint name="lShoulderZ" type="hinge">')
	print ('		<body>lShoulderDummyX</body>')
	print ('		<body>lShoulderDummyZ</body>')
	print ('		<offsetfrom>lShoulderDummyZ</offsetfrom>')
	print ('		<!--        <anchor>-0.0112 0.23982 0.428571</anchor>-->')
	print ('		<axis>0 0 -1</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')
	
	print ('	<joint name="lShoulderY" type="hinge">')
	print ('		<body>lShoulderDummyZ</body>')
	print ('		<body>lHumerus</body>')
	print ('		<offsetfrom>lHumerus</offsetfrom>')
	print ('		<!--        <anchor>-0.0112 0.23982 0.428571</anchor>-->')
	print ('		<axis>0 -1 0</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')

	print ('	<joint name="lArmTrans" type="slider">')
	print ('		<body>lHumerus</body>')
	print ('		<body>lElbowDummy</body>')
	print ('		<offsetfrom>lElbowDummy</offsetfrom>')
	print ('		<!--        <anchor>-0.007033 0.446428 0.430224</anchor>-->')
	print ('		<axis>0 1 0</axis>')
	print ('		<limits>-0.50 0.50</limits>')
	print ('	</joint>\n')
	
	print ('	<joint name="lElbowZ" type="hinge">')
	print ('		<body>lElbowDummy</body>')
	print ('		<body>lRadius</body>')
	print ('		<offsetfrom>lRadius</offsetfrom>')
	print ('		<!--        <anchor>-0.007033 0.446428 0.430224</anchor>-->')
	print ('		<axis>0 0 -1</axis>')
	print ('		<limitsdeg>-180 180</limitsdeg>')
	print ('	</joint>\n')
	
	print ('	<joint name="lWristX" type="hinge">')
	print ('		<body>lRadius</body>')
	print ('		<body>lWristDummyX</body>')
	print ('		<offsetfrom>lWristDummyX</offsetfrom>')
	print ('		<!--        <anchor>-0.004259 0.697 0.43478</anchor>-->')
	print ('		<axis>-1 0 0</axis>')
	print ('		<limitsdeg>-90 90</limitsdeg>')
	print ('	</joint>\n')

	print ('	<joint name="lWristY" type="hinge">')
	print ('		<body>lWristDummyX</body>')
	print ('		<body>lWristDummyY</body>')
	print ('		<offsetfrom>lWristDummyY</offsetfrom>')
	print ('		<!--        <anchor>-0.004259 0.697 0.43478</anchor>-->')
	print ('		<axis>0 -1 0</axis>')
	print ('		<limitsdeg>-180 0</limitsdeg>')
	print ('	</joint>\n')

	print ('	<joint name="lWristZ" type="hinge">')
	print ('		<body>lWristDummyY</body>')
	print ('		<body>lHand</body>')
	print ('		<offsetfrom>lHand</offsetfrom>')
	print ('		<!--        <anchor>-0.004259 0.697 0.43478</anchor>-->')
	print ('		<axis>0 0 -1</axis>')
	print ('		<limitsdeg>-40 40</limitsdeg>')
	print ('	</joint>\n')
	
	print ('	<!-- ******************* UNIFED LEG ***************************** -->')
	print ('	<!-- *********************************************************** -->\n')

   
	print ('	<joint name="HipX" type="hinge">')
	print ('		<body>PelvisBody</body>')
	print ('		<body>HipDummyX</body>')
	print ('		<offsetfrom>HipDummyX</offsetfrom>')
	print ('		<!--        <anchor>0.022487 -0.100975 -0.086017</anchor>-->')
	print ('		<axis>1 0 0</axis>')
	print ('		<limitsdeg>-100 10</limitsdeg>')
	print ('	</joint>\n')
 
	print ('	<joint name="HipY" type="hinge">')
	print ('		<body>HipDummyX</body>')
	print ('		<body>HipDummyY</body>')
	print ('		<offsetfrom>HipDummyY</offsetfrom>')
	print ('		<!--        <anchor>0.022487 -0.100975 -0.086017</anchor>-->')
	print ('		<axis>0 1 0</axis>')
	print ('		<limitsdeg>-150 60</limitsdeg>')
	print ('	</joint>\n')

	print ('	<joint name="HipZ" type="hinge">')
	print ('		<body>HipDummyY</body>')
	print ('		<body>Femur</body>')
	print ('		<offsetfrom>Femur</offsetfrom>')
	print ('		<!--        <anchor>0.022487 -0.100975 -0.086017</anchor>-->')
	print ('		<axis>0 0 1</axis>')
	print ('		<limitsdeg>-40 40</limitsdeg>')
	print ('	</joint>\n')

	
	print ('	<joint name="Knee" type="hinge">')
	print ('		<body>Femur</body>')
	print ('		<body>Tibia</body>')
	print ('		<offsetfrom>Tibia</offsetfrom>')
	print ('		<!--        <anchor>-0.002421 -0.097751 -0.554311</anchor>-->')
	print ('		<axis>0 1 0</axis>')
	print ('		<limitsdeg>0 140</limitsdeg>')
	print ('	</joint>\n')
	  
	print ('	<joint name="AnkleX" type="hinge">')
	print ('		<body>Tibia</body>')
	print ('		<body>AnkleDummyX</body>')
	print ('		<offsetfrom>AnkleDummyX</offsetfrom>')
	print ('		<!--        <anchor>-0.016412 -0.092302 -0.94291</anchor>-->')
	print ('		<axis>1 0 0</axis>')
	print ('		<limitsdeg>-20 20</limitsdeg>')
	print ('	</joint>\n')

	print ('	<joint name="AnkleY" type="hinge">')
	print ('		<body>AnkleDummyX</body>')
	print ('		<body>AnkleDummyY</body>')
	print ('		<offsetfrom>AnkleDummyY</offsetfrom>')
	print ('		<!--        <anchor>-0.016412 -0.092302 -0.94291</anchor>-->')
	print ('		<axis>0 1 0</axis>')
	print ('		<limitsdeg>-30 30</limitsdeg>')
	print ('	</joint>\n')

	print ('	<joint name="AnkleZ" type="hinge">')
	print ('		<body>AnkleDummyY</body>')
	print ('		<body>Foot</body>')
	print ('		<offsetfrom>Foot</offsetfrom>')
	print ('		<!--        <anchor>-0.016412 -0.092302 -0.94291</anchor>-->')
	print ('		<axis>0 0 1</axis>')
	print ('		<limitsdeg>-40 40</limitsdeg>')
	print ('	</joint>\n')	
	
	print ('	<!-- Adjacent Bodies -->')

	print ('	<!-- Torso -->')
	print ('	<!-- Body_Torso ')
	print ('	<adjacent>Body_Torso Body_Hip</adjacent> -->')

	print ('</kinbody>')
	print ('</robot>')

def parse_input():
	#for radii inputs take max of width/height (or take circumference)
	head_inputs[0] = float(raw_input('Enter head height:'))
	head_inputs[1] = float(raw_input('Enter head width:'))

	arm_inputs[0] = float(raw_input('Enter arm length:'))
	arm_inputs[1] = float(raw_input('Enter arm width:'))
	arm_inputs[2] = float(raw_input('Enter forearm length:'))
	arm_inputs[3] = float(raw_input('Enter forearm width:'))
	arm_inputs[4] = float(raw_input('Enter hand length:'))
	arm_inputs[5] = float(raw_input('Enter hand width:'))
	arm_inputs[6] = float(raw_input('Enter finger length:'))
	arm_inputs[7] = float(raw_input('Enter finger width:'))
	arm_inputs[8] = float(raw_input('Enter thumb length:'))
	arm_inputs[9] = float(raw_input('Enter thumb width:'))

	torso_inputs[0] = float(raw_input('Enter neck length:'))
	torso_inputs[1] = float(raw_input('Enter neck circumference:')) 
	torso_inputs[2] = float(raw_input('Enter pelvis length:'))
	torso_inputs[3] = float(raw_input('Enter pelvis circumference:'))
	torso_inputs[4] = float(raw_input('Enter torso length:'))
	torso_inputs[5] = float(raw_input('Enter torso circumference:'))
	torso_inputs[6] = float(raw_input('Enter chest length:'))
	torso_inputs[7] = float(raw_input('Enter chest width:'))
	torso_inputs[8] = float(raw_input('Enter chest height:'))

	leg_inputs[0] = float(raw_input('Enter femur length:'))
	leg_inputs[1] = float(raw_input('Enter femur circumference:')) 
	leg_inputs[2] = float(raw_input('Enter lower femur length:'))
	leg_inputs[3] = float(raw_input('Enter lower femur circumference:'))
	leg_inputs[4] = float(raw_input('Enter tibia length:'))
	leg_inputs[5] = float(raw_input('Enter tibia circumference:'))
	leg_inputs[6] = float(raw_input('Enter foot length:'))
	leg_inputs[7] = float(raw_input('Enter foot width:'))
	leg_inputs[8] = float(raw_input('Enter foot height:'))

if __name__ == '__main__':
	mode = 0
	print_model()
	# parse_input()