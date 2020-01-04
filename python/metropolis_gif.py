import numpy as np
import matplotlib.pyplot as plt
import io
from tqdm import tqdm
from PIL import Image
from datetime import datetime as dt
from scipy.stats import gamma
from scipy.stats import norm

def p(x):
    return (x**3)*np.exp(-x)

T=50
X=[]
x=4
sigma=4
accept=0
images=[]
for t in tqdm(range(T)):
    x_new=np.random.normal(4,4)
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
    title+="accept_rate="+str(round(accept/(t+1),2))
    plt.title(title)
    plt.hist(X,density=True,bins=100)
    x_range=np.linspace(0,10,1000)
    y_range=gamma(4).pdf(x_range)
    plt.plot(x_range,y_range)
    #画像保存
    buf=io.BytesIO()
    plt.savefig(buf,format="png")
    images.append(Image.open(buf))
    plt.close()
#gifを作成して保存
now=dt.now().strftime("%Y%m%d%H%M%S")
name="gif/metropolis"+now+".gif"
images[0].save(name, save_all=True, append_images=images[1:], duration=0.01, loop=0)
buf.close()
