#Name: Michelle Lin, ENGR 1050, Homework 8, Spring 2023
#Collaborators: None
#Program Description: Simulation of billiards

#import modules
import numpy as np
import matplotlib.pyplot as plt

class Ball(object):
    def __init__(self,color='r'):
        # Stores plot information so we can animate
        self.plot_handle = []
        #sets color to be input
        self.color = color
        
        # Ball parameters
        self.radius = 0.5

        plt.title('Click on the ball location')
        pts = plt.ginput(1)
        self.pos = np.array(pts[0])
        self.draw()

        plt.title('Click to indicate the ball velocity')
        pts = plt.ginput(1)
        self.vel = (np.array(pts[0]) - self.pos)
        self.vel = self.vel / np.linalg.norm(self.vel)

        plt.title('')
    
    def calc_circ(self):
        theta = np.arange(0,2*np.pi,0.01)
        xc = self.radius * np.cos(theta)+self.pos[0]
        yc = self.radius * np.sin(theta)+self.pos[1]
        return xc, yc

    def draw(self):
        xc, yc = self.calc_circ()
        self.plot_handle = plt.plot(xc,yc,'-'+self.color)

    def redraw(self):
        xc, yc = self.calc_circ()
        self.plot_handle[0].set_data(xc,yc)

    def update(self, dt):
        self.pos = self.pos + self.vel*dt

    def v_reflect(self, dir):
        self.vel[dir] = -self.vel[dir]

    def check_collide(self, other_ball):
        """
        Checks if two balls collide
        Input: self, other_ball
        Output: True or False
        Usage: check_collide(ball2)
        Returns: False
        """

        #Calculates distance between ball and other ball
        dist = np.linalg.norm(self.pos - other_ball.pos)

        #Checks if distance is less than both radii and returns T/F accordingly
        if dist < self.radius + other_ball.radius:
            return True
        else:
            return False
        
    def v_ball_collision(self, other_ball):
        """
        Calculates velocities of two balls after collision
        Input: self, other_ball
        Output: None
        Usage: v_ball_collision(ball2)
        Returns: None
        """
        #finds initial direction of the collision
        collision_dir = (other_ball.pos - self.pos) / np.linalg.norm(other_ball.pos - self.pos)

        # Calculate initial velocities in collision direction
        self_v_init = np.dot(self.vel, collision_dir)
        other_v_init = np.dot(other_ball.vel, collision_dir)

        # Calculate new velocities in collision direction using the given formulas
        self_v_final= self_v_init - (((self_v_init-other_v_init)*(self.pos-other_ball.pos))/((abs(self.pos-other_ball.pos))**2))*(self.pos-other_ball.pos)
        other_v_final = other_v_init - (((other_v_init-self_v_init)*(other_ball.pos-self.pos))/((abs(other_ball.pos-self.pos))**2))*(other_ball.pos-self.pos)

        # Calculate the final velocities in the other orthogonal direction
        self_v_final_ortho = self.vel - self_v_init * collision_dir
        other_v_final_ortho = other_ball.vel - other_v_init * collision_dir 

        # Set the final velocities
        self.vel = self_v_final * collision_dir + self_v_final_ortho
        other_ball.vel = other_v_final * collision_dir + other_v_final_ortho

class BlueBall(Ball):
    """ This subclass inherits from the ball class and creates a blue ball object
    """
    def __init__(self):
        super().__init__(color='b')
        
class RedBall(Ball):
    """ This subclass inherits from the ball class and creates a red ball object
    """
    def __init__(self):
        super().__init__(color='r')

class Billiards(object):
    def __init__(self, h, w):
        # Billiard table parameters
        self.current_time = 0
        self.height = h
        self.width = w

        # Plotting information
        self.fig = []

        # Balls on the table
        self.ball = []

    def add_ball(self):
        """
        Asks user for input on number of balls of each color and adds to ball list
        Input: self
        Output: None
        Usage: add_ball()
        Returns: None
        """
        #asks user how many red and blue balls and sets to integers
        num_red=(int(input("How many red balls? (Integer value)")))
        num_blue=(int(input("How many blue balls? (Integer values)")))

        #for loop based on number of red balls
        for i in range(num_red):
            ball=RedBall()
            #add red balls to list of balls
            self.ball.append(ball)
        
        #for loop based on number of blue balls
        for i in range(num_blue):
            ball=BlueBall()
            #adds blue balls to list of balls
            self.ball.append(ball)
    
    def setup_animation(self):
        # We haven't see this line before. It basically sets the interactive property
        # of the plot so that we can update the plot repeatedly in the code
        plt.ion()

        self.fig = plt.figure()
        plt.plot([0,0,self.width,self.width,0], [0,self.height,self.height,0,0], '-k')
        plt.axis('equal')
        plt.show()

    def redraw(self):
        #updates balls that are in the self.ball list
        for ball in self.ball:
            ball.redraw()

        plt.title("Current time: "+str(self.current_time))

        # These next two lines force the plot to update
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def is_closed(self):
        return not plt.fignum_exists(self.fig.number)

    def update(self, dt):
        """
        Updates balls at each time step
        Input: self, dt
        Output: None
        Usage: update(.01)
        Returns: Updated ball animation
        """
        # Continuous update
        #checks ball object is in ball list and updates 
        for ball in self.ball:
            ball.update(dt)

            #discrete transitions
            #checks for collision with wall and reflects velocity
            did_collide, reflect_dir = self.check_collide_wall(ball)
            if did_collide:
                ball.v_reflect(reflect_dir)

        # checks for ball collisions with each other
        self.handle_collide_balls()

        # Update time
        self.current_time = self.current_time + dt

        # Animate all balls
        self.redraw()

    def check_collide_wall(self, the_ball):
        if the_ball.pos[0] > self.width-the_ball.radius:
            return True, 0
        if the_ball.pos[0] < the_ball.radius:
            return True, 0
        if the_ball.pos[1] > self.height-the_ball.radius:
            return True, 1
        if the_ball.pos[1] < the_ball.radius:
            return True, 1
        
        return False, None
    
    def handle_collide_balls(self):
        """
        Checks if two balls collide and changes velocities
        Input: self
        Output: None
        Usage: handle_collide_balls
        Returns: None
        """
        # Check all pairs of balls for collisions
        for i in range(len(self.ball)):
            for j in range(i+1, len(self.ball)):
                ball1 = self.ball[i]
                ball2 = self.ball[j]

                #checks if two balls collide and if they do, change velocities
                if ball1.check_collide(ball2):
                    ball1.v_ball_collision(ball2)

# Initialize
billiard_sim = Billiards(10,10)
billiard_sim.setup_animation()
billiard_sim.add_ball()

# Simulate
dt = 0.1
Tf = 10
while (billiard_sim.current_time < Tf) and (not billiard_sim.is_closed()):
    billiard_sim.update(dt)
    plt.pause(dt)

plt.title('Simulation complete. Close the figure to exit')
while not billiard_sim.is_closed():
    plt.pause(1)