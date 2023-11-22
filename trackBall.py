#import modules
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def isOpen(f):
    return plt.fignum_exists(f.number)

def calc_center_pixels(v1,v2,height,width):
    """Calculates the center of the ball in pixels
        Inputs: v1= video
                v2= video
                height= integer
                width= integer
        Outputs: center_x1 = 1d np array
                center_y1 = 1d np array
                center_x2 = 1d np array
                center_y2 = 1d np array
        Usage: calc_center_pixels(v1,v2,height,width)
            Returns: []...[]...[], [128.6341,178.3053...]
    """
    # set up plotting
    plt.ion()
    fig, ax = plt.subplots(2,2)

    #sets up left video and mask/center
    h_img_left = ax[0,0].imshow(np.zeros((height,width,3)))
    h_ball_left = ax[1,0].imshow(np.ones((height,width)), cmap='viridis', vmin=0, vmax=1)
    h_center_left = ax[1,0].plot(0,0,'*r')[0]

    #sets up right video and mask/center
    h_img_right = ax[0,1].imshow(np.zeros((height,width,3)))
    h_ball_right = ax[1,1].imshow(np.ones((height,width)), cmap='viridis', vmin=0, vmax=1)
    h_center_right = ax[1,1].plot(0,0,'*r')[0]

    plt.show()

    #sets empty arrays for center of the ball in pixels
    center_x1=[]
    center_y1=[]
    center_x2=[]
    center_y2=[]

    # start processing video
    while v1.isOpened() and v2.isOpened() and isOpen(fig):
        has_frame1, img1 = v1.read()
        has_frame2, img2 = v2.read()

        if has_frame1 and has_frame2:
            
            #display right video
            img_plt_right = cv.cvtColor(img1, cv.COLOR_BGR2RGB)
            h_img_right.set_data(img_plt_right)
            ax[0,1].set_title("Right Camera")
            ax[1,1].set_title("Right Mask")

            #display left video
            img_plt_left = cv.cvtColor(img2, cv.COLOR_BGR2RGB)
            h_img_left.set_data(img_plt_left)
            ax[0,0].set_title("Left Camera")
            ax[1,0].set_title("Left Mask")

            # isplay right mask
            img_hsv_right = cv.cvtColor(img1, cv.COLOR_BGR2HSV)
            mask_h1 = (img_hsv_right[:,:,0] > 0) & (img_hsv_right[:,:,0] < 30)
            mask_s1 = (img_hsv_right[:,:,1] > 160)
            mask_v1 = (img_hsv_right[:,:,2] > 110)
            mask1 = mask_h1 & mask_s1 & mask_v1
            h_ball_right.set_data(1*mask1)

            #display left mask
            img_hsv_left = cv.cvtColor(img2, cv.COLOR_BGR2HSV)
            mask_h2 = (img_hsv_left[:,:,0] > 0) & (img_hsv_left[:,:,0] < 30)
            mask_s2 = (img_hsv_left[:,:,1] > 160)
            mask_v2 = (img_hsv_left[:,:,2] > 110)
            mask2 = mask_h2 & mask_s2 & mask_v2
            h_ball_left.set_data(1*mask2)

            #calculate right ball center
            row1,col1 = np.where(mask1)
            x_mid1 = np.mean(col1)
            y_mid1 = np.mean(row1)
            h_center_right.set_data(x_mid1,y_mid1)
            center_x1.append(x_mid1)
            center_y1.append(y_mid1)

            #calculate left ball center
            row2,col2 = np.where(mask2)
            x_mid2 = np.mean(col2)
            y_mid2 = np.mean(row2)
            h_center_left.set_data(x_mid2,y_mid2)
            center_x2.append(x_mid2)
            center_y2.append(y_mid2)
            
            fig.canvas.draw()
            fig.canvas.flush_events()
            
        else:
            break
            
    v1.release()
    v2.release()
    cv.destroyAllWindows()
    plt.ioff()

    return center_x1,center_y1,center_x2,center_y2

def calc_center_inches(scale,centerx,centery,width,height):
    """Calculates the center of the ball in inches
        Inputs: scale = float
                centerx = 1d np array
                centery = 1d np array
                width = integer
                height = integer
        Outputs: center_x = 1d np array
                center_7 = 1d np array
        Usage: calc_center_inches(scale,centerx,centery,width,height)
            Returns: 128.6341,171.4569...
    """
    #sets np arrays of length of original arrays
    center_x=np.zeros(len(centerx))
    center_y=np.zeros(len(centery))

    #for loop that interates length of inputs
    for i in range(len(centerx)):
        #calculates center in inches by multiplying by scale
        center_x[i]=(centerx[i] - width / 2) * (scale)
        center_y[i]=((height / 2)- centery[i]) * (scale)

    return center_x,center_y

