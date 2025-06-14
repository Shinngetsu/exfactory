from exfactory import *

def test_product_Generate_ReturnItr():
    "Generateが正しいイテレータ―を生成するか"
    i = Var()
    f = Generate(i,
        (i, [1, 2, 3, 4, 5]))
    itr = [1, 2, 3, 4, 5]
    assert all(i == j for i, j in zip(product(f), itr))
