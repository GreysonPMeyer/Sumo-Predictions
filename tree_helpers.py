class SkNode:
    """Rooted binary tree class with attributes to match sklearn's decision tree object."""
    def __init__(self, label = None):
        self.label = label 
        self.left  = None #left child node
        self.right = None #right child node
        self.feature = None # the feature we are splitting on
        self.threshold = None # the threshold value for the feature we are splitting on
        self.parent = None # the parent node
        self.leaf = False # whether or not this is a leaf node
        self.i_am_left = False # if this is the left child of the parent
        self.i_am_right = False # if this is the right child of the parent
        self.pred = None # For a leaf node, this will be the index of the majority class
        self.n_classes = None 
        self.n_features = None 

    def find_constraints(self):
        """Recursively traverses the tree from child to parent and collects the constraints on each feature"""
        mins = [float('-inf') for i in range(self.n_features)] # list of mins by feature index
        maxs = [float('inf') for i in range(self.n_features)] # list of maxs by feature index
        if self.parent:
            (mins, maxs) = self.parent.find_constraints() # we start with the mins and maxs of our parent
            i = self.parent.feature
            if self.i_am_left:
                maxs[i] = self.parent.threshold 
            if self.i_am_right:
                mins[i] = self.parent.threshold
        return (mins, maxs)


def traversable_nodes(sk_tree_fit_model_object):
    """ Converts a fit sklearn model object into a dictionary of SkNodes"""
    sk_tree = sk_tree_fit_model_object.tree_
    nodes = {i: SkNode(label = i) for i in range(sk_tree.node_count)}
    n_classes = sk_tree.n_classes[0]
    n_features = sk_tree.n_features
    for i in range(sk_tree.node_count):
        nodes[i].n_classes = n_classes
        nodes[i].n_features = n_features
        if sk_tree.feature[i] >= 0:
            nodes[i].left = nodes[sk_tree.children_left[i]]
            nodes[i].left.parent = nodes[i]
            nodes[i].left.i_am_left = True

            nodes[i].right = nodes[sk_tree.children_right[i]]
            nodes[i].right.parent = nodes[i]
            nodes[i].right.i_am_right = True

            nodes[i].threshold  = sk_tree.threshold[i]

            nodes[i].feature = sk_tree.feature[i]
            
        else:
            nodes[i].leaf = True
            nodes[i].pred = sk_tree.value.reshape((-1,n_classes)).argmax(axis = 1)[i]
            
    return nodes