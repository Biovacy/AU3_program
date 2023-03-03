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
theta_panel = degree_to_radian(25)
alpha_panel = degree_to_radian(150)

# Plottar
x = []
y_panel = []
y_available = []

dagen = 15

# Beräkning
year = [day for day in range(dagen, dagen + 1)]

for day in year:

    for hour in np.arange(0, 24, 0.1):

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
        
        
        # print(f"Theta_sun: {radian_to_degree(theta_sun)}, I real: {I}") 

        # print(theta_sun)
        # print( 1 / math.sin(theta_sun) )
        # inside_pow = 1 / math.sin(theta_sun) ** 0.678
        # I = math.pow(1.1 * I_0 * 0.7,  inside_pow.real)
        I = I.real

        if (I < 0):
            I = 0
        
        I_panel = I * ( math.cos(theta_panel - theta_sun) * math.cos(alpha_panel - alpha_sun) + (1 - math.cos(alpha_panel - alpha_sun)) * math.sin(theta_panel) * math.sin(theta_sun))

        if (I_panel < 0):
            I_panel = 0
        
        P_real    = epsilon * I_panel * A
        P_perfect = epsilon * I * A

        print(f"Dag: {day}, Timme: {hour}, effekt: {P_real}")

        x.append(hour)
        y_panel.append(P_real)
        y_available.append(P_perfect)


plt.plot(x, y_available, "b--", label=f"Ideal panels upptagning")
plt.plot(x, y_panel, "m-", label=f"Panelens upptagna energi")
plt.title("15 januari", fontsize=14)
plt.xlabel(r'$t(h)$', fontsize=14)
plt.ylabel(r'$P(W)$', fontsize=14)
plt.tick_params(labelsize=14)
plt.legend(fontsize=14)
plt.show()