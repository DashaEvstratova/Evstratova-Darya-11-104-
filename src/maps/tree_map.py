'''
do the tree_map
'''

from dataclasses import dataclass
from src.maps.base_map import BaseMap
@dataclass
class Node:
    '''
    do the node
    '''
    key: str
    val: int
    left = None
    right = None

class TreeMap(BaseMap):
    '''
    do the tree_map
    '''
    def __init__(self):
        self.root = None
        self.size = 0

    def __setitem__(self, key, val):
        def inner_setitem(node):
            if node is None:
                return Node(key, val)
            if key == node.key:
                node.val = val
            elif key < node.key:
                node.left = inner_setitem(node.left)
            else:
                node.right = inner_setitem(node.right)
            return node

        self.root = inner_setitem(self.root)
    @staticmethod
    def find_min_node(node):
        '''
        find min
        '''
        if node.left is not None:
            return TreeMap.find_min_node(node.left)
        return node

    def __delitem__(self, key):
        '''
        recursive deletion
        '''
        def inner_delitem(node, key):
            if node is None:
                raise KeyError
            if key < node.key:
                node.left = inner_delitem(node.left, key)
                return node
            if key > node.key:
                result = inner_delitem(node.right, key)
                node.right = result
                return node
            if node.left is None and node.right is None:
                return None
            if node.left is not None and node.right is None:
                return node.left
            if node.left is None and node.right is not None:
                return node.right
            min_node = TreeMap.find_min_node(node.right)
            node.key = min_node.key
            node.val = min_node.val
            node.right = inner_delitem(node.right, min_node.key)
            return node
        self.root = inner_delitem(self.root, key)

    def __getitem__(self, key):
        if self.root is None:
            return False
        node = self.root
        while node:
            if key < node.key:
                if node.left is None:
                    return False
                node = node.left
            elif key > node.key:
                if node.right is None:
                    return False
                node = node.right
            else:
                return node.val

    def __iter__(self):
        def iter_node(node):
            if node is not None:
                yield node.key, node.val
                yield from iter_node(node.left)
                yield from iter_node(node.right)
        yield from iter_node(self.root)

    def __len__(self):
        return self.size
