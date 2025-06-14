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
        return item._Factory__product(cc)
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

class Constructs[CONT, OBJ, CC](Factory[CONT, CC]):
    """指定されたコンテナのグリッド構造を生成するファクトリ"""
    def __init__(self, c:type[CONT],
            cnts:tuple[Factory[int, CC], ...],
            obj:Factory[OBJ, CC]|OBJ):
        self.__c = c
        self.__cnts = cnts
        self.__obj = obj
    def _Factory__product(self, cc, vc):
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

class Var(Factory[OBJ, CC]):
    """変数ファクトリ"""
    def __init__(self, idx=None, valid=None):
        self.__valid = valid
        self.__id = id(self) if idx is None else idx
    def _Factory__product(self, cc, vc):
        value = vc[self.__id]
        assert self.__valid is None or self.__valid(value)
        return value

class Star:
    """可変長引数を受け取るシンボル
    Generateのストアに利用される"""
    def __init__(self, var:Var):
        self.var = var

STORE = Var | Star | tuple[Any, ...]
PREDICATE = PRODUCTABLE[bool, CC]

def store_var(
        store:STORE,
        src:OBJ| tuple[OBJ, ...]
    ) -> dict[Var, OBJ]:
    """ストアの内容を辞書に変換"""
    if isinstance(store, Var):
        return {store: src}
    elif isinstance(store, Star):
        store = store.var
        return {store: [src]}
    else:
        res = {}
        star_pos = 0
        for var, val in zip(store, src):
            if isinstance(var, Star): break
            res |= store_var(var, val)
            star_pos += 1
        else:
            # Starが見つからなかった場合、ストアの長さとソースの長さを確認
            if len(store) != len(src):
                raise ValueError(
                    f"Store length {len(store)} does not match"
                    f" source length {len(src)}")
        if star_pos < len(store):
            # Star以降の要素にStarが含まれている場合はエラー
            if any(isinstance(i, Star) for i in store[star_pos+1:]):
                raise ValueError(
                    "Star must be only element in the same-level store tuple")
            # Starの位置を見つけたら、残りの要素を格納
            tails = len(store) - star_pos - 1
            # Starの位置以降の要素がソースに十分な長さがあるか確認
            if tails > len(src) - star_pos:
                raise ValueError(
                    f"Not enough elements in source to fill store: "
                    f"store length {len(store)}, source length {len(src)}")
            res[store[star_pos].var] = src[star_pos:-tails]
            # Star以降の要素を格納
            if tails > 0:
                res |= store_var(store[-tails:], src[-tails:])
        return res


class Generate(Factory[ctyping.Iterator[OBJ], CC]):
    def __init__(self,
            elt:PRODUCTABLE,
            *generators:
                tuple[
                    STORE,
                    PRODUCTABLE[ctyping.Iterator[OBJ], CC]]
                | tuple[
                    STORE,
                    PRODUCTABLE[ctyping.Iterator[OBJ], CC],
                    tuple[PREDICATE, ...]]):
        self.__elt = elt
        self.__generators = generators
    def _Factory__product(self, cc, vc):
        def generate(elt, vc, *generators):
            """生成器を再帰的に呼び出して要素を生成"""
            if generators:
                store, iter, pred = generators[0]
                for value in product(iter, cc, vc):
                    ivc = vc | store_var(store, iter)
                    if all(product(p, cc, ivc) for p in pred):
                        return generate(elt, ivc, *generators[1:])
            else:
                yield product(elt, cc, vc)
        return generate(self.__elt, vc, *self.__generators)
