import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 50)
y1 = 3*x + 2
y2 = x**2

plt.figure()

plt.xlim(-1, 2)
plt.ylim(-2, 3)
plt.xlabel("1 and x")
plt.ylabel('1 and y')
new_ticks = np.linspace(-1, 2, 5)
print(new_ticks)
plt.xticks(new_ticks)
plt.yticks([-2, -1.8, -1, 1.22, 3,],
    [r'$relly\ bad$', r'$bad\ \alpha$', r'$normal$', r'$good$', r'$relly\ good$'])
#gca = 'get current axis'
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))

l1, = plt.plot(x, y2, label='up')
l2, = plt.plot(x, y1, color='red', linewidth=1.0, linestyle='--', label='down')

plt.legend(handles=[l1, l2,], labels=['aaa', 'bbb'], loc='best')

x0 = 1.25
y0 = x0**2
plt.scatter(x0, y0, s=50, color='b')
plt.plot([x0, x0], [y0, 0], 'k--', lw=2.5)

#methon 1
plt.annotate(r'$x**2=%s$' % y0, xy=(x0, y0), xycoords='data', xytext=(+30, -30),
             textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))
# plt.annotate(r'$x**2=%s$' % y0, xy=(x0+0.25, y0), xycoords='data')
#method 2
plt.text(-0.5, 1.5, r'$This\ is\ the\ some\ text. \mu\ \sigma_i\ \alpha_t$',
         fontdict={'size': 16, 'color': 'r'})
plt.show()
