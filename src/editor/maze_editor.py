# simple interactive maze editor using pygame
import copy
import datetime
import os
import sys
import pygame

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.generator.recursive_backtrack import RecursiveBacktrackGenerator
from src.maze import Maze
from src.algorithms.bfs import BFSSolver
from src.algorithms.dfs import DFSSolver
from src.algorithms.astar import AStarSolver
from src.visualization.themes import get_theme, next_theme

class MazeEditor:
    TOOLBAR_HEIGHT = 44
    STATUSBAR_HEIGHT = 28

    def __init__(self, rows=21, cols=21, theme_name="dark"):
        pygame.init()
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cols = cols if cols % 2 == 1 else cols + 1

        self.theme_name = theme_name
        self.theme = get_theme(theme_name)

        # Standard fixed window size across all maze sizes
        self.window_w = 960
        self.window_h = 700

        avail_w = self.window_w - 32
        avail_h = self.window_h - self.TOOLBAR_HEIGHT - self.STATUSBAR_HEIGHT - 32

        self.cell_size = max(2, min(32, min(avail_w // self.cols, avail_h // self.rows)))
        self.canvas_w = self.cols * self.cell_size
        self.canvas_h = self.rows * self.cell_size

        self.offset_x = (self.window_w - self.canvas_w) // 2
        self.offset_y = self.TOOLBAR_HEIGHT + 16 + (avail_h - self.canvas_h) // 2

        pygame.display.set_caption("MAZESolver — Interactive Maze Editor")
        try:
            icon_p = os.path.join(PROJECT_ROOT, "assets", "icons", "app_icon.png")
            if os.path.exists(icon_p):
                pygame.display.set_icon(pygame.image.load(icon_p))
        except Exception:
            pass
        self.screen = pygame.display.set_mode((self.window_w, self.window_h))
        self.clock = pygame.time.Clock()

        pygame.font.init()
        font_name = "Consolas"
        try:
            self.font_btn = pygame.font.SysFont(font_name, 12, bold=True)
            self.font_status = pygame.font.SysFont(font_name, 12)
        except Exception:
            self.font_btn = pygame.font.Font(None, 16)
            self.font_status = pygame.font.Font(None, 16)

        self.grid = self._init_empty_grid()
        self.undo_stack = []
        self.start = (1, 1)
        self.goal = (self.rows - 2, self.cols - 2)
        self.grid[self.start[0]][self.start[1]] = "S"
        self.grid[self.goal[0]][self.goal[1]] = "G"

        self.tool = "wall"
        self.solution_overlay = set()
        self.status_msg = "Ready | Left-Click: Toggle Wall | Right-Click: S/G | B: BFS | Ctrl+S: Save"
        self.is_running = True

        # Cached canvas surface for ultra-fast 60 FPS rendering without frame drops
        self.canvas_surf = pygame.Surface((self.canvas_w, self.canvas_h))
        self.dirty = True

    def _init_empty_grid(self):
        grid = [["#"] * self.cols for _ in range(self.rows)]
        for r in range(1, self.rows - 1):
            for c in range(1, self.cols - 1):
                grid[r][c] = " "
        return grid

    def push_undo(self):
        self.undo_stack.append(copy.deepcopy(self.grid))
        if len(self.undo_stack) > 25:
            self.undo_stack.pop(0)

    def undo(self):
        if self.undo_stack:
            self.grid = self.undo_stack.pop()
            self._re_detect_start_goal()
            self.solution_overlay.clear()
            self.status_msg = "Undid last action."
            self.dirty = True

    def _re_detect_start_goal(self):
        self.start = None
        self.goal = None
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == "S":
                    self.start = (r, c)
                elif self.grid[r][c] == "G":
                    self.goal = (r, c)

    def _cell_at(self, mx, my):
        if mx < self.offset_x or mx >= self.offset_x + self.canvas_w:
            return None
        if my < self.offset_y or my >= self.offset_y + self.canvas_h:
            return None
        c = (mx - self.offset_x) // self.cell_size
        r = (my - self.offset_y) // self.cell_size
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return (r, c)
        return None

    def save_maze(self, filepath=None):
        if not self.start:
            self.status_msg = "Error: Start cell 'S' is missing!"
            return False
        if not self.goal:
            self.status_msg = "Error: Goal cell 'G' is missing!"
            return False

        if not filepath:
            data_dir = os.path.join(PROJECT_ROOT, "data")
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(data_dir, f"custom_maze_{self.rows}x{self.cols}_{ts}.txt")

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        txt = "\n".join("".join(row) for row in self.grid)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(txt)

        self.status_msg = f"Saved: {os.path.basename(filepath)}"
        print(f"[Editor] Saved to {filepath}")
        return True

    def generate_random(self):
        self.push_undo()
        gen = RecursiveBacktrackGenerator(self.rows, self.cols)
        gen.generate()
        self.grid = gen.grid
        self.start = gen.start
        self.goal = gen.goal
        self.solution_overlay.clear()
        self.status_msg = "Generated procedural maze."
        self.dirty = True

    def solve_preview(self, algo="bfs"):
        if not self.start or not self.goal:
            self.status_msg = "Cannot solve: Start or Goal missing!"
            return

        temp_file = os.path.join(PROJECT_ROOT, "output", "_editor_temp.txt")
        os.makedirs(os.path.dirname(temp_file), exist_ok=True)
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write("\n".join("".join(row) for row in self.grid))

        try:
            maze = Maze(temp_file)
            if algo == "dfs":
                res = DFSSolver(maze).solve()
            elif algo == "astar":
                res = AStarSolver(maze).solve()
            else:
                res = BFSSolver(maze).solve()

            if res["found"]:
                self.solution_overlay = set(res["path"])
                self.status_msg = f"{algo.upper()}: Path={res['path_length']} | Explored={res['nodes_explored']} in {res['time_taken']*1000:.2f}ms"
            else:
                self.solution_overlay.clear()
                self.status_msg = f"{algo.upper()}: No solution path exists!"
            self.dirty = True
        except Exception as e:
            self.status_msg = f"Solve error: {e}"

    def _render_canvas(self):
        """Draws all cells to the offscreen canvas surface only when dirty"""
        self.canvas_surf.fill(self.theme["bg"])
        for r in range(self.rows):
            for c in range(self.cols):
                pos = (r, c)
                val = self.grid[r][c]
                if val == "S":
                    color = self.theme["start"]
                elif val == "G":
                    color = self.theme["goal"]
                elif pos in self.solution_overlay:
                    color = self.theme["path"]
                elif val == "#":
                    color = self.theme["wall"]
                else:
                    color = self.theme["open"]

                rect = pygame.Rect(
                    c * self.cell_size,
                    r * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.canvas_surf, color, rect)
                if self.cell_size > 10:
                    pygame.draw.rect(self.canvas_surf, self.theme["border"], rect, 1)
        self.dirty = False

    def run(self):
        drawing_wall = False
        drawing_open = False

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                elif event.type == pygame.KEYDOWN:
                    mods = pygame.key.get_mods()
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                    elif (mods & pygame.KMOD_CTRL) and event.key == pygame.K_s:
                        self.save_maze()
                    elif (mods & pygame.KMOD_CTRL) and event.key == pygame.K_z:
                        self.undo()
                    elif (mods & pygame.KMOD_CTRL) and event.key == pygame.K_g:
                        self.generate_random()
                    elif (mods & pygame.KMOD_CTRL) and event.key == pygame.K_c:
                        self.push_undo()
                        self.grid = self._init_empty_grid()
                        self.start = (1, 1)
                        self.goal = (self.rows - 2, self.cols - 2)
                        self.grid[1][1] = "S"
                        self.grid[self.rows - 2][self.cols - 2] = "G"
                        self.solution_overlay.clear()
                        self.dirty = True
                    elif event.key == pygame.K_b:
                        self.solve_preview("bfs")
                    elif event.key == pygame.K_d:
                        self.solve_preview("dfs")
                    elif event.key == pygame.K_a:
                        self.solve_preview("astar")
                    elif event.key == pygame.K_t:
                        self.theme_name = next_theme(self.theme_name)
                        self.theme = get_theme(self.theme_name)
                        self.dirty = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = self._cell_at(*event.pos)
                    if pos:
                        r, c = pos
                        if r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1:
                            continue

                        self.push_undo()
                        self.solution_overlay.clear()

                        if event.button == 1:
                            if self.grid[r][c] == "#":
                                self.grid[r][c] = " "
                                drawing_open = True
                            else:
                                if (r, c) == self.start:
                                    self.start = None
                                if (r, c) == self.goal:
                                    self.goal = None
                                self.grid[r][c] = "#"
                                drawing_wall = True
                            self.dirty = True

                        elif event.button == 3:
                            if self.grid[r][c] != "S" and self.grid[r][c] != "G":
                                if self.start:
                                    self.grid[self.start[0]][self.start[1]] = " "
                                self.start = (r, c)
                                self.grid[r][c] = "S"
                            elif self.grid[r][c] == "S":
                                if self.goal:
                                    self.grid[self.goal[0]][self.goal[1]] = " "
                                self.goal = (r, c)
                                self.start = None
                                self.grid[r][c] = "G"
                            else:
                                self.goal = None
                                self.grid[r][c] = " "
                            self.dirty = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing_wall = False
                    drawing_open = False

                elif event.type == pygame.MOUSEMOTION:
                    if drawing_wall or drawing_open:
                        pos = self._cell_at(*event.pos)
                        if pos:
                            r, c = pos
                            if 0 < r < self.rows - 1 and 0 < c < self.cols - 1:
                                if drawing_wall and self.grid[r][c] != "#":
                                    if (r, c) == self.start:
                                        self.start = None
                                    if (r, c) == self.goal:
                                        self.goal = None
                                    self.grid[r][c] = "#"
                                    self.dirty = True
                                elif drawing_open and self.grid[r][c] != " ":
                                    if (r, c) == self.start:
                                        self.start = None
                                    if (r, c) == self.goal:
                                        self.goal = None
                                    self.grid[r][c] = " "
                                    self.dirty = True

            self.screen.fill(self.theme["bg"])

            # toolbar
            tb_rect = pygame.Rect(0, 0, self.window_w, self.TOOLBAR_HEIGHT)
            pygame.draw.rect(self.screen, self.theme["hud_bg"], tb_rect)
            pygame.draw.line(self.screen, self.theme["hud_divider"], (0, self.TOOLBAR_HEIGHT), (self.window_w, self.TOOLBAR_HEIGHT), 1)

            btn_text = "[Ctrl+S] Save | [Ctrl+G] Gen | [Ctrl+Z] Undo | [B] BFS | [D] DFS | [A] A* | [T] Theme | [ESC] Exit"
            self.screen.blit(self.font_btn.render(btn_text, True, self.theme["hud_accent"]), (14, 14))

            # canvas - blit pre-rendered surface
            if self.dirty:
                self._render_canvas()
            self.screen.blit(self.canvas_surf, (self.offset_x, self.offset_y))

            # statusbar
            sb_y = self.window_h - self.STATUSBAR_HEIGHT
            sb_rect = pygame.Rect(0, sb_y, self.window_w, self.STATUSBAR_HEIGHT)
            pygame.draw.rect(self.screen, self.theme["hud_bg"], sb_rect)
            pygame.draw.line(self.screen, self.theme["hud_divider"], (0, sb_y), (self.window_w, sb_y), 1)

            st_surf = self.font_status.render(
                f"{self.status_msg} | Grid: {self.rows}x{self.cols}", True, self.theme["hud_text"]
            )
            self.screen.blit(st_surf, (14, sb_y + 7))

            pygame.display.flip()
            self.clock.tick(60)

        # Do not call pygame.quit() here to keep parent GUI launcher alive

if __name__ == "__main__":
    editor = MazeEditor()
    editor.run()
