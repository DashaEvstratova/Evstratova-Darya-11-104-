class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class TreeMap:
    def __init__(self):
        self.root = None

    def __setitem__(self, key, value):
        if self.root == None:
            self.root = Node(key, value)
        else:
            a = self.root
            while (not a.left) and (not a.right):
                if key<a.key:
                    if a.left is None:
                        a.left = Node(key, value)
                        break
                    a = a.left
                elif key>a.key:
                    if a.right is None:
                        a.right = Node(key, value)
                        break
                    a= a.right
                elif key == a.key:
                    a.value = value
                    break
    def __delitem__(self, key):
        pass

    def __getitem__(self, key):
        if self.root == None:
            return False
        else:
            a = self.root
            while a:
                if key<a.key:
                    if a.left is None:
                        return False
                    else:
                        a = a.left
                elif key>a.key:
                    if a.right is None:
                        return False
                    else:
                        a = a.right
                else:
                    return a.value