def plot_ball_center(center_leftx1,center_lefty1,center_rightx2, center_righty2):
    """Plots center of ball from left and right camera
    Inputs: center_leftx1: 1d np array
        center_lefty1: 1d np array
        center_rightx2: 1d np array
        center_righty2: 1d np array
    Outputs: Plot of left and right views
    Usage: plot_ball_center(center_leftx1,center_lefty1,center_rightx2, center_righty2)
        Return: plot
    """
    #sets up plots
    fix,ax=plt.subplots(1,2)

    #plots center of left ball
    ax[0].plot(center_leftx1,center_lefty1,'r')
    ax[0].set_xlabel("X Position (Inches)")
    ax[0].set_ylabel("Y Position (Inches)")
    ax[0].set_title("Left Camera - Ball Center")

    #plots center of right ball
    ax[1].plot(center_rightx2,center_righty2,'r')
    ax[1].set_xlabel("X Position (Inches)")
    ax[1].set_ylabel("Y Position (Inches)")
    ax[1].set_title("Right Camera - Ball Center")
    plt.show()

def calc_3dtrajectory(f,d,center1_x_inches, center2_x_inches, center2_y_inches):
    """Calculates x, y, z positions of the ball in scene coordinates
        Inputs: f = integer
                d = integer
                center1_x_inches = 1d np array
                center2_x_inches = 1d np array
                center2_y_inches = 1d np array
        Outputs: ball_pos_z = 1d np array
                ball_pos_x = 1d np array
                ball_pos_y = 1d np array
        Usage: calc_3dtrajectory(f,d,center1_x_inches, center2_x_inches, center2_y_inches)
            Returns: pos_x, pos_y, pos_z
    """
    #creates array length of inputs
    pos_z=np.zeros(len(center1_x_inches))
    pos_x=np.zeros(len(center1_x_inches))
    pos_y=np.zeros(len(center1_x_inches))

    #for loop that iterates length of inputs
    for i in range(len(center1_x_inches)):
    #calculates the true position of the ball
        pos_z[i]=(f*d)/(center2_x_inches[i]-center1_x_inches[i])
        pos_x[i]=((pos_z[i]/f)*center2_x_inches[i])-(d/2)
        pos_y[i]=(pos_z[i]/f)*center2_y_inches[i]
    
    return pos_x, pos_y, pos_z

def plot_3dtrajectory(pos_x,pos_y,pos_z):
    """plots 3d trajectory of the ball
        Inputs: pos_x = 1d np array
                pos_y = 1d np array
                pos_z = 1d np array
        Outputs: plot
        Usage: plot_3dtrajectory(pos_x,pos_y,pos_z)
            Returns: 3d plot
    """
    #plots 3d trajectory
    fig=plt.figure()
    ax = plt.figure().add_subplot(111,projection='3d')
    ax.plot(pos_x,pos_y,pos_z, label='3D Plot of Ball Trajectory')
    ax.set_xlabel("X Position (inches)")
    ax.set_ylabel("Y Position (inches)")
    ax.set_zlabel("Z Position (inches)")
    ax.set_title("3D Plot of Ball Trajectory")
    ax.legend
    plt.show()

def plot_2dtrajectory(pos_x,pos_y, pos_z,time):
    """plots 2d trajectory of the ball
        Inputs: pos_x = 1d np array
                pos_y = 1d np array
                pos_z = 1d np array
                time = 1d np array
        Outputs: plot
        Usage: plot_2dtrajectory(pos_x, pos_y, pos_z)
            Returns: 2d plot
    """
    #plots 2d trajectory
    fig,ax=plt.subplots()
    ax.plot(time, pos_x, label="X")
    ax.plot(time, pos_y, label="Y")
    ax.plot(time, pos_z, label="Z")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Distance (Inches)")
    ax.set_title("2D Plot of Ball Trajectory")
    ax.legend()
    plt.show()

#sets constants
f=3
d=3
scale=.02

# load in right video
v1 = cv.VideoCapture('right.mp4')

#loads in left video
v2 = cv.VideoCapture('left.mp4')

#gets video properties
Nframes = int(v1.get(cv.CAP_PROP_FRAME_COUNT))
width = int(v1.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(v1.get(cv.CAP_PROP_FRAME_HEIGHT))

#get fps
fps=v1.get(cv.CAP_PROP_FPS)

#calculate video time
seconds=round(Nframes/fps)
time=np.arange(0,seconds,seconds/(Nframes-1))

#calculates center of the ball in pixels
center1_x_pixels, center1_y_pixels, center2_x_pixels, center2_y_pixels=calc_center_pixels(v1,v2,height,width)

#calculates center of the ball in inches of the right camera
center1_x_inches, center1_y_inches=calc_center_inches(scale,center1_x_pixels, center1_y_pixels,width,height)

#calculates center of the ball in inches of the left camera
center2_x_inches, center2_y_inches=calc_center_inches(scale,center2_x_pixels, center2_y_pixels,width,height)

#plots center of the left and right camera balls
plot_ball_center(center2_x_inches, center2_y_inches,center1_x_inches, center1_y_inches,)

#calculates x, y, z coordinates over time
pos_x, pos_y, pos_z=calc_3dtrajectory(f,d,center1_x_inches, center2_x_inches, center2_y_inches)

#plots 2d trajectory over time
plot_2dtrajectory(pos_x, pos_y,pos_z,time)

#plots 3d trajectory over time
plot_3dtrajectory(pos_x,pos_y,pos_z)


