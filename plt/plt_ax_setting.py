import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 50)
y1 = 3*x + 2
y2 = x ** 2

plt.figure()
plt.plot(x, y2)
plt.plot(x, y1, color='red', linewidth=1.0, linestyle='--')

plt.xlim(-1, 2)
plt.ylim(-2, 3)
plt.xlabel("1 and x")
plt.ylabel('1 and y')
new_ticks = np.linspace(-1, 2, 5)
print(new_ticks)
plt.xticks(new_ticks)
plt.yticks([-2, -1.8, -1, 1.22, 3,],
    [r'$relly\ bad$', r'$bad\ \alpha$', r'$normal$', r'$good$', r'$relly\ good$'])
plt.show()
