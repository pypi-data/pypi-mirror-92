"""The main grafiti class."""


import threading
from threading import Thread
from queue import Queue


class Node:
    """The central object which represents everything
    """

    def __init__(self, callable_, depends_on=None, *args, **kwargs):
        if not callable(callable_):
            raise Exception(f"{callable_} must be a callable")
        self.callable = callable_

        self.args = args
        self.kwargs = kwargs

        self.depends_on = depends_on or []
        self.output = None

    def backward(self):
        t_lst = []
        for dependency in self.depends_on:
            t = Thread(target=dependency.backward, name=str(dependency))
            t.start()
            t_lst.append(t)

        for t in t_lst:
            t.join()

        self.output = self.callable(*self.args, **self.kwargs)
        return self.output

    def __le__(self, other):
        if isinstance(other, Node):
            other = [other]
        self.depends_on = other

    def clear():
        for dependency in self.depends_on:
            dependency.clea


class Graph:
    """
    Class to generate graphs
    """

    def __init__(self):
        self.nodes = []

    def add_node(self, callable_, depends_on=None):
        """
        Add a node to the graph.

        Parameters
        -----------

        callable_
            The function to be called when this node is `backward`-ed.
        depends_on
            the `Node` s that this node depends on to compute its result

        """
        depends_on = depends_on or []
        node = Node(callable_, depends_on=depends_on)
        self.nodes.append(node)
        return node

    def __getitem__(self, item):
        return

    def __call__(self, callable_, depends_on=None):
        return self.add_node(callable_, depends_on=depends_on)

