import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image
from datetime import datetime as dt

def H(x):
    return x**4
def f(x):
    return -4*(x**3)

T=10000
accept=0
x=1
N=10
eps=0.3
X=[]
for t in range(T):
    y=np.random.normal(0,1)
    x0=x
    y0=y
    for n in range(N):
        y1=y0+f(x0)*eps/2
        x2=x0+y1*eps
        y2=y1+f(x2)*eps/2
        x0=x2
        y0=y2
    u=np.random.random()
    if u<np.exp((y**2-y0**2)/2+H(x)-H(x0)):
        accept+=1
    else:
        x0=x
    x=x0
    X.append(x)
plt.xlim(-3,3)
plt.ylim(0,0.7)
title="t="+str(T)
title+=", leap_flog="+str(N)
title+=", accept_rate="+str(round(accept/T,3))
plt.title(title)
plt.hist(X,density=True,bins=100)
x_range=np.linspace(-3,3,1000)
y_range=np.exp(-H(x_range))/(0.906402*2)
plt.plot(x_range,y_range)
now=dt.now().strftime("%Y%m%d%H%M%S")
name="image/hybrid_monte_carlo"+now+".png"
plt.savefig(name)

plt.figure()
plt.ylim(-3,3)
plt.plot(range(T),X)
title="leap_flog="+str(N)
plt.title(title)
name="image/hybrid_monte_carlo_path"+now+".png"
plt.savefig(name)