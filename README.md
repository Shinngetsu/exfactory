# exfactory
Pythonの計算式でファクトリを構築できます。

## 特徴
- 計算式をもとにファクトリを構築
- product()にファクトリとコンテキストを渡して生成
- ほとんどのデータクラスに対応できます
- ピクラブル(多分)
  - lambdaやジェネレータ、クロージャ、ファイルコンテキストを要素として含むファクトリはありません。
  - 設定に使うオブジェクトもすべてピクラブルなら、ファクトリもピクル可能なはずです。

## インストール
```bash
pip install git+https://github.com/Shinngetsu/exfactory.git
```

## 使用例
オブジェクト生成
```python
import random
from exfactory import product, Construct, Wrap, Context

# クラス定義
class A:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f'A({self.value})'

# 前提オブジェクト
fA = Wrap(A)                　# Aのファクトリ化
frand = Wrap(random.Random()) # ランダムのファクトリ化
ctx = Context()               # コンテキスト
# ファクトリ作成
factory1 = Construct(A, 10)
factory2 = fA(frand.randint(10, 20))
factory3 = fA(ctx['value'])

# 生成
print(product(factory1)) # A(10)
print(product(factory2)) # A(10~20)
print(product(factory3, {'value':30})) # A(30)
```

## 処理能力
極端に遅いことはありませんが、ありえないほど速いわけではありません。
…と言われて期待するほどには早くはないものの、前文を否定できるほど致命的に遅いことはありません。

## まだできてない
### 生成対象をもとにした要素や型の推論
- IDLE等で動作する時の表示であれば作れなくもないですが、VSCodeの静的な型推論には表示されません。
### 構成チェック・最適化
- 生成エラーはproduct時に発生します。
- 出力時の副作用を起こさずに生成エラーの検証を行う機能はありません。
  - Visitorパターンを使って処理構造の検証や最適化ができるようにしたい。
### 生成構造の可視化
- ファクトリの構造を文字列で表現する機能はありません。
### マルチスレッド、マルチプロセスでの動作確認
- 多分ピクラブルなのでキューには通せるはず…
### 分かりやすいエラー
- product時のエラーは、大抵が非常に奥まった場所から送出され、何がどう悪いのか分かりづらいことが多いです。
- これは優先度の高い課題です。

## やめてね
- 自己参照を持たせる
  - 自己参照を持つファクトリはproduct時に再帰処理の無限ループを引き起こします。
  - 副作用で処理が停止することが分かっている場合でも、コードからその判断をするのは難しいはずです。

## 必要条件
- Python 3.13~
- https://github.com/Shinngetsu/mathobj.git 0.1.0