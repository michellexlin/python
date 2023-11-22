#import modules
import matplotlib.pyplot as plt
import numpy as np

def SEIR(S, E, I , R , alpha, beta, gamma):
    """This function evaluates changes in populations of susceptible, exposed, infected, and recovered people
        Inputs: S=float
                E=float
                I=float
                R=float
                Note: S+E+I+R=1
                alpha: float/Integer
                beta: float/integer
                gamma: float/integer
        Outputs: dSdt, dEdt, dIdt, dRdt
        Usage: SEIR(.25,.25,.25,.25,1,.5,.3)
            Returns: (-0.03125, -0.21875, 0.175, 0.075)
    """
    dSdt=(-beta)*S*I #sets dSdt
    dEdt=((beta*I*S)-(alpha*E)) #sets dEdt
    dIdt=((alpha*E)-(gamma*I)) #sets dIdt
    dRdt=(gamma*I) #sets dRdt
    return dSdt,dEdt,dIdt,dRdt

def integrate_SEIR_model(S0,E0,I0,R0,alpha, beta, gamma, dt, Tf):
    """This function evaluates changes in populations of susceptible, exposed, infected, and recovered people based on initial populations
        Inputs: S0=Scalar
                E0=Scalar
                I0=Scalar
                R0=Scalar
                alpha: float/integer
                beta: float/integer
                gamma: float/integer
        Outputs: t,S,E,I,R
        Usage: integrate_SEIR_model(.9,0,.1,0,1, .5, .3, 5, 100)
            Returns: ([0.675, 0.45, 0.22499999999999998, -5.551115123125783e-17, ....)]
    """
    #sets initial values for t,S,E,I, and R
    t=0;S=S0;I=I0;E=E0;R=R0
    #sets empty arrays for updated values for S,E,I,R and t
    S_vec=[];E_vec=[];I_vec=[];R_vec=[];t_vec=[]
    #adds inital values for t,S,E,I, and R to respective arrays
    S_vec.append(S0);E_vec.append(E0);I_vec.append(I0);R_vec.append(R0);t_vec.append(0)
    #calculates number of steps based on final time and step size
    n=int(Tf/dt)
    #for loop that iterates n times
    for i in range(1,n+1):
        #sets derivative array to be function of SEIR with inputs based on previous values
        der=SEIR(S_vec[i-1],E_vec[i-1], I_vec[i-1] , R_vec[i-1] , alpha, beta, gamma)
        #adds to arrays an updated value after calculating based on previous values
        S_vec.append(S_vec[i-1]+(dt*der[0]))
        E_vec.append(E_vec[i-1]+(dt*(der[1])))
        I_vec.append(I_vec[i-1]+(dt*(der[2])))
        R_vec.append(R_vec[i-1]+(dt*(der[3])))
        #adds to t_vec(time) array by increasing new index value of t by step size
        t_vec.append(t_vec[i-1]+dt)
    #Renames and returns each array
    S=S_vec;E=E_vec;I=I_vec;R=R_vec;t=t_vec
    return S,E,I,R,t

def plot_SEIR_model(S0,E0,I0,R0,alpha, beta, gamma, dt, Tf):
    """Produces a plot of the SEIR model from o to Tf
    Inputs: S0=Scalar
            E0=Scalar
            I0=Scalar
            R0=Scalar
            alpha: float/integer
            beta: float/integer
            gamma: float/integer
    Outputs: out = line graph

    Usage: plot_SEIR_model(.9,0,.1,0,1, .5, .3, 1, 100)
        Returns out: line graph with x values from 0 to 100, and y values from from S0,E0,I0,R0
    """
    #creates a figure with single axes
    fig, ax = plt.subplots() 
    #sets x values to be vector of time values
    t=(integrate_SEIR_model(S0,E0,I0,R0,alpha,beta,gamma,dt,Tf)[4])
    #plots S,E,I, and r
    ax.plot(t,(integrate_SEIR_model(S0,E0,I0,R0,alpha, beta, gamma, dt, Tf))[0], label="Susceptible")
    ax.plot(t,(integrate_SEIR_model(S0,E0,I0,R0,alpha, beta, gamma, dt, Tf))[1], label="Exposed")
    ax.plot(t,(integrate_SEIR_model(S0,E0,I0,R0,alpha, beta, gamma, dt, Tf))[2], label="Infected")
    ax.plot(t,(integrate_SEIR_model(S0,E0,I0,R0,alpha, beta, gamma, dt, Tf))[3], label="Recovered")
    #label axis
    ax.set_xlabel('Time')
    ax.set_ylabel('Fraction of Population')
    #sets plot title based on alpha, beta, and gamma values
    title=f"Alpha={alpha}, Beta={beta}, Gamma={gamma}"
    ax.set_title(title)
    ax.legend()
    plt.show()

#plots figures with various S0,E0,I0,R0,alpha, beta, gamma, step size, and end time values
#(a) S0 = 0.9, E0 = R0 = 0, I0 = 0.1, α = 1, β = 0.5, γ = 0.3, dt = 5, Tf = 100
plot_SEIR_model(.9,0,.1,0,1, .5, .3, 5, 100)
#(b) S0 = 0.9, E0 = R0 = 0, I0 = 0.1, α = 1, β = 0.5, γ = 0.3, dt = 1, Tf = 100
plot_SEIR_model(.9,0,.1,0,1, .5, .3, 1, 100)
#(c) S0 = 0.9, E0 = R0 = 0, I0 = 0.1, α = 1, β = 0.5, γ = 0.3, dt = 0.01, Tf = 100 
plot_SEIR_model(.9,0,.1,0,1, .5, .3, .01, 100)

