from math import sin, cos, sqrt, atan2, radians
from lmfit import minimize,Parameters,fit_report
import numpy as np

# initial condition
# can be the last point

scan_1_tag_1 = np.load("C:/Estagio/Beacon/scan_1_tag_1.npy", allow_pickle=True)
scan_1_tag_2 = np.load("C:/Estagio/Beacon/scan_1_tag_2.npy", allow_pickle=True)
scan_2_tag_1 = np.load("C:/Estagio/Beacon/scan_2_tag_1.npy", allow_pickle=True)
scan_2_tag_2 = np.load("C:/Estagio/Beacon/scan_2_tag_2.npy", allow_pickle=True)
scan_3_tag_1 = np.load("C:/Estagio/Beacon/scan_3_tag_1.npy", allow_pickle=True)
scan_3_tag_2 = np.load("C:/Estagio/Beacon/scan_3_tag_2.npy", allow_pickle=True)

guess = np.array([-12.92,-38.38]) # meters

# scanner positions
##scanners = np.array([[0.,0.],
##                     [0.,15.],
##                     [15.,0.]
##                    ])
scanners = np.array([[-12.9233167397374,-38.3883990923512],   # scan 1: a7b5dd3e-94e9-458f-acbb-2c0fbe797004
                    [-12.923410006353,-38.388414047007],     # scan 2: 54e93778-4a09-44dc-a0a0-6e51119e3842
                    [-12.923420006353,-38.3883810923512]])    # scan 3: c182d1e7-3a7a-47b3-afb5-d8309bb31c4f

##R = 6371
##x_cart = []
##y_cart = []
##xy_cart = []
##for i in range(0,len(scanners)):
##    x_cart.append(R*np.cos(scanners[i][0])*np.cos(scanners[i][1]))
##    y_cart.append(R*np.cos(scanners[i][0])*np.sin(scanners[i][1]))
##    xy_cart.append([x_cart[i],y_cart[i]])

def d_lat_lng(aa,bb):
    R = 6373.0
    distance = np.empty(len(bb)) 
    for i in range(0, len(bb)):
        lat1 = radians(aa[0])
        lon1 = radians(aa[1])
        lat2 = radians(bb[i][0])
        lon2 = radians(bb[i][1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance[i] = R * c
    return distance

def distance(a,b):
    """
        a = decision variable (coordinates)
        b = scanners coordinates
    """
    d = np.empty(len(b))
    for i in range(0, len(b)):
        d[i] = np.sqrt(np.power(a[0]-b[i][0],2)+np.power(a[1]-b[i][1],2))
    return d

def residual(params,measure,scanners):
    """
        params = contains the decision variables
        measure = contains the measured distances
        scanners = contains the scanner positions
    """
    x=np.array([params['x'].value,
                params['y'].value])
    s = np.power(d_lat_lng(x,scanners)-measure,2)
    #s = s/np.power(0.01,2)
    return s

params = Parameters()
params.add('x', value=guess[0])
params.add('y', value=guess[1])

#measure = np.array([7.07945784,1.4959794,1.])
measure = np.array([0.0233157844686567,4.499140728225,1.98755540735773])
measure = measure/1000

out = minimize(residual, params, args=(measure,scanners))
print(out.params['x'].value)
print(out.params['y'].value)
#print(fit_report(out))
#print(out.params.pretty_print()
#print(out.params['x'].stderr) 