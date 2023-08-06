import threading
from threading import Thread
from queue import Queue


class Node:
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


class Graph:
    def __init__(self):
        self.nodes = []

    @classmethod
    def add_node(callable_, depends_on=None):
        node = Node(callable_, depends_on=depends_on)
        self.nodes.append(node)
        return node

