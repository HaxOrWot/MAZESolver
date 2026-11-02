# search tree node
class Node:
    def __init__(self, position: tuple, parent=None, depth: int = 0):
        self.position = position
        self.parent = parent
        self.depth = depth

    def get_path(self):
        """backtracks parents to get path from start"""
        path = []
        curr = self
        while curr is not None:
            path.append(curr.position)
            curr = curr.parent
        path.reverse()
        return path

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.position == other.position
        return False

    def __hash__(self):
        return hash(self.position)

    def __repr__(self):
        return f"Node(pos={self.position}, depth={self.depth})"
