"""Extract displacement data for OpenFOAM 6DoF.dat from positional data around a 
Formula 1 track. 
The exctracted data is written in the appropriate format for OpenFOAM.
We also need to do some conversions.

"""
##############################################################################
# Import FastF1 and load the data

import matplotlib.pyplot as plt
import numpy as np
import fastf1 as f1


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    
    v1_u_deg = np.degrees(v1_u)
    v2_u_deg = np.degrees(v2_u)
   
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def vector_to_euler(x, y, z):
    yaw = np.arctan2(y, x)  # Rotation around Z-axis
    pitch = np.arctan2(z, np.sqrt(x**2 + y**2))  # Rotation around Y-axis
    
    # Convert to degrees for better readability
    yaw_deg = np.degrees(yaw)
    pitch_deg = np.degrees(pitch)
    
    return yaw_deg, pitch_deg

###############################################################################
###############################################################################
year = 2021
grand_prix = 'Austrian Grand Prix'

session = f1.get_session(year, grand_prix, 'Q')
session.load()

lap = session.laps.pick_fastest()
tel = lap.get_telemetry()
print("########################")
print(tel.columns)

###############################################################################
# Prepare the data for plotting by converting it to the appropriate numpy
# data types
x = list(np.array(tel['X'].values))
y = list(np.array(tel['Y'].values))
z = list(np.array(tel['Z'].values))
time = list(np.array(tel['Time'].values))

num_entries = len(x)

# visualize first ten entries 
print("**********************")
for i in range(10):
    print(time[i], x[i], y[i], z[i])


x_0 = x[0]
y_0 = y[0]
z_0 = z[0]
track_length = 0
# convert nanoseconds to seconds and translate start/finish to (0,0,0)
for i in range(num_entries):
    time_entry = float(time[i])
    time[i] = time_entry / 1e9
    x[i] = round((x[i] - x_0) / 10 , 6) # no idea why we have to divide 
    y[i] = round((y[i] - y_0) / 10 , 6) # by ten to get meters, weird.
    z[i] = round((z[i] - z_0) / 10 , 6)
    

# sum up length just to check if everything's alright
print("\n++++++++++++++++++++++")
for i in range(num_entries-1):
    track_length += np.sqrt((x[i+1] - x[i])**2 + (y[i+1] - y[i])**2 + (z[i+1] - z[i])**2)
track_length = float(track_length)
print(f"{track_length = } meters")
    

# look at the first ten entries in our lists
print("\n######################")
for i in range(10):
    print(time[i], x[i], y[i], z[i])
    
# let's plot the track from the data, red dot indicates first values
# these should be at start/finish, and they are.
fig = plt.figure()
ax = plt.axes(projection='3d')    
ax.plot3D(x, y, z, 'green')
ax.scatter3D(x[0], y[0], z[0], 'red')
ax.set_title(grand_prix)
plt.show()


# we need rotational data too! We can generate all Euler angles from step-wise
# trajectory data. Again we subtract the first values from all the data
ang_yaw = []
ang_pitch = []
ang_roll = []

i = 0
vector_0 = [float(x[i+1]) - float(x[i]), float(y[i+1]) - float(y[i]), float(z[i+1]) - float(z[i])]
yaw_0, pitch_0 = vector_to_euler(vector_0[0], vector_0[1], vector_0[2])

for i in range(num_entries - 1):
#for i in range(5):    
    vector = [float(x[i+1]) - float(x[i]), float(y[i+1]) - float(y[i]), float(z[i+1]) - float(z[i])]
    yaw, pitch = vector_to_euler(vector[0], vector[1], vector[2])
    roll = 0 # we could calculate an artificial roll value from lateral acc., but for now we set = 0
        
    ang_yaw.append(yaw - yaw_0) # we subtract the first yaw value to start from = 0
    ang_pitch.append(pitch - pitch_0) # we subtract the first pitch value to start from = 0
    ang_roll.append(roll)


# now we need to construct the weird data format for OpenFoam
filename = '6DoF.dat'

# check if file exists, if so, delete it (we write in append mode later)
import os
if os.path.exists(filename):
  os.remove(filename)
else:
  print("The file does not exist") 


# write the data to our file in OpenFOAM 6DoF.dat format
# order of entries is ((x y z ) (roll pitch yaw))
with open(filename, 'a') as file:
    file.write(str(num_entries-1)+"\n")
    file.write("("+"\n")
    for i in range(num_entries - 1):
        line = "(" + str(time[i])+" " + "((" + str(x[i]) +" " + str(y[i]) +" " +\
            str(z[i]) + ") (" + str(ang_roll[i])+" " +str(ang_pitch[i])+" " +str(ang_yaw[i])+")))"
        file.write(line+"\n")
    file.write(")")



# print("****************************************************")
# print("****************************************************")
# vec_1 = [-395.747154, -105.726953, 12.601921]
# vec_2 = [-405.083496, -106.242632, 13.422183]
# vector_0 = [vec_2[0] - vec_1[0], vec_2[1] - vec_1[1], vec_2[2] - vec_1[2]     ]
# yaw_1, pitch_1 = vector_to_euler(vector_0[0], vector_0[1], vector_0[2])
# print("****", yaw_1 - yaw_0, pitch_1 - pitch_0, "0")
    
# print("****************************************************")
# vec_1 = [-405.083496, -106.242632, 13.422183]
# vec_2 = [-406.047154, -106.226953, 13.501921]
# vector_0 = [vec_2[0] - vec_1[0], vec_2[1] - vec_1[1], vec_2[2] - vec_1[2]     ]
# yaw_1, pitch_1 = vector_to_euler(vector_0[0], vector_0[1], vector_0[2])
# print("****", yaw_1 - yaw_0, pitch_1 - pitch_0, "0")

# test vector_to_euler
# vec_1 = [1,1,1]
# print(vector_to_euler(vec_1[0], vec_1[1], vec_1[2]))
