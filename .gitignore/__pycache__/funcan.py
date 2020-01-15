import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


fig, ax = plt.subplots()
ax.set_xlim(0, 50)
ax.set_ylim(0, 50)
line1, =  ax.plot([],[])
line2, =  ax.plot([],[])

x = [5,30,15,12,9,30,5,4,3]
y = [12, 40, 34, 24,6,4,2,8]

def update(frame):
    line1.set_xdata(x[:frame+2])
    line1.set_ydata(y[:frame+2])

    # line1.setxdata(x[:frame+2])
    # line1.setydata(y[:frame+2])

    return line1

ani = FuncAnimation(fig, update, frames=5, blit=True, interval = 100)
plt.show()

a = 9
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import numpy as np

# fig, ax1 = plt.subplots(1,1)

# def animate_routes(i,argu):
#     print(i, argu)

#     #graph_data = open('example.txt','r').read()
#     graph_data = "1, 1 \n 2, 4 \n 3, 9 \n 4, 16 \n"
#     lines = graph_data.split('\n')
#     xs = []
#     ys = []
#     for line in lines:
#         if len(line) > 1:
#             x, y = line.split(',')
#             xs.append(float(x))
#             ys.append(float(y)+np.sin(2.*np.pi*i/10))
#         ax1.clear()
#         ax1.plot(xs, ys)
#         plt.grid()

# ani = animation.FuncAnimation(fig, animate_routes, fargs=[5],interval = 100)
# plt.show()

a = 8