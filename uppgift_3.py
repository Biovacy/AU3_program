import matplotlib.pyplot as plt
import numpy as np
import math

# Konvertering mellan radianer och grader
def degree_to_radian(degree):
    return 2 * math.pi * (degree / 360)

def radian_to_degree(radian):
    return (360 * radian) / (2 * math.pi)

# Konstanter
I_0 = 1360  # Solarkonstanten
fi = degree_to_radian(65.6)
A = 30
epsilon = 0.15 
alpha_panel = degree_to_radian(150)

min_effect = 120

# Plottar
x = []
y_panel = []
y_available = []

def effekt_day_hour(day, hour, theta_panel):

    omega = degree_to_radian(15) * hour - degree_to_radian(180)

    delta_sun = degree_to_radian(-23.44) * math.cos(2 * math.pi * day/ 365)
    
    theta_sun = math.asin(  math.sin(fi) * math.sin(delta_sun)  + math.cos(fi) * math.cos(delta_sun) * math.cos(omega) )

    inne_i_acos = round( (math.sin(fi) * math.sin(theta_sun) - math.sin(delta_sun) ) / ( math.cos(fi) * math.cos(theta_sun)), 4) # Avrundningen finns pga python3 suger.


    if (omega < 0):
        alpha_sun = math.pi - math.acos( inne_i_acos )
    else: 
        alpha_sun = math.pi + math.acos( inne_i_acos )
    
    if (theta_sun < 0):
        I = 0
    else: 
        I = 1.1 * I_0 * 0.7 ** (( 1 / math.sin(theta_sun) ) ** 0.678 )

    if (I < 0):
        I = 0
    
    I_panel = I * ( math.cos(theta_panel - theta_sun) * math.cos(alpha_panel - alpha_sun) + (1 - math.cos(alpha_panel - alpha_sun)) * math.sin(theta_panel) * math.sin(theta_sun))

    if (I_panel < 0):
        I_panel = 0
    
    P_real    = epsilon * I_panel * A
    P_perfect = epsilon * I * A

    # print(f"Dag: {day}, Timme: {hour}, effekt: {P_real}")

    return P_real, P_perfect


# Soltimmar för helt år
days = [i for i in range(1, 366)]

max_theta_panel = 0
max_effekt = 0

for theta_panel in range(0, 360, 1):

    total_effekt = 0
    
    for day in days:

        for hour in np.arange(1, 24, 0.1):

            total_effekt += effekt_day_hour(day, hour, degree_to_radian(theta_panel))[0]

    if (total_effekt > max_effekt):
        max_theta_panel = theta_panel
        max_effekt = total_effekt

print("MAX:")
print(f"theta_panel (grader): {max_theta_panel}, max_effekt [kWh]: {max_effekt / 10000}")