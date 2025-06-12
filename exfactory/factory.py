# coding: utf-8

from mathobj import MathObj
import abc, operator as op
from typing import Any

# ファクトリの抽象クラス
class Factory[OBJ, CC](MathObj, abc.ABC):
    """ファクトリの抽象クラス"""
    @abc.abstractmethod
    def _Factory__product(self, cc:CC, vc:dict) -> OBJ: pass
    def _unary(self, uf): return Construct(uf, self)
    def _binary(self, bf, b): return Construct(bf, self, b)
    def _rbinary(self, bf, a): return Construct(bf, a, self)
    def __getattr__(self, k): return Construct(getattr, self, k)
    def __getitem__(self, k): return Construct(op.getitem, self, k)
    def __call__(self, *a, **ka): return Construct(self, *a, **ka)

# ファクトリからインスタンスを生成する関数
def product[OBJ, CC](item:Factory[OBJ, CC]|OBJ, cc:CC=None, vc:dict=None) -> OBJ:
    """ファクトリからインスタンスを生成"""
    if vc is None: vc = {}
    if isinstance(item, Factory):
        return item._Factory__product(cc)
    return item

# Factoryのサブクラス
class Construct[OBJ, CC](Factory[OBJ, CC]):
    """コンストラクタと引数の組み合わせから生成するファクトリ"""
    def __init__(self, c, *a, **ka):
        self.__c = c
        self.__a = a
        self.__ka = ka
    def _Factory__product(self, cc, vc):
        return product(self.__c, cc, vc)(
            *[product(i, cc, vc) for i in self.__a],
            **{k:product(i, cc, vc) for k, i in self.__ka.items()})

class Wrap[OBJ](Factory[OBJ, Any]):
    """オブジェクトをファクトリに変換"""
    def __init__(self, o:OBJ):
        self.__o = o
    def _Factory__product(self, cc, vc):
        return self.__o

class Context[CC](Factory[CC, CC]):
    """コンテキストファクトリ"""
    def _Factory__product(self, cc, vc): return cc

class Constructs[CONT, OBJ, CC](Factory[CONT, CC]):
    """指定されたコンテナのグリッド構造を生成するファクトリ"""
    def __init__(self, c:type[CONT],
            cnts:tuple[Factory[int, CC], ...],
            obj:Factory[OBJ, CC]|OBJ):
        self.__c = c
        self.__cnts = cnts
        self.__obj = obj
    def _Factory__product(self, cc):
        def iterate(itr, *itrs):
            if itrs:
                return product(self.__c, cc, vc)(
                    iterate(*itrs)
                    for _ in range(product(itr, cc, vc)))
            else:
                return product(self.__c, cc, vc)(
                    product(self.__obj, cc, vc)
                    for _ in range(product(itr, cc, vc)))
        return iterate(*self.__cnts)

class Once[OBJ, CC](Factory[OBJ, CC]):
    """一度だけ生成されるファクトリ"""
    def __init__(self, f:Factory[OBJ, CC]|OBJ):
        self.__f = f
        self.__o = None
    def _Factory__product(self, cc):
        if self.__o is None:
            self.__o = product(self.__f, cc, vc)
        return self.__o
