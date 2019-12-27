import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image
from datetime import datetime as dt

def p(x,a,b):
    p0=np.exp(-x**2/2)/(2*np.pi)**(1/2)
    p1=np.exp(-(x-b)**2/2)/(2*np.pi)**(1/2)
    return (1-a)*p0+a*p1

# 真のパラメータ
a0=0.5
b0=0

# サンプル数
N=100

# サンプル生成
X=[]
for n in range(N):
    u=np.random.random()
    if u<1-a0:
        x=np.random.normal(0,1)
        X.append(x)
    else:
        x=np.random.normal(b0,1)
        X.append(x)

images=[]
for n in range(1,N+1):
    a_range=np.linspace(0,1,100)
    b_range=np.linspace(-5,5,100)
    a,b=np.meshgrid(a_range,b_range)
    c=np.exp(sum([np.log(p(X[i],a,b)) for i in range(n)]))
    plt.contour(a,b,c)
    title="(a0,b0)="+"("+str(a0)+","+str(b0)+"), "+"n="+str(n)
    plt.title(title)
    #画像保存
    buf=io.BytesIO()
    plt.savefig(buf,format="png")
    images.append(Image.open(buf))
    plt.close()

#gifを作成して保存
now=dt.now().strftime("%Y%m%d%H%M%S")
name="gif/likelihood"+now+".gif"
images[0].save(name, save_all=True, append_images=images[1:], duration=10, loop=0)
buf.close()
print("complete")
