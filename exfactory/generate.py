
from .factory import Factory, PRODUCTABLE, product, OBJ, CC
from typing import Any
import collections.abc as ctyping

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
    """複数のジェネレータを組み合わせて要素を生成するファクトリ"""
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
            """ジェネレータを再帰的に呼び出して要素を生成"""
            if generators:
                store, iter, pred = generators[0]
                for value in product(iter, cc, vc):
                    ivc = vc | store_var(store, iter)
                    if all(product(p, cc, ivc) for p in pred):
                        return generate(elt, ivc, *generators[1:])
            else:
                yield product(elt, cc, vc)
        return generate(self.__elt, vc, *self.__generators)
