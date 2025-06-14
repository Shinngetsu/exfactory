from exfactory import *

def test_product_Generate_ReturnCollectValues():
    "Generateが正しいイテレータ―を生成するか"
    i = Var()
    f = Generate(i,
        (i, [1, 2, 3, 4, 5]))
    itr = [1, 2, 3, 4, 5]
    assert all(i == j for i, j in zip(product(f), itr))

def test_product_GenerateWithPred_ReturnCollectValues():
    "条件付きGenerateが正しいイテレータを生成するか"
    i = Var()
    f = Generate(i,
        (i, [1, 2, 3, 4, 5], i % 2 == 0))
    itr = [j for j in [1, 2, 3, 4, 5] if j % 2 == 0]
    assert all(i == j for i, j in zip(product(f), itr))

def test_product_GenerateNestRoop_ReturnCollectValues():
    "ネストされたループのGenerateが正しいイテレータを生成するか"
    i = Var()
    j = Var()
    frange = Wrap(range)
    f = Generate(i * j,
        (i, frange(1, 10)),
        (j, frange(1, 10)))
    itr = [i * j
        for i in range(1, 10)
        for j in range(1, 10)]
    assert all(i == j for i, j in zip(product(f), itr))

def test_product_GenerateMultiStore_ReturnCollectValues():
    "ストアがうまく機能するか検証"
    i = Var()
    j = Var()
    frange = Wrap(range)
    fzip = Wrap(zip)
    f = Generate(i * j,
        ((i, j), fzip(frange(1, 10), frange(1, 10))))
    itr = [i * j
        for i in zip(range(1, 10), range(1, 10))]
    assert all(i == j for i, j in zip(product(f), itr))

def test_product_GenerateMultiStore_ReturnCollectValues():
    "スターストアがうまく機能するか検証"
    i = Var()
    j = Var()
    fsum = Wrap(sum)
    frange = Wrap(range)
    fzip = Wrap(zip)
    f = Generate(i * fsum(j),
        ((i, Star(j)), 
            fzip(frange(1, 10),
                 frange(1, 10),
                 frange(1, 10))))
    itr = [i * sum(j)
        for i, *j in 
            zip(range(1, 10),
                range(1, 10),
                range(1, 10))]
    assert all(i == j for i, j in zip(product(f), itr))

def test_product_GenerateMultiStore2_ReturnCollectValues():
    "スターストアがうまく機能するか検証(スター後に)"
    i = Var()
    j = Var()
    k = Var()
    fsum = Wrap(sum)
    frange = Wrap(range)
    fzip = Wrap(zip)
    f = Generate(i * fsum(j) - k,
        ((i, Star(j), k), 
            fzip(frange(1, 10),
                 frange(1, 10),
                 frange(1, 10),
                 frange(1, 10))))
    itr = [i * sum(j) - k
        for i, *j, k in 
            zip(range(1, 10),
                range(1, 10),
                range(1, 10),
                range(1, 10))]
    assert all(i == j for i, j in zip(product(f), itr))
