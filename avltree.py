# COS 120 Hw02
# Author: Dante Lee

# Self-Balancing Binary Search Tree
class AVLTree:

    # Node structure
    class BinaryNode:

        # BinaryNode Constructor
        def __init__(self, key=None):
            self.key = key
            self.left = None
            self.right = None
            self.depth = 1

        def __repr__(self):
            return repr(self.key)
        
        def __eq__(self, other):
            # Integer comparison
            if isinstance(other, int):
                return self.key == other
            # Memory instance comparison
            elif isinstance(other, AVLTree.BinaryNode):
                return self is other
            else:
                return False

        def __lt__(self, other):
            # Integer comparison
            if isinstance(other, int):
                return self.key < other
            # Other node comparison
            elif isinstance(other, AVLTree.BinaryNode):
                return self.key < other.key
            else:
                raise TypeError(f"unsupported operand type(s) for <: {type(self)} and {type(other)}")
        
        def __gt__(self, other):
            # Integer comparison
            if isinstance(other, int):
                return self.key > other
            # Other node comparison
            elif isinstance(other, AVLTree.BinaryNode):
                return self.key > other.key
            else:
                raise TypeError(f"unsupported operand type(s) for >: {type(self)} and {type(other)}")


    # AVLTree Constructor
    def __init__(self):
        self.root = None


    # Inserts the key x into your AVL tree
    def insert(self, key):
        
        def _insert(node, key):

            # Starting at root
            # No node
            if not node:
                return AVLTree.BinaryNode(key)

            elif key < node.key:
                node.left = _insert(node.left, key)
            else:
                node.right = _insert(node.right, key)
            
            node.depth = 1 + max(self.node_height(node.left), self.node_height(node.right))
            balance = self._balance(node)
        
            if balance > 1 and key < node.left.key:
                return self._rotate_right(node)
        
            if balance < -1 and key > node.right.key:
                return self._rotate_left(node)
        
            if balance > 1 and key > node.left.key:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
        
            if balance < -1 and key < node.right.key:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)
        
            return node

        self.root = _insert(self.root, key)


    # Removes key x from your AVL tree
    def remove(self, key):

        def _remove(node, key):
    
            # If this node is null then return node
            if node == None:
                return AVLTree.BinaryNode(key)

            # Traverse down tree recursively
            # Turn left
            if key < node.key:
                node.left = self._remove(node.left, key)

            # Turn right
            elif key > node.key:
                node.right = self._remove(node.right, key)

            # Found key
            else:

                # No children -- leaf node
                if (node.left is None) and (node.right is None):
                    del node
                    node = None

                # Left child
                elif (node.left is not None) and (node.right is None):
                    temp = node
                    node = node.left
                    del temp

                # Right child
                elif (node.right is not None) and (node.left is None):
                    temp = node
                    node = node.right
                    del temp

                # Two children
                else:
                    temp = node.right

                    while temp.left:
                        temp = temp.left

                    node.key = temp.key
                    node.right = self._remove(node.right, temp.key)

                return node

        self.root = _remove(self.root, key)

    
    # Reurns the key that matches x
    def find(self, key):

        # Start at root
        node = self.root

        # While node not null
        while node:
            # Found
            if node.key == key:
                return node
            # Go left
            elif key < node.key:
                node = node.left
            # Go right
            else:
                node = node.right

        # Not found
        return None


    # Returns the current height of the AVL tree
    def tree_height(self):
        
        def _tree_height(node):
            if node is None:
                return -1
            else:
                return max(self.node_height(node.left), self.node_height(node.right)) + 1

        return _tree_height(self.root)


    # Returns the height of a given node
    def node_height(self, node):
        if node is None:
            return -1
        else:
            return max(self.node_height(node.left), self.node_height(node.right)) + 1


    # Returns the depth of the node that contains the x key
    def depth(self, key):

        def _depth(node, key, depth):
            if node is None:
                return None
            elif key < node.key:
                return _depth(node.left, key, depth + 1)
            elif key > node.key:
                return _depth(node.right, key, depth + 1)
            else:
                return depth

        return _depth(self.root, key, 1)
    

    # Returns the linear representation of the tree
    def linear_representation(self):

        def _lr(node):
            if not node:
                return ''
            if not node.left and not node.right:
                return str(node.key)
            if not node.left:
                return str(node.key) + ' -> ' + '_ ' + ', ' + _lr(node.right)
            if not node.right:
                return str(node.key) + ' -> ' + _lr(node.left) + ', _ '
            return str(node.key) + ' -> ' + _lr(node.left) + ', ' + _lr(node.right)

        return _lr(self.root)


    # Get the balance factor of a node - ChatGPT
    def _balance(self, node):
        if node.key is None:
            return 0
        else:
            return self.depth(node.left) - self.depth(node.right)

    
    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        node.depth = 1 + max(self._height(node.left), self._height(node.right))
        new_root.depth = 1 + max(self._height(new_root.left), self._height(new_root.right))
        return new_root


    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        node.depth = 1 + max(self._depth(node.left), self._depth(node.right))
        new_root.depth = 1 + max(self._depth(new_root.left), self._depth(new_root.right))
        return new_root


menu = """\
Choose an option:\n\
1: Add a key\n\
2: Remove a key\n\
3: Find a key\n\
4: Get height of tree\n\
5: Get depth of node\n\
6: Show linear representation\n\
9: Exit\n\
> """

def main():
    
    # Create empty tree
    tree = AVLTree()

    # Initialize choice variable
    choice = 0

    # Menu loop
    while choice != 9:

        # Get choice from user
        choice = input(menu)
        
        # Match user choice to action
        match choice:
            
            # Add a key
            case '1':
                try:
                    key = int(input("Enter a key to add: "))
                    tree.insert(key)
                    print(f"Key {key} added to tree\n")
                    continue
                except:
                    print(f"Invalid key\n") 
                    continue
            
            # Remove a key
            case '2':
                try:
                    key = int(input("Enter a key to remove: "))
                    tree.remove(key)
                    print(f"Key {key} removed from tree\n")
                    continue
                except:
                    print("Invalid key\n")
                    continue

            # Find a key
            case '3':
                try:
                    key = int(input("Enter a key to find: "))
                    key = tree.find(key)
                    print(f"{key} found\n")
                    continue
                except:
                    print("Invalid key\n")
                    continue
            
            # Print height of tree
            case '4':
                print(f"Tree height: {tree.tree_height()}\n")
                continue
            
            # Get depth of node
            case '5':
                try:
                    key = int(input("Enter a key to find the depth of: "))
                    depth = tree.depth(key)

                    if depth is not None:
                        print(f"Key {key} has depth {tree.depth(key)}\n")
                    else:
                        print(f"Key {key} not found\n")
                    continue
                except:
                    print("Invalid key\n")
                    continue

            # Print linear representation
            case '6':
                print(f"Linear representation:\n{tree.linear_representation()}\n")
                continue
            
            # Exit
            case '9':
                print("Goodbye")
                break

            case default:
                print("Invalid choice\n")
                continue


def test_bench():
    tree = AVLTree()

    tree.insert(1)
    tree.insert(2)


if __name__ == "__main__":
    main()
