# need numpy installation
import numpy as np
from math import cos, sin, radians

a = np.array([ [20], [20], [1] ])

# move center to (0, 0)
b = np.array([[ 1, 0, -50 ], 
               [0, 1, -40], 
               [0, 0, 1] ])
    
# rotate around (0, 0)
c = np.array([[cos(radians(30)), -1 * sin(radians(30)), 0 ], 
               [sin(radians(30)), cos(radians(30)), 0], 
               [0, 0, 1] ])

# move center back to (50, 40)
d = np.array([[ 1, 0, 50 ], 
               [0, 1, 40], 
               [0, 0, 1] ])
    

# rotate around (0, 0)                        
e = np.array([[cos(radians(30)), -1 * sin(radians(30)), 0 ], 
               [sin(radians(30)), cos(radians(30)), 0], 
               [0, 0, 1] ])
                 
f = np.linalg.inv(e)


# e ^ (-1) \cdot (rv) = d \cdot c \cdot b \cdot a 
# rv = return value 

rv =  np.linalg.multi_dot([f, d, c, b, a])

print(f'result is {rv}')

#     result is [[ 33.30127019]
# [-10.35898385]
# [  1.        ]]

