"""
Module containing various helper functions to be used during SWT
"""

import numpy as np

class ConnectedComponents(object):
    """
    Class implementing the Connected Components Algorithm
    """

    def __init__(self, swt_image):
        self.swt_image = swt_image
        self.image_shape = self.swt_image.shape
        self.label_image = np.zeros(self.image_shape, np.uint64)

        self.dsa = []
        for i in xrange(self.image_shape[0]):
            for j in xrange(self.image_shape[1]):
                self.dsa.append(i*self.image_shape[1] + j)

    def find_root(self, node):
        """
        Method to find the root of a node idx
        """

        if node == self.dsa[node]:
            return node
        self.dsa[node] = self.find_root(self.dsa[node])
        return self.dsa[node]

    def create_union(self, row1, col1, row2, col2):
        """
        Method to make node idx the parent of node jdx
        """

        root1 = self.find_root(row1*self.image_shape[1] + col1)
        root2 = self.find_root(row2*self.image_shape[1] + col2)

        if root1 == root2:
            return
        self.dsa[root1] = root2

    def label_components(self):
        """
        Method to perform the second pass for assigning root nodes
        """

        for i in xrange(self.image_shape[0]):
            for j in xrange(self.image_shape[1]):
                self.dsa[i*self.image_shape[1] + j] = self.find_root(i*self.image_shape[1] + j);


    def find_connected_components(self):
        """
        Method to find connected components and assign them labels
        """

        neighbor_threshold = 3.0

        for y in xrange(self.image_shape[0]):
            for x in xrange(self.image_shape[1]):
                sw_point = self.swt_image[y, x]
                if sw_point < np.Infinity and sw_point > 0:
                    neighbors = [(y, x-1), (y-1, x-1), (y-1, x), (y-1, x+1)]

                    for neighbor in neighbors:
                        if neighbor[0] > 0 and neighbor[1] > 0 and neighbor[0] < self.image_shape[0] and neighbor[1] < self.image_shape[1]:
                            sw_neighbor = self.swt_image[neighbor]

                            if sw_neighbor/sw_point < neighbor_threshold and sw_point/sw_neighbor < neighbor_threshold:
                                self.create_union(y, x, neighbor[0], neighbor[1])
