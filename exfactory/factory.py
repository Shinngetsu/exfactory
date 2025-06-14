# coding: utf-8

from .mathobj import MathObj
import abc, operator as op
import typing, collections.abc as ctyping
from typing import Any


OBJ = typing.TypeVar('OBJ')
"ファクトリの生成対象"
CC = typing.TypeVar('CC', bound=Any)
"生成時コンテキストの型"

# ファクトリの抽象クラス
class Factory(typing.Generic[OBJ, CC], MathObj, abc.ABC):
    """ファクトリの抽象クラス"""
    @abc.abstractmethod
    def _Factory__product(self, cc:CC, vc:dict) -> OBJ: pass
    def _MathObj__unary(self, uf) -> typing.Self:
        """単項演算子を適用する"""
        return Construct(uf, self)
    def _MathObj__binary(self, bf, b) -> typing.Self:
        """二項演算子を適用する"""
        return Construct(bf, self, b)
    def _MathObj__rbinary(self, bf, a) -> typing.Self:
        """逆順の二項演算子を適用する"""
        return Construct(bf, a, self)
    def __getattr__(self, k): return Construct(getattr, self, k)
    def __getitem__(self, k): return Construct(op.getitem, self, k)
    def __call__(self, *a, **ka): return Construct(self, *a, **ka)


PRODUCTABLE = Factory[OBJ, CC] | OBJ
# ファクトリからインスタンスを生成する関数
def product(
        item:PRODUCTABLE,
        cc:CC=None, vc:dict=None) -> OBJ:
    """ファクトリからインスタンスを生成"""
    if vc is None: vc = {}
    if isinstance(item, Factory):
        return item._Factory__product(cc, vc)
    return item


# Factoryのサブクラス
class Construct(Factory[OBJ, CC]):
    """コンストラクタと引数の組み合わせから生成するファクトリ"""
    def __init__(self, c, *a, **ka):
        self.__c = c
        self.__a = a
        self.__ka = ka
    def _Factory__product(self, cc, vc):
        return product(self.__c, cc, vc)(
            *[product(i, cc, vc) for i in self.__a],
            **{k:product(i, cc, vc) for k, i in self.__ka.items()})

class Wrap(Factory[OBJ, Any]):
    """オブジェクトをファクトリに変換"""
    def __init__(self, o:OBJ):
        self.__o = o
    def _Factory__product(self, cc, vc):
        return self.__o

class Context(Factory[CC, CC]):
    """コンテキストファクトリ"""
    def _Factory__product(self, cc, vc): return cc

import threading
class Once(Factory[OBJ, CC]):
    """一度だけ生成されるファクトリ"""
    def __init__(self, f:Factory[OBJ, CC]|OBJ):
        self.__f = f
        self.__o = None
        self.__lock = threading.Lock()
    def _Factory__product(self, cc, vc):
        self.__lock.acquire()
        try:
            if self.__o is None:
                self.__o = product(self.__f, cc, vc)
        finally:
            self.__lock.release()
        return self.__o
