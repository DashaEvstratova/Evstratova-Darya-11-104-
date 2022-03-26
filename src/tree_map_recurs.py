'''
do the tree_map
'''

from dataclasses import dataclass
@dataclass
class Node:
    '''
    do the node
    '''
    key: str
    value: int
    left = None
    right = None

class TreeMapRecurs:
    '''
    do the tree_map
    '''
    def __init__(self):
        self.root = None
    def __setitem__(self, key, value):
        '''
        recursive addition
        '''
        def inner_setitem(node):
            if node is None:
                return Node(key, value)
            if key == node.key:
                node.value = value
            elif key < node.key:
                node.left = inner_setitem(node.left)
            else:
                node.right = inner_setitem(node.right)
            return node
        self.root = inner_setitem(self.root)

    def __getitem__(self, key):
        '''
        recursive finding
        '''
        def inner_getitem(node):
            if node is None:
                raise KeyError
            if key == node.key:
                return node.value
            if key < node.key:
                return inner_getitem(node.left)
            return inner_getitem(node.right)
        return inner_getitem(self.root)

    @staticmethod
    def find_min_node(node):
        '''
        find min
        '''
        if node.left is not None:
            return TreeMapRecurs.find_min_node(node.left)
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
            min_node = TreeMapRecurs.find_min_node(node.right)
            node.key = min_node.key
            node.value = min_node.value
            node.right = inner_delitem(node.right, min_node.key)
            return node
        self.root = inner_delitem(self.root, key)
