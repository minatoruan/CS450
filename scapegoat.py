from math import log, ceil, floor

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.p = None

    def __repr__(self):
        return str(self.key)  

class Tree():
    def __init__(self, alpha, key):
        self.__alpha = alpha
        self.__root = None
        self.__size = 1
        self.__maxsize = 0
        self.__insertKey(key)

    def __sizeof(self, node):
        return 1 + self.__sizeof(node.left) + self.__sizeof(node.right) if node else 0

    def __maxHeight(self, size):
        if size == 0: return 0
        return int(log(size, 1/self.__alpha))
    
    def __insertKey(self, key):
        if (self.__root == None): # Tree is empty, root is Node
            self.__root = Node(key)
            return 0, self.__root

        h = 0
        x = self.__root
        while (x and x.key != key):
            y = x
            x = x.key > key and x.left or x.right
            h += 1

        if (x and x.key == key): return -1, None # duplicate

        node = Node(key)
        node.p = y
        if (y.key > key): y.left = node
        else: y.right = node
        
        return h, node

    def __transplant(self, u, v):
        if not u.p: self.__root = v
        elif u == u.p.left: u.p.left = v
        else: u.p.right = v
        if v: v.p = u.p

    def __minimum(self, node):
        while node.left: node = node.left
        return node

    def __deleteKey(self, key):
        if (self.__root == None): return False

        node = self.__search(self.__root, key)
        if not node: return False

        if not node.left: self.__transplant(node, node.right)
        elif not node.right: self.__transplant(node, node.left)
        else:
            successor = self.__minimum(node.right)
            if (successor.p != node):
                self.__transplant(successor, successor.right)
                successor.right = node.right
                successor.right.p = successor
            self.__transplant(node, successor)
            successor.left = node.left
            successor.left.p = successor
            
        return True

    def __findScapeGoat(self, node):
        size = 1
        height = 0
        while (node.p):
            height += 1
            sibling = node.p.right if node.p.left == node else node.p.left
            size += 1 + self.__sizeof(sibling)
            if (height > self.__maxHeight(size)): break
            node = node.p
        return size, node.p

    def __flatten(self, node, head):
        if not node : return head
        node.right = self.__flatten(node.right, head)
        return self.__flatten(node.left, node)
            
    def __search(self, node, key):
        if (node == None): return None
        if (node.key == key): return node
        if (node.key > key): return self.__search(node.left, key)
        return self.__search(node.right, key)

    def __build(self, n, x):
        if n == 0:
            x.left = None
            return x
        m = n/2
        r = self.__build(m, x)
        s = self.__build(n - m - 1, r.right)
        r.right = s.left
        s.left = r
        return s

    def __rebuild(self, size, scapegoat, verbose):
        p = scapegoat.p
        if verbose: print 'Rebuild with size', size, 'at scapegoat', scapegoat
       
        w = Node(-2)
        head = self.__flatten(scapegoat, w)
        newroot = self.__build(size, head).left     
        newroot.p = p
        w.left = None
        if (not p): self.__root = newroot
        elif p.key > newroot.key: p.left = newroot
        else: p.right = newroot
        self.__fixParentLink(newroot)
        
    def __fixParentLink(self, node):
        if not node: return
        if node.left:
            node.left.p = node
            self.__fixParentLink(node.left)
        if node.right:
            node.right.p = node
            self.__fixParentLink(node.right)
    
    def __print(self, sb, node, indent):
        if (node == None): return sb
        sb += '----'*indent + str(node) + '\n'
        sb = self.__print(sb, node.left, indent + 1)
        sb = self.__print(sb, node.right, indent + 1)
        return sb

    def __serialize(self, sb, node):
        if (node == None): return sb
        sb = self.__serialize(sb, node.left)
        sb += ' ' + str(node)
        sb = self.__serialize(sb, node.right)
        return sb
    
    def __repr__(self):
        sb = 'Alpha: ' + str(self.__alpha) + '\tSize: ' + str(self.__size) + '\tMax heigh: ' + str(self.__maxHeight(self.__size)) + '\n'
        return self.__print(sb, self.__root, 0)

    def search(self, key):
        return self.__search(self.__root, key)

    def insert(self, key, verbose = False):
        h, inserted = self.__insertKey(key)
        if (h == -1): # duplicated
            if verbose: print 'Duplicated key', key
            
        self.__size += 1
        if (h > self.__maxHeight(self.__size)):
            size, scapegoat = self.__findScapeGoat(inserted)
            if verbose: print 'Add key', key, 'at height', h, self.__maxHeight(self.__size), 'Rebuild at', scapegoat
            if scapegoat: self.__rebuild(size, scapegoat, verbose)

    def delete(self, key, verbose = False):
        if not self.__deleteKey(key):
            if verbose: print 'Key not found', key

        self.__size -= 1
        if self.__root and self.__size < self.__alpha * self.__maxsize:
            if verbose: print 'Size: ', self.__size, 'Maxx size at last rebuilt', self.__maxsize, 'Rebuild'
            self.__rebuild(size, self.__root, verbose)  
            self.__maxsize = self.__size
        if verbose: print 'Delete key: ', key

    def size(self):
        return self.__size

    def getroot(self):
        return self.__root

    # return a string with format
    # alpha, size, list of node in order
    def serialize(self):
        s = self.__serialize('', self.__root)
        return '%s %s%s' % (str(self.__alpha), str(self.__size), s)








        
