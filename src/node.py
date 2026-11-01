"""
MAZESolver — Node Class
=======================
Represents a search tree node tracking position, parent pointer, and depth.
"""
from typing import Optional, List, Tuple


class Node:
    def __init__(
        self,
        position: Tuple[int, int],
        parent: Optional["Node"] = None,
        depth: int = 0,
    ):
        self.position: Tuple[int, int] = position
        self.parent: Optional["Node"] = parent
        self.depth: int = depth

    def get_path(self) -> List[Tuple[int, int]]:
        """
        Backtrack from current node through parents to get path from start to this node.
        """
        path = []
        curr: Optional[Node] = self
        while curr is not None:
            path.append(curr.position)
            curr = curr.parent
        path.reverse()
        return path

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Node):
            return self.position == other.position
        return False

    def __hash__(self) -> int:
        return hash(self.position)

    def __repr__(self) -> str:
        return f"Node(position={self.position}, depth={self.depth})"
