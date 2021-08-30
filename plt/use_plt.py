import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-1, 1, 50)
y = x * 3 +  1
#print(x)
plt.plot(x, y)
plt.show()
y1 = x ** 4
plt.plot(x, y1)
plt.show()