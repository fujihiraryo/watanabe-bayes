import numpy as np
import matplotlib.pyplot as plt
import io
from tqdm import tqdm
from PIL import Image
from datetime import datetime as dt
from scipy.stats import gamma

def p(x):
    return (x**3)*np.exp(-x)

T=10000
sigma=30
accept=0
x=4
X=[]
for t in range(T):
    x_new=np.random.normal(x,sigma)
    u=np.random.random()
    if u<p(x_new)/p(x):
        accept+=1
    else:
        x_new=x
    X.append(x_new)
    x=x_new
plt.xlim(0,10)
plt.ylim(0,0.3)
title="t="+str(T)+", "
title+="sigma="+str(sigma)+", "
title+="accept_rate="+str(round(accept/T,2))
plt.title(title)
plt.hist(X,density=True,bins=100)
x_range=np.linspace(0,10,1000)
y_range=gamma(4).pdf(x_range)
plt.plot(x_range,y_range)
now=dt.now().strftime("%Y%m%d%H%M%S")
name="image/metropolis"+now+".png"
plt.savefig(name)
