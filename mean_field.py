import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image
from datetime import datetime as dt
from scipy.special import psi

#サンプル生成
X1=np.random.multivariate_normal([0,3],[[1,0],[0,1]],30)
X2=np.random.multivariate_normal([2,-2],[[1,0],[0,1]],45)
X3=np.random.multivariate_normal([-3,-3],[[1,0],[0,1]],25)
X=np.concatenate((X1,X2,X3),axis=0)

N=len(X) #サンプル数
T=30 #くりかえし回数
K=3 #コンポーネント数

#ハイパラの初期値
phi=[1 for k in range(K)]
mu=[np.zeros(2)+np.random.rand(2)/10 for k in range(K)]
tau=[1 for k in range(K)]

images=[]
for t in range(T):
    #描画準備
    plt.figure(figsize=(10,10))
    plt.xlim(-5,5)
    plt.ylim(-5,5)
    plt.title("N="+str(N)+", iter="+str(t))

    #サンプルの散布図
    plt.scatter(X1[:,0],X1[:,1])
    plt.scatter(X2[:,0],X2[:,1])
    plt.scatter(X3[:,0],X3[:,1])

    #予測分布の等高線
    lin=np.linspace(-5,5,100)
    x0,x1=np.meshgrid(lin,lin)
    p_predict=0
    for k in range(K):
        p_predict_k=1
        p_predict_k*=(phi[k]/(N+K))*(1/(2*np.pi))*(tau[k]/(1+tau[k]))
        p_predict_k*=np.exp(-((x0-mu[k][0])**2+(x1-mu[k][1])**2)*tau[k]/(2*(1+tau[k])))
        p_predict+=p_predict_k
    plt.contour(x0,x1,p_predict)

    #画像保存
    buf=io.BytesIO()
    plt.savefig(buf,format="png")
    images.append(Image.open(buf))
    plt.close()

    #隠れ変数の推定
    L=[]
    for i in range(N):
        Li=[]
        for k in range(K):
            Lik=psi(phi[k])-psi(sum(phi))-1/tau[k]
            Lik=Lik-((X[i][0]-mu[k][0])**2+(X[i][1]-mu[k][1])**2)/2
            Li.append(Lik)
        L.append(Li)
    Y=[]
    for i in range(N):
        Yi=[]
        for k in range(K):
            Yik=np.exp(L[i][k])/sum([np.exp(L[i][k]) for k in range(K)])
            Yi.append(Yik)
        Y.append(Yi)

    #ハイパラ更新
    for k in range(K):
        phi[k]=phi[k]+sum([Y[i][k] for i in range(N)])
        mu[k]=(tau[k]*mu[k]+sum([X[i]*Y[i][k] for i in range(N)]))/(tau[k]+sum([Y[i][k] for i in range(N)]))
        tau[k]=tau[k]+sum([Y[i][k] for i in range(N)])

#gifを作成して保存
now=dt.now().strftime("%Y%m%d%H%M%S")
name="mean_field"+now+".gif"
images[0].save(name, save_all=True, append_images=images[1:], duration=10, loop=0)
buf.close()
print("complete")
