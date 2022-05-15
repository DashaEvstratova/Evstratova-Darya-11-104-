'''pytests'''
import pytest
from src.maps.tree_map import TreeMap

def test_tree_map():
    '''test of add'''
    tree_mapa = TreeMap()
    tree_mapa["sd"] = 42
    assert tree_mapa["sd"] == 42

def test_size():
    '''test of len'''
    tree_mapa = TreeMap()
    for i in range(7):
        tree_mapa[i] = i
    leng1 = len(tree_mapa)
    tree_mapa[7] = 7
    leng2 = len(tree_mapa)
    assert leng1 < leng2

def test_delkey():
    '''test of del'''
    tree_mapa = TreeMap()
    tree_mapa["sd"] = 42
    del tree_mapa["sd"]
    with pytest.raises(KeyError):
        tree_mapa.__getitem__("sd")
