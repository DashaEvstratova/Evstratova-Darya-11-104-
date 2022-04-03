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
        if self.root is None:
            self.root = Node(key, val)
            self.size+=1
        else:
            node = self.root
            while (not node.left) and (not node.right):
                if key < node.key:
                    if node.left is None:
                        node.left = Node(key, val)
                        self.size += 1
                        break
                    node = node.left
                elif key > node.key:
                    if node.right is None:
                        node.right = Node(key, val)
                        self.size += 1
                        break
                    node = node.right
                elif key == node.key:
                    node.val +=1
                    break

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
                yield node.key, node.value
                yield from iter_node(node.left)
                yield from iter_node(node.right)
        yield from iter_node(self.root)
    def __len__(self):
        return self.size
