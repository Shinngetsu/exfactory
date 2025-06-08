from mathobj import MathObj
import abc, operator as op
from typing import Any

class Factory[OBJ, CC](MathObj, abc.ABC):
    """ファクトリの抽象クラス"""
    @abc.abstractmethod
    def _Factory__product(self, cc:CC) -> OBJ: pass
    def _unary(self, uf): return Construct(uf, self)
    def _binary(self, bf, b): return Construct(bf, self, b)
    def _rbinary(self, bf, a): return Construct(bf, a, self)
    def __getattr__(self, k): return Construct(getattr, self, k)
    def __getitem__(self, k): return Construct(op.getitem, self, k)
    def __call__(self, *a, **ka): return Construct(self, *a, **ka)

def product[OBJ, CC](item:Factory[OBJ, CC]|OBJ, cc:CC=None) -> OBJ:
    """ファクトリからインスタンスを生成"""
    if isinstance(item, Factory): return item._Factory__product(cc)
    return item

class Construct[OBJ, CC](Factory[OBJ, CC]):
    """コンストラクタと引数の組み合わせ"""
    def __init__(self, c, *a, **ka): self.__c, self.__a, self.__ka = c, a, ka
    def _Factory__product(self, cc): return product(self.__c, cc)(
        *[product(i, cc) for i in self.__a],
        **{k:product(i, cc) for k, i in self.__ka.items()})
class Wrap[OBJ](Factory[OBJ, Any]):
    """オブジェクトをファクトリに変換"""
    def __init__(self, o:OBJ): self.__o = o
    def _Factory__product(self, cc): return self.__o
class Context[CC](Factory[CC, CC]):
    """コンテキスト"""
    def _Factory__product(self, cc): return cc
class Constructs[CONT, OBJ, CC](Factory[CONT, CC]):
    """指定されたコンテナのグリッド構造"""
    def __init__(self, c:type[CONT],
            cnts:tuple[Factory[int, CC], ...],
            obj:Factory[OBJ, CC]|OBJ):
        self.__c, self.__cnts, self.__obj = c, cnts, obj
    def _Factory__product(self, cc):
        def iterate(itr, *itrs):
            if itrs: return product(self.__c, cc)(
                iterate(*itrs) for _ in range(product(itr, cc)))
            else: return product(self.__c, cc)(
                product(self.__obj, cc) for _ in range(product(itr, cc)))
        return iterate(*self.__cnts)

