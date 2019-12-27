import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image
from datetime import datetime as dt
from scipy.stats import dirichlet

#サンプル生成
X1=np.random.multivariate_normal([0,3],[[1,0],[0,1]],30)
X2=np.random.multivariate_normal([1,-1],[[1,0],[0,1]],40)
X3=np.random.multivariate_normal([-3,-3],[[1,0],[0,1]],50)
X=np.concatenate((X1,X2,X3),axis=0)

N=len(X) #サンプル数
T=50 #くりかえし回数
K=3 #コンポーネント数

#パラメータの初期値
a=[1/K]*K
b=[[0,0]]*K

a_list=[a]
b_list=[b]

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

    #予測分布の計算
    lin=np.linspace(-5,5,100)
    x0,x1=np.meshgrid(lin,lin)
    p_predict=0
    for s in range(t+1):
        p_predict_t=0
        a_s=a_list[s]
        b_s=b_list[s]
        for k in range(K):
            p_predict_t_k=1
            p_predict_t_k*=a_s[k]
            p_predict_t_k*=1/(2*np.pi)
            p_predict_t_k*=np.exp(-((x0-b_s[k][0])**2+(x1-b_s[k][1])**2)/2)
            p_predict_t+=p_predict_t_k
        p_predict+=p_predict_t/(t+1)
    plt.contour(x0,x1,p_predict)

    #画像保存
    buf=io.BytesIO()
    plt.savefig(buf,format="png")
    images.append(Image.open(buf))
    plt.close()

    #現在のパラメータ
    a=a_list[t]
    b=b_list[t]

    #Yのサンプリング
    Y=[]
    for i in range(N):
        #Yiの分布
        p_y=[]
        for k in range(K):
            p_y_k=1
            p_y_k*=a[k]
            p_y_k*=np.exp(-((X[i][0]-b[k][0])**2+(X[i][1]-b[k][1])**2)/2)
            p_y.append(p_y_k)
        p_y=np.array(p_y)/sum(p_y)
        Yi=[0]*K
        u=np.random.random()
        for k in range(K):
            if sum(p_y[:k])<u<sum(p_y[:k+1]):
                Yi[k]=1
        Y.append(Yi)

    #ハイパーパラメータの計算
    alpha=[]
    for k in range(K):
        alpha_k=1+sum([Y[i][k] for i in range(N)])
        alpha.append(alpha_k)
    gamma=[1+alpha[k] for k in range(K)]
    beta=[]
    for k in range(K):
        beta_k=sum([X[i]*Y[i][k] for i in range(N)])/gamma[k]
        beta.append(beta_k)

    #a,bのサンプリング
    a=list(dirichlet.rvs(alpha)[0])
    b=[]
    for k in range(K):
        b_k=np.random.normal(beta[k],gamma[k]**(-0.5))
        b.append(b_k)
    a_list.append(a)
    b_list.append(b)

#gifを作成して保存
now=dt.now().strftime("%Y%m%d%H%M%S")
name="gibbs"+now+".gif"
images[0].save(name, save_all=True, append_images=images[1:], duration=10, loop=0)
buf.close()
print("complete")
