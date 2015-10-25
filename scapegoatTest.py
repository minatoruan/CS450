import scapegoat
testfn = 'texts.txt'

def buildTreeFromFile(fn):
    tree = None
    with open(fn, 'r') as reader:
        for row in reader:
            print row
            if row.startswith('BuildTreeFromFile') : continue
            tree = runCommand(tree, row)
    return tree

def runCommand(tree, command):
    splits = [s.strip() for s in command.split(' ')]
    if (splits[0] == 'BuildTree'):
        tree = scapegoat.Tree(float(splits[1]), int(splits[2]))
    elif (tree and splits[0] == 'Insert'):
        tree.insert(int(splits[1]), verbose = True)
    elif (tree and splits[0] == 'Search'):
        node = tree.search(int(splits[1]))
        if node: print 'Node found', node
        else: print 'Not found node', splits[1]
    elif (tree and splits[0] == 'Print'):
        print tree
    elif (tree and splits[0] == 'Delete'):
        tree.delete(int(splits[1]), verbose = True)
    elif (splits[0] == 'BuildTreeFromFile'):
        tree = buildTreeFromFile(testfn)
    return tree

s = 0
tree = None
while s != 'Done':
    print '='*40
    print 'ScapeGoat Tree'
    print '1. BuildTree alpha, key (Ex:  BuildTree alpha key)'
    print '2. Insert key (Ex:  Insert key)'
    print '3. Search key (Ex:  Search key)'
    print '4. Delete key (Ex:  Delete key)'
    print '5. Print (Ex: Print)'
    print '6. BuildTreeFromFile (Ex: BuildTreeFromFile)'
    print '7. Done (Ex: Done)'
    print '='*40
    s = raw_input('Command: ')
    tree = runCommand(tree, s)
    
