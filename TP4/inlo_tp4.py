# encoding utf-8

from collections import deque

"""This program permits to create binary trees. We can add nodes, calculate the depth
and display the tree from a chosen node."""

class BinaryTree() :
    """This class permits to create the root of a binary tree."""
    def __init__(self) :
        """"Initialization of the tree."""
        self.root = None

    def tree_left_right(self) :
        """Displaying the tree from the root to the end, from left to right."""
        return self.root.display_left_right()

    def tree_up_down(self) :
        """Displaying the tree from the root to the end, from up to down."""
        return self.root.display_up_down()

class Node() :
    """This class permits to add nodes to a biinary tree. We can add only one node to the
    right or the left, or we can add both. The node has to be created before to be added.
    The depth of a new node is automaticaly updated while added to the tree. We can display
    all the nodes from a chosen one. And we can print the tree derived from a node from two
    diffrent methods."""

    def __init__(self, value) :
        """This method permits to create a new node. It takes in argument the value of the node."""
        self.left = None
        self.right = None
        self.depth = 0
        self.value = value

    def add_node(self, left = None, right = None) :
        """This methods permits to add nodes to another one. We can add only one of the left
        and right nodes, or both. The depth of the new nodes is automaticaly changed."""
        self.left = left
        self.right = right
        if self.left :
            left.depth = self.depth + 1
            left.update_children_depth()
        if self.right :
            right.depth = self.depth + 1
            right.update_children_depth()

    def update_children_depth(self) :
        """This methods, called in the add_node methods, permits to update the children nodes
        depth. If the added node already has left and right nodes, all the following nodes will
        have there depth updated."""
        if self.left :
            self.left.depth = self.depth + 1
            self.left.update_children_depth()
        if self.right :
            self.right.depth = self.depth + 1
            self.right.update_children_depth()
        # pass is used so that there is no return -> not returning None.
        # pass

    def display_node(self) :
        """This method is used to display all the nodes deriving from another one. This method
        does not return a tree, only the nodes are printed one by one."""
        retour = str(self)
        if self.left :
            retour += " " + self.left.display_node()
        if self.right :
            retour += " " + self.right.display_node()
        return retour

    def display_left_right(self, level = 0) :
        """This methods is used to display the tree from the left to the right. It uses recursion
        to increase the level in the tree. The level is first set to 0."""
        tree = str(self)
        if self.left :
            tree += "\n"
            for i in range(0, level+1) :
                tree += "\t"
            tree += self.left.display_left_right(level+1)
        if self.right :
            tree += "\n"
            for i in range(0, level+1) :
                tree += "\t"
            tree += self.right.display_left_right(level+1)
        return tree

    # def display_up_down(self, level = 0) :
    #     """This methods is used to display the tree from up to down. It uses recursion to increase
    #     the level in the tree using the max_depth. The level is first set to 0."""
    #     max_depth = self.find_depth()
    #     nb_val_final = 2**max_depth
    #     # pour le premier noeud :
    #     left_space_nb = int(nb_val_final/(2**(level)))
    #     right_space_nb = int(nb_val_final/(2**(level)))
    #     left_space = ""
    #     right_space = ""
    #     for i in range(left_space_nb) :
    #         left_space += "  "
    #     for i in range(right_space_nb) :
    #         right_space += "  "
    #     tree = left_space + str(self) + right_space + "\n"
    #     if self.left :
    #         tree += self.left.display_up_down(level + 1)
    #     if self.right :
    #         tree += self.right.display_up_down(level + 1)
    #     return tree

    def dico_for_up_down(self) :
        """This methods is used to create a dictionnary containing the tree. The dictionnary keys
        goes from 0 to the max_depth of the tree. Considering that this is a binary tree, we have
        got all the nodes corresponding to a depth in the value list of any key, with adding a tab
        in every place there is no node. The method is called in the display_up_down method."""
        # Creates an empty dictionnary that will contain the nodes per levels :
        max_depth = self.find_depth()
        dico = {}
        for k in range(max_depth+1) :
            dico[k] = []
        # Create an empty queue (using the collection library) :
        queue = deque()
        # Add the root node to the queue :
        queue.append(self)
        # For each level of the tree :
        for i in range(max_depth+1) :
            # Get the number of nodes in the queue
            nodes_number = len(queue)
            # Loop through the nodes at the current level :
            for j in range(nodes_number) :
                # Remove the first node from the queue :
                current_node = queue.popleft()
                # Put the node in the dictionnary :
                dico[i].append(str(current_node))
                # If the element in the queue is a node :
                if isinstance(current_node, Node) :
                    # If the current node has a left child, add it to the queue :
                    if current_node.left :
                        queue.append(current_node.left)
                    else : # Else, add a tab :
                        queue.append("\t")
                    # If the current node has a right child, add it to the queue :
                    if current_node.right :
                        queue.append(current_node.right)
                    else : # Else, add a tab :
                        queue.append("\t")
                # If the element in the queue is "\t" :
                else :
                    queue.append("\t") # for the missing left child
                    queue.append("\t") # for the missing right child
        return dico

    def display_up_down(self) :
        dico = self.dico_for_up_down()
        space_number_list = []
        for i in range(len(dico.keys())) :
            space_number_list.append(int((2**i)/2))
        space_number_list.reverse()
        return space_number_list

    def is_leaf(self) :
        """This methods is used to know if we are at the end of a branch or if there is still
        at least another node after the actual one. The method is called in the find_depth method.
        It returns a boolean."""
        return self.left is None and self.right is None

    def find_depth(self, max_depth = 0) :
        """This method is used to find the maximum depth of a tree. It takes an optional argument
        which is the maximum depth."""
        # if the node is a leaf (end of a branch) :
        if self.is_leaf() :
            # and if its depth is > actual max_depth
            if self.depth > max_depth :
                return self.depth
        # if the node is not a leaf :
        # recursion is used on the child nodes with a new max_depth until it is a leaf
        if self.right :
            max_depth = self.right.find_depth(max_depth)
        if self.left :
            max_depth = self.left.find_depth(max_depth)
        # when all the tree has been verified, we have the max_depth
        return max_depth

    def __str__(self) -> str:
        """This method is used to print the nodes. It returns 'value/depth' of the node."""
        return str(self.value) + "/" + str(self.depth)

if __name__ == "__main__" :
    # creation of the nodes :
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node5 = Node(5)
    node6 = Node(6)
    node7 = Node(7)
    node8 = Node(8)
    node9 = Node(9)
    node10 = Node(10)
    node11 = Node(11)
    node12 = Node(12)
    node13 = Node(13)
    node14 = Node(14)
    node15 = Node(15)
    # creation of the tree starting with the first node as root :
    tree1 = BinaryTree()
    tree1.root = node1
    # adding the nodes to the tree :
    node1.add_node(node2, node3)
    node2.add_node(node4, node5)
    node4.add_node(node7, node8)
    node8.add_node(node11, node12)
    node11.add_node(node15)
    node3.add_node(node6)
    node6.add_node(node9, node10)
    node9.add_node(node13, node14)
    # searching the max_depth from node 1 to the end of the tree :
    print(node1.find_depth(0), "\n")
    # displaying the tree from node 1 to the end on one line :
    print(node1.display_node(), "\n")
    # displaying the tree from the left to the right :
    # print(tree1.tree_left_right(),"\n")
    # displaying the tree from up to down :
    print(tree1.tree_up_down())
