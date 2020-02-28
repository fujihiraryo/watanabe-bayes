# 渡辺澄夫「ベイズ統計の理論と方法」についての実装

| ファイル                                                                                        | 内容                                           | 参考                                                                   |
| ----------------------------------------------------------------------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------- |
| [likelihood.py](https://github.com/fujihiraryo/watanabe-bayes/blob/master/python/likelihood.py) | 混合正規分布の尤度関数                         | p.18                                                                   |
| [gibbs.py](https://github.com/fujihiraryo/watanabe-bayes/blob/master/python/gibbs.py)           | 混合正規分布の事後分布からのギブスサンプリング | 章末問題 5.1                                                           |
| [mean_field.py](https://github.com/fujihiraryo/watanabe-bayes/blob/master/python/mean_field.py) | 混合正規分布を用いた変分ベイズ                 | 章末問題 5.3                                                           |
| [metropolis.py](https://github.com/fujihiraryo/watanabe-bayes/blob/master/python/metropolis.py) | メトロポリス法                                 | p.137                                                                  |
| [hybrid.py](https://github.com/fujihiraryo/watanabe-bayes/blob/master/python/hybrid.py)         | ハイブリッド･モンテカルロ法                    | p.140                                                                  |
| [langevin.py](https://github.com/fujihiraryo/watanabe-bayes/blob/master/python/langevin.py)     | ランジュバン･モンテカルロ法                    | p.143                                                                  |
| [mala.py](https://github.com/fujihiraryo/watanabe-bayes/blob/master/python/mala.py)             | 棄却ステップ付きランジュバン･モンテカルロ法    | https://ktrmnm.github.io/blog/2016/08/25/201608-lmc/201608_mala.pdf    |
| [WAIC.py](https://github.com/fujihiraryo/watanabe-bayes/blob/master/python/WAIC.py)             | 混合正規分布で汎化損失とその推定量の計算       | http://watanabe-www.math.dis.titech.ac.jp/users/swatanab/waic2011.html |
| [WBIC.py](https://github.com/fujihiraryo/watanabe-bayes/blob/master/python/WBIC.py)             | 混合正規分布で自由エネルギーとその推定量の計算 | http://watanabe-www.math.dis.titech.ac.jp/users/swatanab/wbic2012.html |
