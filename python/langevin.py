import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt

def H(x):
    return x**4
def f(x):
    return -4*(x**3)
Z=0.906402*2
# 目的の分布はexp(-H(x))/Z

T=10000
x=0
eps=0.1
X=[]
for t in range(T):
    g=np.random.normal()
    try:
        x=x+eps*f(x)+g*(2*eps)**0.5
        X.append(x)
    except:
        break
T=len(X)
plt.xlim(-3,3)
plt.ylim(0,0.7)
title="t="+str(T)
plt.title(title)
plt.hist(X,density=True,bins=100)
x_range=np.linspace(-3,3,1000)
y_range=np.exp(-H(x_range))/Z
plt.plot(x_range,y_range)
now=dt.now().strftime("%Y%m%d%H%M%S")
name="image/langevin_monte_carlo"+now+".png"
plt.savefig(name)

plt.figure()
plt.ylim(-10,10)
plt.plot(range(T),X)
plt.title("eps="+str(eps))
name="image/langevin_monte_carlo_path"+now+".png"
plt.savefig(name)