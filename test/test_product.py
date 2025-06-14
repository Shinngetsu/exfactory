from exfactory import *

def test_product_NotFactory_Return():
    "productはファクトリ以外であればそのまま返す"
    tgt = object()
    assert product(tgt) is tgt, \
        "ファクトリ以外であればそのまま返す"
