#Name: Michelle Lin, ENGR 1050, Homework 4, Spring 2023
#Collaborators: None
#Program Description: Locates zeros of data through bisection method of searching through an interval

#import modules
import matplotlib.pyplot as plt
import numpy as np
import math

#load data files
data = np.load("snapthrough.npy")

#slicing data to get all the values in the first column [mm]
z = data[:,0]
#get all the values in the second column [N]
force = data[:,1] 

#function to call bisection method
def bisection(z,force):
    """
        This function locates the z value at which the force cross zero with a negative slope
        Inputs: z [1D np array]
                force [1D np array]
        Outputs: float 
        Usage: bisection(-10,5)
                returns: "There is a zero at z=-4.2965 "
        """
    #sets variables for start and end of interval, finds which value cooresponds to z values of beginning and end of interval
    a=np.searchsorted(z,interval[0])
    b=np.searchsorted(z,interval[-1])
    #while loop that iterates as long as error is greater than tolerance
    while (b-a)>1:
        #sets variable to update one end of the interval by halving current interval
        x=math.ceil((a+b)/2)
        #checks if f(a)f(b) is positive
        if (force[a]*force[b])>0:
            break #breaks loop since existence of 0 is not certain
        #checks if f(a)f(b)=0
        else:
            if (force[a]*force[b])==0:
                #checks whether f(a) or f(b) is 0 and sets x to that value
                if force[a]==0:
                    x=a
                elif force[b]==0:
                    x=b
            #checks if f(a)f(b) is negative
            elif (force[a]*force[b])<0:
                #checks if new interval, which is halved is negative
                if force[a]*force[x]<0:
                    #sets b to be updated value of interval
                    b=x
                else:
                    #sets a to be updated value of interval
                    a=x
    #checks if value is near 0 (within tolerance)
    y=interpolate(z,force,z[x])
    #checks if force is near 0
    if (((y-1)<1) and ((y-1)>=0) or ((y+1)>(-1)) and (y-1)<=0):
        print("There is a zero at z=",z[x])
    else:
        print("Sorry, I cannot be sure there is a zero in this interval")
    

def interpolate(z, force, zs):
    """
    This function interpolates the force value at zs, the desired z (height, mm) value.
    Inputs: z, [1d np array], height data (mm)
            force, [1d np array], force data (N)
            zs, [float], height value to find the force at (mm)
    Output: fs, [float], interpolated force at zs
    Usage: interpolate(z, force, 10.0)
            returns 0.6257614678899088
    """
    index_right = np.searchsorted(z, zs) #find the first index of closest value in array to the right of zs, assuming a sorted array
    index_left = index_right - 1 #get the index to the left
    force_right = force[index_right] 
    force_left = force[index_left] 
    z_right = z[index_right]
    z_left = z[index_left]
    fs = (force_right - force_left)/(z_right-z_left) * (zs - z_left) + force_left #formula for linear interpolation
    return fs

#set interval that function checks
interval=np.arange(-10,6) #interval from -10,6
bisection(z,force)
