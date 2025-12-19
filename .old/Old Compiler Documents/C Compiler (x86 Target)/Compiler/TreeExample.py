
from itertools import chain

def single(item):
    yield item

class Node:

    def __init__(self, value):
        self.value = value
        self.children = []

    def __repr__(self):
        return f"{self.value}"

    def __iter__(self):
        for c in self.children:
            for cc in c:
                yield cc
        yield self

if __name__ == "__main__":

    root = Node(6)
    root.children.extend([Node(2), Node(23), Node(7)])
    root.children[0].children.append([Node(93), Node(4)])
    root.children[2].children.append([Node(56), Node(400)])

    for n in root:
        print(n)
    