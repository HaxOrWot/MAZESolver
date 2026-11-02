# loads and handles maze representation
class Maze:
    # UP, DOWN, LEFT, RIGHT
    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, filepath: str):
        self.grid = []
        self.rows = 0
        self.cols = 0
        self.start = None
        self.goal = None
        self.filepath = filepath
        self.load_from_file(filepath)

    def load_from_file(self, filepath: str):
        """reads text file and parses S and G"""
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\r\n") for line in f]

        lines = [line for line in lines if line]
        if not lines:
            raise ValueError("Maze file is empty.")

        self.grid = [list(line) for line in lines]
        self.rows = len(self.grid)
        self.cols = max(len(row) for row in self.grid)

        # pad shorter rows if needed
        for r in range(self.rows):
            if len(self.grid[r]) < self.cols:
                self.grid[r].extend([" "] * (self.cols - len(self.grid[r])))

        start_found = False
        goal_found = False

        for r in range(self.rows):
            for c in range(self.cols):
                char = self.grid[r][c]
                if char == "S":
                    self.start = (r, c)
                    start_found = True
                elif char == "G":
                    self.goal = (r, c)
                    goal_found = True

        if not start_found:
            raise ValueError("Start position 'S' not found in maze file.")
        if not goal_found:
            raise ValueError("Goal position 'G' not found in maze file.")

        # TODO: handle edge case where start == goal

    def is_in_bounds(self, pos: tuple) -> bool:
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_wall(self, pos: tuple) -> bool:
        if not self.is_in_bounds(pos):
            return False
        return self.grid[pos[0]][pos[1]] == "#"

    def is_valid(self, pos: tuple) -> bool:
        return self.is_in_bounds(pos) and not self.is_wall(pos)

    def get_neighbors(self, pos: tuple):
        # returns valid cardinal neighbors
        neighbors = []
        r, c = pos
        for dr, dc in self.DIRECTIONS:
            nb = (r + dr, c + dc)
            if self.is_valid(nb):
                neighbors.append(nb)
        return neighbors

    def display(self):
        for row in self.grid:
            print("".join(row))
