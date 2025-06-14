
from .factory import Factory, PRODUCTABLE, product, OBJ, CC

class Var(Factory[OBJ, CC]):
    """変数ファクトリ"""
    def __init__(self, idx=None, valid=None):
        self.__valid = valid
        self.__id = id(self) if idx is None else idx
    def _Factory__product(self, cc, vc):
        value = vc[self.__id]
        assert self.__valid is None or self.__valid(value)
        return value

def var_idx(v:Var) -> int:
    """変数のIDを取得"""
    return v._Var__id


#もっといい方法あるよなあ…

class Statement:
    def process(self, cc, vc):
        pass
class Assign(Statement):
    def __init__(self, var, val):
        self.__var = var
        self.__val = val
    def process(self, cc, vc):
        return cc, vc | {
            var_idx(self.__var): product(self.__val, cc, vc)}

class Do(Factory[OBJ, CC]):
    def __init__(self,
            *stmt:Statement):
        self.__stmt = stmt
    def _Factory__product(self, cc, vc):
        for s in self.__stmt:
            cc, vc = s.process(cc, vc)
        # 式を評価
        return product(self.__ex, cc, vc)


