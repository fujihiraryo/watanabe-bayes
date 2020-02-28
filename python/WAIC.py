import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt


def p_j(x, y, a, b):
    p0 = (1 - a) * np.exp(-x**2 / 2) / (2 * np.pi)**0.5
    p1 = a * np.exp(-(x - b)**2 / 2) / (2 * np.pi)**0.5
    return (p0**(1 - y)) * (p1**y)


def p(x, a, b):
    return p_j(x, 0, a, b) + p_j(x, 1, a, b)


def prd(x, A, B, K):
    return np.mean([p(x, A[k], B[k]) for k in range(K)])


def main(n=100, a=0.5, b=2, s=1, K=1000, burn=200):
    # n:サンプル数, K:MCMCの遷移回数
    # 真の分布: (1-a)N(0,s)+aN(b,s)からサンプリング
    X = []
    for i in range(2 * n):
        u = np.random.random()
        if u < 1 - a:
            x = np.random.normal(0, 1)
        else:
            x = np.random.normal(b, 1)
        X.append(x)
    # 事後分布からのサンプリング
    A, B = [], []
    alpha = (1, 1)
    beta = 1
    gamma = 1
    mu = 0
    for k in range(K):
        a = np.random.beta(alpha[0], alpha[1])
        b = np.random.normal(mu, gamma**(-0.5))
        Y = []
        for i in range(n):
            u = np.random.random()
            x = X[i]
            if u < p_j(x, 0, a, b) / p(x, a, b):
                Y.append(0)
            else:
                Y.append(1)
        sum_Y = sum(Y)
        sum_XY = sum([X[i] * Y[i] for i in range(n)])
        alpha = alpha[0] + beta * sum_Y, alpha[1] + beta * (n - sum_Y)
        mu = (gamma * mu + beta * sum_XY) / (gamma + beta * sum_Y)
        gamma = gamma + beta * sum_Y
        if k >= burn:
            A.append(a)
            B.append(b)
    K = K - burn
    # 汎化損失などを計算
    T = np.mean([-np.log(prd(X[i], A, B, K)) for i in range(n)])
    G = np.mean([-np.log(prd(X[i], A, B, K)) for i in range(n, 2 * n)])
    AIC = T + 2 / n
    WAIC = T + np.mean([
        np.mean([np.log(p(X[i], A[k], B[k]))**2 for k in range(K)]) -
        (np.mean([np.log(p(X[i], A[k], B[k])) for k in range(K)]))**2
        for i in range(n)
    ])
    ISCV = np.mean([
        np.log(np.mean([1 / p(X[i], A[k], B[k]) for k in range(K)]))
        for i in range(n)
    ])
    return G, AIC, WAIC, ISCV


def plot(a=0.5, b=2, s=1, N=100, K=100, burn=20, ex=100, name='test'):
    G, AIC, WAIC, ISCV = [], [], [], []
    for _ in range(ex):
        g, aic, waic, iscv = main(a=a, b=b, s=s, n=N, K=K, burn=burn)
        G.append(g)
        AIC.append(aic)
        WAIC.append(waic)
        ISCV.append(iscv)
    plt.boxplot((G, AIC, WAIC, ISCV), labels=['G', 'AIC', 'WAIC', 'ISCV'])
    if a == 0:
        plt.title('N(0, {})'.format(s))
    else:
        plt.title('{}N(0, {}) + {}N({}, {})'.format(1 - a, s, a, b, s))
    now = dt.now().strftime("%Y%m%d%H%M%S")
    plt.savefig('image/WAIC/{}_{}.png'.format(name, now))
    plt.cla()


plot(a=0.5, b=2, s=1, name='regular&realizable')
plot(a=0.5, b=2, s=0.8, name='regular&unrealizable')
plot(a=0, b=0, s=1, name='nonregular&realizable')
plot(a=0, b=0, s=0.8, name='nonregular&unrealizable')
plot(a=0.5, b=0.5, s=0.95, name='delicate')
plot(a=0.01, b=2, s=1, name='unbalanced')
