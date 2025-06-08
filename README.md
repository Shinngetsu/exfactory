# exfactory
Pythonの計算式でファクトリを構築できます。

## 特徴
- 計算式をもとにファクトリを構築
- product()にファクトリとコンテキストを渡して生成
- ほとんどのデータクラスに対応できます

## 使用例
オブジェクト生成
```python
import random
from exfactory import product, con, wrap, context

# クラス定義
class A:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f'A({self.value})'

# 前提オブジェクト
fA = wrap(A)                　# Aのファクトリ化
frand = wrap(random.Random()) # ランダムのファクトリ化
ctx = context()               # コンテキスト
# ファクトリ作成
factory1 = con(A, 10)
factory2 = fA(frand.randint(10, 20))
factory3 = fA(ctx['value'])

# 生成
print(product(factory1, None)) # A(10)
print(product(factory2, None)) # A(10~20)
print(product(factory3, {'value':30})) # A(30)
```

## 処理能力
極端に遅いことはありませんが、ありえないほど速いわけではありません。
…と言われて期待するほどには早くはないものの、前文を否定するほど致命的に遅いわけでもありません。

## 必要条件
- Python 3.13~
- MathObj