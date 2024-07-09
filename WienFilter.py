from math import sin, cos, pi
from time import time
from matplotlib import pyplot as plt
from matplotlib.patches import Patch

ELECTRON_CHARGE = 1.602176621e-19 # C
ELECTRON_MASS = 9.10938356e-31 # kg
PROTON_MASS = 1.672621898e-27 # kg


B_FIELD_DEFAULT = 7.5e-2 # T
E_FIELD_DEFAULT = 3.75e4 # N/C
V_0_DEFAULT = E_FIELD_DEFAULT / B_FIELD_DEFAULT # m/s
Q_DEFAULT = 1.6022e-19 # C electron charge
M_DEFAULT = 1.6726e-27 # kg proton mass
WIDTH_DEFAULT = 0.20 # m
HEIGHT_DEFAULT = 0.10 # m
RESOLUTION_DEFAULT = 1.0e-9 # s


b_field = 0
e_field = 0
v_0 = 0
q = 0
m = 0

width = 0
height = 0

resolution = 0

num_arrows = 8

def x(t):
    return v_0 * t + ((e_field - b_field * v_0) / b_field) * (t - m / (q * b_field) * sin(q * b_field * t / m))

def y(t):
    return m * (e_field - b_field * v_0) / (q * b_field * b_field) * (1 - cos(q * b_field * t / m))

print('enter empty string for default, use e.g. 0.1e+2 or 4e-3')
b_str = input(f'B= (default {B_FIELD_DEFAULT}, > 0, in T)')
if b_str.isspace() or len(b_str) == 0:
    b_field = B_FIELD_DEFAULT
else:
    b_field = float(b_str)
if b_field <= 0:
    print(f'B must be > 0, but was {b_field}')
    exit(-1)

e_str = input(f'E= (default {E_FIELD_DEFAULT}, >= 0, in N/C)')
if e_str.isspace() or len(e_str) == 0:
    e_field = E_FIELD_DEFAULT
else:
    e_field = float(e_str)
if e_field < 0:
    print(f'E must be >= 0, but was {e_field}')
    exit(-1)

v_0_str = input(f'v_0= (default {V_0_DEFAULT} = E/B, > 0, in m/s)')
if v_0_str.isspace() or len(v_0_str) == 0:
    v_0 = V_0_DEFAULT
else:
    v_0 = float(v_0_str)
if v_0 <= 0:
    print(f'v_0 must be > 0, but was {v_0}')
    exit(-1)

q_str = input(f'q= (default {Q_DEFAULT}, e=-1.6022e-19C, p=1.6022e-19C, in C)')
if q_str.isspace() or len(q_str) == 0:
    q = Q_DEFAULT
elif q_str.strip() == 'e':
    q = ELECTRON_CHARGE
elif q_str.strip() == 'p':
    q = -ELECTRON_CHARGE
else:
    q = float(q_str)

m_str = input(f'm= (default {M_DEFAULT}, me=9.1094e-31kg, mp=1.6726e-27kg, in kg)')
if m_str.isspace() or len(m_str) == 0:
    m = M_DEFAULT
elif m_str.strip() == 'me':
    m = ELECTRON_MASS
elif m_str.strip() == 'mp':
    m = PROTON_MASS
else:
    m = float(m_str)

w_str = input(f'width= (default {WIDTH_DEFAULT}, > 0, in m)')
if w_str.isspace() or len(w_str) == 0:
    width = WIDTH_DEFAULT
else:
    width = float(w_str)
if width <= 0:
    print(f'width must be > 0, but was {width}')
    exit(-1)

h_str = input(f'height= (default {HEIGHT_DEFAULT}, > 0, in m)')
if h_str.isspace() or len(h_str) == 0:
    height = HEIGHT_DEFAULT
else:
    height = float(h_str)
if height <= 0:
    print(f'width must be > 0, but was {height}')
    exit(-1)

r_str = input(f'resulution= (default {RESOLUTION_DEFAULT}, time between points, in s)')
if r_str.isspace() or len(r_str) == 0:
    resolution = RESOLUTION_DEFAULT
else:
    resolution = float(r_str)
if resolution <= 0:
    print(f'width must be > 0, but was {resolution}')
    exit(-1)


points = [(0, 0)]
start_time = time()
point = (0, 0)
t = 0

while not (point[0] < 0.0 or point[0] > width or abs(point[1]) > height / 2):
    point = (x(t), y(t))
    points.append(point)
    t += resolution
    if len(points) > 10000:
        print('Stopped calculation, because to many points where calculated. Maybe try a longer time as resolution.')

#points.sort(key=lambda x: x[0])
x_s, y_s = zip(*points)

for i in range(1, num_arrows):
    x_pos = (width / num_arrows) * i
    y_pos = -(height/2) if e_field > 0 else (height/2)
    y_pos = y_pos * 0.95
    dy = height if e_field > 0 else -height
    dy = dy * 0.90
    plt.arrow(x_pos, y_pos, 0, dy, width=width/num_arrows/100, head_width=width/num_arrows/10, color='lightgreen')

for i in range(0, num_arrows):
    radius = width/num_arrows/7
    x_pos = (width / num_arrows) * i + width / num_arrows / 2

    num_arrows_y = int(num_arrows * (height / width))

    for j in range(-num_arrows_y//2, num_arrows_y//2):
        y_pos = (height / num_arrows_y) * j + height / num_arrows_y / 2

        plt.gca().add_patch(plt.Circle((x_pos, y_pos), radius=radius, fill=False, color='green'))

        if b_field > 0:
            # arrows out of the screen plane
            plt.gca().add_patch(plt.Circle((x_pos, y_pos), radius=radius/5, color='green'))
        else:
            radius = radius * sin(1/4 * pi)
            plt.plot([x_pos-radius, x_pos+radius], [y_pos-radius, y_pos+radius], color='green')
            plt.plot([x_pos-radius, x_pos+radius], [y_pos+radius, y_pos-radius], color='green')


plt.plot(x_s, y_s, color='blue')


legend_elements = [Patch(color='lightgreen', label=f'E={e_field:.4E}N/C'),
                   Patch(color='green', label=f'B={b_field:.4E}T'),
                   Patch(color='blue', label=f'Particle v_0={v_0:.4E}m/s, q={q:.4E}C, m={m:.4E}kg'),
                   ]

plt.gca().legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.4))

plt.xlabel('x in m')
plt.ylabel('y in m')
plt.axis('square')
plt.axis([0, width, -(height / 2), height / 2])
plt.show()
