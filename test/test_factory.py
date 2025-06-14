from exfactory import *

def test_product_Wrap_ReturnWrappedObj():
    "Wrapはラップした対象を生成"
    tgt = object()
    assert product(Wrap(tgt)) is tgt, \
        "Wrapはラップした対象を生成"

def test_product_Context_ReturnContextObj():
    "Contextは生成時にコンテキストとして渡されたオブジェクトを生成"
    ctx = object()
    assert product(Context(), ctx) is ctx, \
        "Contextは生成時にコンテキストとして渡されたオブジェクトを生成"

def test_product_Construct_ReturnObj():
    "Constructは指定したコンストラクタに各種引数を渡して生成"
    class A:
        def __init__(self, a, b):
            self.a = a
            self.b = b
        def __eq__(self, b):
            return (type(self) is type(b) and
                    self.a == b.a and
                    self.b == b.b)
    f = Construct(A, 10, 20)
    obj = A(10, 20)
    assert product(f) == obj, \
        "Constructは指定したコンストラクタに各種引数を渡して生成"

def test_product_Expression_ReturnObj():
    "計算式によって生成されるファクトリが正しいオブジェクトを生成するか"
    f = Context() *3 +2
    ctx = 10
    assert product(f, ctx) == ctx *3 +2, \
        "計算が合いません"
