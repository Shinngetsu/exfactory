# coding: utf-8
"""
mathobj.py - 数学的なオブジェクトの抽象クラス
========================================
このモジュールで定義される`MathObj`は、
全ての演算子に対する一般的な処理を提供できる、
- _MathObj__unary : 単項演算
- _MathObj__binary : 二項演算
- _MathObj__rbinary : 逆順の二項演算
の抽象メソッドを持ちます。

HaskellにおけるFunctorのように
- 所持しているリストアイテムに対して演算を適用
- 遅延評価をする計算構造の構築
の土台として利用できます。


リポジトリに公開してるmathobjはプライベートを使ってないので、
ここではプライベート版を定義しています。
"""

import operator as op, abc
import typing, collections.abc as ctyping

# 演算子の定義
unaries = op.pos, op.neg, op.inv, op.abs
"""単項演算子"""
binaries = (
    op.add, op.sub, op.mul, op.truediv, op.floordiv, op.mod,
    op.pow, op.matmul,
    op.and_, op.or_, op.xor, op.rshift, op.lshift,
    op.lt, op.gt, op.le, op.ge, op.eq, op.ne)
"""二項演算子"""
rjoins = op.pow,
"""右結合で評価される二項演算子"""

# 型定義
OBJ = typing.TypeVar('OBJ')
UNARY = ctyping.Callable[[OBJ], OBJ]
"""単項演算子の型"""
BINARY = ctyping.Callable[[OBJ, OBJ], OBJ]
"""二項演算子の型"""

def defop(local, o):
    """演算子を定義する"""
    name = o.__name__.replace('_', '')
    if o in unaries:
        local[f'__{name}__'] = lambda self: self._MathObj__unary(o)
    else:
        local[f'__{name}__'] = lambda self, b: self._MathObj__binary(o, b)
        local[f'__r{name}__'] = lambda self, a: self._MathObj__rbinary(o, a)
def defops(local, ops):
    """複数の演算子を定義する"""
    # このループをクラスでやってしまうと、
    # oがクラスの属性として定義されてしまう。
    for o in ops: defop(local, o)

class MathObj(abc.ABC):
    """数学的なオブジェクトの抽象クラス"""
    @abc.abstractmethod
    def _MathObj__unary(self, uf:UNARY) -> typing.Any:
        """単項演算子を適用する"""
    @abc.abstractmethod
    def _MathObj__binary(self, bf:BINARY, b) -> typing.Any:
        """二項演算子を適用する"""
    @abc.abstractmethod
    def _MathObj__rbinary(self, bf:BINARY, a) -> typing.Any:
        """逆順の二項演算子を適用する"""
    
    defops(locals(), unaries)
    defops(locals(), binaries)

    # __eq__を更新してしまうので__hash__を定義しなおす
    def __hash__(self): return id(self)

# 演算子メソッドがラムダであることに注意