def SEIR_mod(S, E, I , R , alpha, beta, gamma, zeta):
    """This function evaluates changes in populations of susceptible, exposed, infected, and recovered people
        Inputs: S=float
                E=float
                I=float
                R=float
                Note: S+E+I+R=1
                alpha: float/Integer
                beta: float/integer
                gamma: float/integer
                zeta: float/integer
        Outputs: dSdt, dEdt, dIdt, dRdt
        Usage: SEIR_mod(.25,.25,.25,.25,1,.5,.3,.2)
            Returns: (0.018750000000000003, -0.21875, 0.175, 0.024999999999999994)
    """
    #sets updated dSdt
    dSdt=(((-beta)*S*I)+(zeta*R)) 
    #sets dEdt,dIdt as existing
    dEdt=SEIR(S, E, I , R , alpha, beta, gamma)[1]
    dIdt=SEIR(S, E, I , R , alpha, beta, gamma)[2]
    #sets updated dRdt
    dRdt=((gamma*I)-(zeta*R))
    return dSdt, dEdt, dIdt, dRdt

def integrate_SEIR_model_mod(S0, E0, I0, R0, alpha, beta, gamma, zeta, dt, Tf):
    """This function evaluates changes in populations of susceptible, exposed, infected, and recovered people based on initial populations
        Inputs: S0=Scalar
                E0=Scalar
                I0=Scalar
                R0=Scalar
                alpha: float/integer
                beta: float/integer
                gamma: float/integer
                zeta: float/integer
        Outputs: t,S,E,I,R
        Usage: integrate_SEIR_model(.9,0,.1,0,1, .5, .3,.2, 5, 100)
            Returns: ([0.9, 0.44999999999999996, 1.4999999999999998, -37.04999999999999, -10157.549999999996, ....)]
    """
    #sets initial values for t,S,E,I, and R
    t=0;S=S0;I=I0;E=E0;R=R0
    #sets empty arrays for updated values for S,E,I,R and t
    S_vec=[];E_vec=[];I_vec=[];R_vec=[];t_vec=[]
    #adds inital values for t,S,E,I, and R to respective arrays
    S_vec.append(S0);E_vec.append(E0);I_vec.append(I0);R_vec.append(R0);t_vec.append(0)
    #calculates number of steps based on final time and step size
    n=int(Tf/dt)
    #for loop that iterates n times
    for i in range(1,n+1):
        #sets derivative array to be function of SEIR with inputs based on previous values
        der=SEIR_mod(S_vec[i-1],E_vec[i-1], I_vec[i-1] , R_vec[i-1] , alpha, beta, gamma,zeta)
        #adds to arrays an updated value after calculating based on previous values
        S_vec.append(S_vec[i-1]+(dt*der[0]))
        E_vec.append(E_vec[i-1]+(dt*(der[1])))
        I_vec.append(I_vec[i-1]+(dt*(der[2])))
        R_vec.append(R_vec[i-1]+(dt*(der[3])))
        #adds to t_vec(time) array by increasing new index value of t by step size
        t_vec.append(t_vec[i-1]+dt)
    #Renames and returns each array
    S=S_vec;E=E_vec;I=I_vec;R=R_vec;t=t_vec
    return S,E,I,R,t

def plot_SEIR_model_mod(S0, E0, I0, R0, alpha, beta, gamma, zeta, dt, Tf):
    """Produces a plot of the SEIR model from o to Tf
    Inputs: S0=Scalar
            E0=Scalar
            I0=Scalar
            R0=Scalar
            alpha: float/integer
            beta: float/integer
            gamma: float/integer
            zeta: float/integer
    Outputs: out = line graph

    Usage: plot_SEIR_model(.9,0,.1,0,1, .5, .3,.2, 1, 100)
        Returns out: line graph with x values from 0 to 100, and y values from from S0,E0,I0,R0
    """
    #creates a figure with single axes
    fig, ax = plt.subplots() 
    #sets x values to be vector of time values
    t=(integrate_SEIR_model_mod(S0,E0,I0,R0,alpha,beta,gamma,zeta,dt,Tf)[4])
    #plots S,E,I, and r
    ax.plot(t,(integrate_SEIR_model_mod(S0,E0,I0,R0,alpha, beta, gamma, zeta, dt, Tf))[0], label="Susceptible")
    ax.plot(t,(integrate_SEIR_model_mod(S0,E0,I0,R0,alpha, beta, gamma, zeta, dt, Tf))[1], label="Exposed")
    ax.plot(t,(integrate_SEIR_model_mod(S0,E0,I0,R0,alpha, beta, gamma, zeta, dt, Tf))[2], label="Infected")
    ax.plot(t,(integrate_SEIR_model_mod(S0,E0,I0,R0,alpha, beta, gamma, zeta, dt, Tf))[3], label="Recovered")
    #label axis
    ax.set_xlabel('Time')
    ax.set_ylabel('Fraction of Population')
    #sets plot title based on alpha, beta, gamma, and zeta values
    title=f"Alpha={alpha}, Beta={beta}, Gamma={gamma}, Zeta={zeta}"
    ax.set_title(title)
    ax.legend()
    plt.show()

#plots figures with various S0,E0,I0,R0,alpha, beta, gamma, zeta, step size, and end time values
#(a) S0 = 0.9, E0 = R0 = 0, I0 = 0.1, α = 1, β = 0.5, γ = 0.3, ζ = 0.01, dt = 0.01, Tf = 100
plot_SEIR_model_mod(.9,0,.1,0,1, .5, .3,.01, .01, 100)
#(b) S0 = 0.9, E0 = R0 = 0, I0 = 0.1, α = 1, β = 0.5, γ = 0.3, ζ = 0.01, dt = 0.01, Tf = 1000
plot_SEIR_model_mod(.9,0,.1,0,1, .5, .3,.01, .01, 1000)
