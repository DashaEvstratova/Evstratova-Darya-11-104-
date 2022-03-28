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
                    node.val = val
                    break

    def __delitem__(self, key):
        pass

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
