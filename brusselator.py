#import modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

def brusselator_MC(X0, Tfinal):
    #creates list of molecule numbers
    X =[X0.copy()]

    #set current time to 0
    T = 0

    #list of all times
    tf=[0]

    #parameters
    c1X1 = 5000
    c2X2 = 50
    c3 = .00005
    c4=5

    #while loop that runs as long as the current time is less than final time
    while T<Tfinal:
        #takes last number of molecules of reactants to update
        Y1 = X[-1][0]
        Y2 = X[-1][1]

        #reaction 1
        a_1 = c1X1
        #reaction 2
        a_2 = c2X2*Y1
        #reaction 3
        a_3 = c3*Y1*(Y1-1)/2*Y2
        #reaction 4
        a_4 = c4*Y1
        a_0 = a_1 + a_2 + a_3 + a_4

        #stores random number to calculate time
        r1 = np.random.rand()
        #solves equation for next reaction time
        dt = -1/a_0*np.log(r1)

        #stores second random number to determine what reaction occurs
        r2=np.random.rand()

        #checks which reaction occurs and updates molecules
        if (r2*a_0 < a_1):
            X.append([X[-1][0] + 1, X[-1][1]])
        elif (r2*a_0 < a_1 + a_2):
            X.append([X[-1][0] - 1, X[-1][1] + 1])
        elif (r2*a_0 < a_1 + a_2 + a_3):
            X.append([X[-1][0] + 1, X[-1][1] - 1])
        else:
            X.append([X[-1][0] - 1, X[-1][1]])

        #updates new time
        T+=dt

        #adds to list keeping track of all times
        tf.append(T)
    return tf, X

def brusselator_ODE(X0, tf, kX1, kX2, k3, k4):
    def brusselator_dyn(t, X, kX1, kX2, k3, k4):
        #calculates derivatives
        Y1 = X[0]
        Y2 = X[1]
        dY1 = kX1 - kX2*Y1 + k3*Y1*Y1*Y2 - k4*Y1
        dY2 = kX2*Y1-k3*Y1*Y1*Y2
        return np.array([dY1, dY2])
    
    #integrates brusellator ODE
    sol = solve_ivp(brusselator_dyn, (0,max(tf)), X0, args=(kX1,kX2,k3,k4), t_eval=tf)
    return sol.t, sol.y

def SOS_error(K, X0, tf, X):
    kX1 = K[0]
    kX2 = K[1]
    k3 = K[2]
    k4 = K[3]
    (tode, Xode) = brusselator_ODE(X0, tf, kX1, kX2, k3, k4)
    Xode = np.transpose(Xode)
    if(Xode.shape != X.shape):
        Xode = np.pad(Xode, ((0, X.shape[0]-Xode.shape[0]),(0,0)), 'edge')
    residual = Xode - X
    return residual.flatten()


# Monte Carlo 10 runs
Niter = 10
#sets initial molecule numbers
X0 = [1000,2000]
#sets final time in seconds
Tf = 14

#for loop that runs Niter times
for i in range(Niter):
    #sets results of run to t and x
    (t, X) = brusselator_MC(X0, Tf)
    #sets number of molecules to an array
    X = np.array(X)
    #plots each molecule amount
    plt.plot(X[:,0], X[:,1], label = 'run '+str(i+1))
plt.xlabel('Y1')
plt.ylabel('Y2')
plt.legend()
plt.show()

# compare to ode
(t, X) = brusselator_MC(X0, Tf)
#divide by 1000 for concentrations
X = np.array(X)/1000
#parameters
K =  [9.5, 38, 13, 21.5]


# bonus
#sets parameters to fitted parameters
params = least_squares(SOS_error, K, args=([1,2], t, X))
K = params.x
print(K)

#plots results of ode and simulation
(tode, Xode) = brusselator_ODE([1,2], t, K[0], K[1], K[2], K[3])
plt.plot(X[:,0], X[:,1], label = 'MC')
plt.plot(Xode[0], Xode[1], label = 'ODE')
plt.xlabel('Y1')
plt.ylabel('Y2')
plt.legend()
plt.show()

