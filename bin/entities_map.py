#!/usr/bin/env python3
# Description: Plots entities on radars
# Author: Tyler "-z-" Mulligan

from matplotlib import pyplot as plt
import numpy as np
import matplotlib

radar_image = 'resources/radars/gfx/gasoline_02_mini.png'

fig, ax = plt.subplots()

plt.axis('off')

# zipped = [
#     (1, 1),
#     (45, 4),
#     (8, 38),
#     (12, 12),
#     (20, 210),
#     (420, 40),
#     (420, 140),
# ]

zipped = [('128', '5600'), ('-128', '5600'), ('0', '-2176'), ('0', '-2176'), ('0.000000', '4352.000000'), ('576', '4096'), ('-576', '4096'), ('0', '1856'), ('448', '1664'), ('-448', '1664'), ('448', '1408'), ('-448', '1408'), ('480', '256'), ('-480', '256'), ('-320', '0'), ('320', '0'), ('-64', '-1984'), ('64', '-1984'), ('480', '-256'), ('-480', '-256'), ('0.000000', '1536.000000'), ('160.000000', '4800.000000'), ('-160.000000', '4800.000000'), ('-320', '3072'), ('320', '3072'), ('480', '3328'), ('-480', '3328'), ('128', '-2528'), ('-128', '-2528'), ('0', '-2112'), ('0', '5248'), ('0', '5248'), ('0.000000', '-1280.000000'), ('-544.000000', '-2080.000000'), ('-256', '-1664'), ('0.000000', '-2432.000000'), ('0.000000', '-2752.000000'), ('256', '-1664'), ('544.000000', '-2080.000000'), ('576', '-1024'), ('-576', '-1024'), ('480', '2816'), ('-480', '2816'), ('-64', '5056'), ('64', '5056'), ('160.000000', '-1728.000000'), ('-160.000000', '-1728.000000'), ('-544.000000', '5152.000000'), ('-256', '4736'), ('0.000000', '5504.000000'), ('0.000000', '5824.000000'), ('256', '4736'), ('544.000000', '5152.000000'), ('0', '5184'), ('448.000000', '1536.000000'), ('0.000000', '960.000000'), ('0.000000', '2112.000000'), ('-448.000000', '1536.000000'), ('0', '1216'), ('0', '-1728'), ('0', '4800'), ('-448.000000', '1536.000000'), ('448.000000', '1536.000000'), ('0.000000', '1536.000000'), ('0.000000', '1504.000000'), ('0.000000', '1568.000000'), ('0.000000', '1536.000000'), ('0.000000', '-2112.000000'), ('0.000000', '5184.000000'), ('-320.000000', '5376.000000'), ('320.000000', '5376.000000'), ('-320.000000', '-2304.000000'), ('320.000000', '-2304.000000'), ('-224.000000', '1152.000000'), ('224.000000', '1920.000000'), ('0.000000', '1536.000000'), ('448', '1536'), ('-448', '1536'), ('0.000000', '1536.000000'), ('0.000000', '1536.000000'), ('448.000000', '1536.000000'), ('-448.000000', '1536.000000'), ('0.000000', '2336.000000'), ('0.000000', '736.000000'), ('0.000000', '1536.000000'), ('608', '5536'), ('736', '5472'), ('736', '5600'), ('672', '5472'), ('608', '5472'), ('672', '5600'), ('736', '5536'), ('64.000000', '1152.000000'), ('-64.000000', '1152.000000'), ('608', '-2400'), ('736', '-2464'), ('672', '-2528'), ('608', '-2464'), ('-64.000000', '1088.000000'), ('736', '-2528'), ('736', '-2400'), ('672', '-2400'), ('608', '-2528'), ('-672', '-2400'), ('-608', '-2528'), ('64.000000', '1088.000000'), ('-736', '-2400'), ('-160.000000', '-1504.000000'), ('160.000000', '-1504.000000'), ('-608', '-2400'), ('-672', '-2528'), ('160.000000', '-1552.000000'), ('-736', '-2464'), ('-736', '-2528'), ('-160.000000', '-1648.000000'), ('-160.000000', '-1552.000000'), ('-608', '-2464'), ('160.000000', '-1648.000000'), ('-160.000000', '4720.000000'), ('-736', '5472'), ('160.000000', '4576.000000'), ('-160.000000', '4624.000000'), ('-672', '5600'), ('160.000000', '4720.000000'), ('-160.000000', '4576.000000'), ('-736', '5536'), ('-736', '5600'), ('-608', '5536'), ('-672', '5472'), ('160.000000', '4624.000000'), ('608', '5600'), ('-608', '5472'), ('-608', '5600'), ('-64.000000', '1920.000000'), ('64.000000', '1920.000000'), ('-64.000000', '1984.000000'), ('64.000000', '1984.000000'), ('-32', '1344'), ('-224', '1344'), ('32', '1728'), ('-32', '1728'), ('224', '1728'), ('224', '1344'), ('32', '1344'), ('-224', '1728'), ('64', '1216'), ('-64', '1216'), ('64', '1856'), ('-64', '1856'), ('-160.000000', '4672.000000'), ('-160.000000', '-1600.000000'), ('160.000000', '-1600.000000'), ('160.000000', '4672.000000'), ('192', '-1024'), ('192', '-960'), ('192', '-896'), ('-192', '-1024'), ('192', '-832'), ('-192', '-832'), ('-192', '-896'), ('-192', '-960'), ('128', '-1088'), ('-128', '-1088'), ('64', '-1088'), ('-64', '-1088'), ('0', '-1088'), ('192', '4096'), ('192', '4032'), ('192', '3968'), ('-192', '4096'), ('-192', '3968'), ('-192', '3904'), ('-192', '4032'), ('-128', '4160'), ('64', '4160'), ('128', '4160'), ('192', '3904'), ('0', '4160'), ('-64', '4160'), ('128', '1728'), ('128', '1344'), ('-128', '1344'), ('-128', '1728'), ('672', '5536'), ('672', '-2464'), ('0', '-2368'), ('-672', '-2464'), ('-672', '5536'), ('0', '5440'), ('192', '1856'), ('-192', '1856'), ('192', '1216'), ('-192', '1216'), ('448.000000', '1536.000000'), ('-448.000000', '1536.000000'), ('0', '-2592'), ('0', '5664'), ('0.000000', '1536.000000'), ('0.000000', '5664.000000'), ('0.000000', '4928.000000'), ('0.000000', '-1856.000000'), ('0.000000', '-2592.000000'), ('0.000000', '1536.000000')]

x, y = zip(*zipped)
s = [100]

plt.scatter(x, y, s, c="g", alpha=0.5, marker=r'$\clubsuit$')


img = plt.imread(radar_image)

x0, x1 = ax.get_xlim()
y0, y1 = ax.get_ylim()
ax.imshow(img, extent=[x0, x1, y0, y1], aspect='auto')

plt.show()
fig.canvas.draw()

plt.savefig("test.png", bbox_inches='tight')

#plt.imsave('test.jpg', data)

#from PIL import Image
#im = Image.fromarray(plt)
#im.save("your_file.jpeg")
