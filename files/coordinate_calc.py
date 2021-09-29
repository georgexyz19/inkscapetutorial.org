# need numpy installation
import numpy as np
from math import cos, sin, radians

a = np.array([ [20], [20], [1] ])

# rotate around (50, 40)
b = np.array([[cos(radians(30)), -1 * sin(radians(30)), 50 ], 
               [sin(radians(30)), cos(radians(30)), 40], 
               [0, 0, 1] ])
               
c = np.array([[ 1, 0, -50 ], 
               [0, 1, -40], 
               [0, 0, 1] ])
    

# rotate around (0, 0)                        
d = np.array([[cos(radians(30)), -1 * sin(radians(30)), 0 ], 
               [sin(radians(30)), cos(radians(30)), 0], 
               [0, 0, 1] ])
                 
e = np.linalg.inv(d)

rv =  np.linalg.multi_dot([e, b, c, a])

print(f'result is {rv}')

#     result is [[ 33.30127019]
# [-10.35898385]
# [  1.        ]]

