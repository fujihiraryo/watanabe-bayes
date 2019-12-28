import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from datetime import datetime as dt

def p(x):
    return (x**3)*np.exp(-x)

T=10000
X=[]
x=4
sigma_list=np.linspace(1,20,100)
accept_rate_list=[]
for sigma in sigma_list:
    accept=0
    for t in range(T):
        x_new=np.random.normal(x,sigma)
        u=np.random.random()
        if u<p(x_new)/p(x):
            accept+=1
        else:
            x_new=x
        X.append(x_new)
        x=x_new
    accept_rate_list.append(accept/T)
plt.plot(sigma_list,accept_rate_list)
plt.title("t="+str(T))
plt.xlabel("sigma")
plt.ylabel("accept_rate")
now=dt.now().strftime("%Y%m%d%H%M%S")
name="image/metropolis_accept_rate"+now+".png"
plt.savefig(name)
