from exfactory import *

def test_product_NotFactory_Return():
    tgt = object()
    assert product(tgt) is tgt, \
        "productはファクトリ以外であればそのまま返す"

def test_product_WrapObj_ReturnWrappedObj():
    tgt = object()
    assert product(Wrap(tgt)) is tgt, \
        "Wrapはラップした対象を返す"

