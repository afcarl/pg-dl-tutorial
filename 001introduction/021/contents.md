# モデルの定義

それでは次に学習対象のモデルを定義します。

今回は3層からなるニューラルネットワークの例をあげます。

```
import chainer
from chainer import links as L
from chainer import functions as F

...

class MLP(chainer.Chain):

    def __init__(self, n_units, n_out):
        super(MLP, self).__init__(
            # the size of the inputs to each layer will be inferred
            l1=L.Linear(None, n_units),  # n_in -> n_units
            l2=L.Linear(None, n_units), # n_units -> n_units
            l3=L.Linear(None, n_out)  # n_units -> n_out
        )

    def __call__(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        return self.l3(h2)
```

ニューラルネットワークのモデルを定義するオブジェクトは `chainer.Chain`（以降 `Chain` ）を継承します。
`Chain` を継承することで，このモデルを保存したり読み込んだりすることができます。

モデルでは初期化時にモデル内で利用するパラメータ付き関数であるLinkを登録します。

上記の例では `Linear` である `l1`, `l2`, `l3` を登録しています。
`Linear` は線形変換であり，初期化引数として入力次元数と出力次元数をうけとります。
`Linear` の入力次元数に `None` を指定した時は，それが最初に呼び出された時，次元数を引数から推定してくれます。

`Chain` においてLinkの登録は例のように `__init__` の中で定義することもできますし，次のように `add_link(name, link)` で登録することもできます。

```
class MLP(chainer.Chain):

    def __init__(self, n_units, n_out):
        super(MLP, self).__init__()
        self.add_link("l1", L.Linear(None, n_units))
        self.add_link("l2", L.Linear(None, n_units))
        self.add_link("l3", L.Linear(None, n_out))
```

例えば，ループを回して多くのLinkを登録したい場合は `add_link` で登録するのが便利です。

```
for i in range(10):
    self.add_link("l{}".format(i), L.Linear(None, n_units))
```

初期化時に登録されたLinkはあとで `self.l1` のようにオブジェクトの属性として参照できます。

次に，モデルを使って入力をどのように変換して出力を得るのかを定義します。
学習時に出力から入力へ逆方向に勾配を伝播させる誤差逆伝搬法との比較で，この入力から出力への計算を順計算（forward-computation）とよびます。

順計算は，多くの場合 `__call__` メソッドで定義します。
さきほど登録した `l1`, `l2`, `l3` を使って入力 `x` から3回線形変換と2回ReLUを適用して結果を返す順計算を定義してみましょう。

```
    def __call__(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        return self.l3(h2)
```

最後， `self.l3(h2)` には `F.relu` を適用していないことに注意してください。
softmaxを使う際によくある間違いとして，最後の出力にもReLUを適用してしまうというのがあります。
softmaxの定義域は負を含む実数ですので，その入力を非負に制約すると，想定しない制約を課して学習することになります。

順計算は `__call__` で定義する必要は必ずしもありません。
また，順計算は複数用意してもよいですし，その場で新しく作ってもよいです。
例えば，2層目の途中の中間結果を返すメソッドを次のように定義し使うこともできます。

```
    def forward_with_two_layers(self, x):
        h1 = F.relu(self.l1(x))
        return self.l2(h1)
```

順計算を `__call__` で定義したおかげで，この `MLP` は， `()` で順計算を呼び出すことができます。

このように作ったMLPを分類器として使うには `L.Classifier` を使ってモデルを作ります。
`Classifier` はデフォルトでは分類器softmax，学習時の損失関数はsoftmaxクロスエントロピー損失を使います。
`Classifier` が引数としてとるモデルは `__call__()` で順計算が定義されていることを想定しています。

```
model = L.Classifier(MLP(784, 10))
```

## メモ: Define-by-Run

Chainerの特徴は"Define-by-Run"，つまり順に実行しながらネットワークを定義していきます。
この例では関数呼び出し `__call__` の中でネットワークを順に作っています。

## 課題

`Chain` を継承したオブジェクトに登録されているパラメータ付関数は `namedlinks()` で呼び出すことができます。
例えば上の例の場合 `l1`, `l2`, `l3` が呼び出されます。
上の例を4層のニューラルネットワークに変更し`namedlinks()`の要素を表示してください。

