import numpy as np
import math

def degree_to_radian(degree):
    return 2 * math.pi * (degree / 360)

def radian_to_degree(radian):
    return (360 * radian) / (2 * math.pi)

I_0 = 1360  # Solarkonstanten
fi = degree_to_radian(55.6)
A = 30
epsilon = 0.15 
theta_panel = degree_to_radian(20)
alpha_panel = math.pi

year = [day for day in range(121, 122)]

for day in year:

    for hour in range(0, 24):

        omega = degree_to_radian(15) * hour - degree_to_radian(180)

        delta_sun = degree_to_radian(-23.44) * math.cos(2 * math.pi * day/ 365)
        
        theta_sun = math.asin(  math.sin(fi) * math.sin(delta_sun)  + math.cos(fi) * math.cos(delta_sun) * math.cos(omega) )

        inne_i_acos = round( (math.sin(fi) * math.sin(theta_sun) - math.sin(delta_sun) ) / ( math.cos(fi) * math.cos(theta_sun)), 4)

        if (omega < 0):
            alpha_sun = math.pi - math.acos( inne_i_acos )
        else: 
            alpha_sun = math.pi + math.acos( inne_i_acos )

        I = 1.1 * I_0 * 0.7 ** (( 1 / math.sin(theta_sun) ) ** 0.678 ) 
        I = I.real

        if (I < 0):
            I = 0

        I_panel = I * ( math.cos(theta_panel - theta_sun) * math.cos(alpha_panel - alpha_sun) + (1 - math.cos(alpha_panel - alpha_sun)) * math.sin(theta_panel) * math.sin(theta_sun))

        if (I_panel < 0):
            I_panel = 0
        
        P = epsilon * I_panel * A

        print(f"Dag: {day}, Timme: {hour}, effekt: {P}")

