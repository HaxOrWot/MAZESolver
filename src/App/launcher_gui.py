"""
MAZESolver 2.0 — Desktop Launcher GUI
====================================
Graphical dashboard opened when double-clicking the application executable.
Allows point-and-click selection of mazes, algorithms, themes, and modes.
"""
import os
import sys
import pygame
from typing import List, Tuple, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.maze import Maze
from src.algorithms.bfs import BFSSolver
from src.algorithms.dfs import DFSSolver
from src.algorithms.dls import DLSSolver
from src.algorithms.iddfs import IDDFSSolver
from src.algorithms.astar import AStarSolver
from src.generator.recursive_backtrack import RecursiveBacktrackGenerator
from src.visualization.themes import get_theme, THEME_ORDER
from src.visualization.renderer import Renderer
from src.visualization.split_view import SplitRenderer
from src.editor.maze_editor import MazeEditor


class Button:
    def __init__(self, rect: pygame.Rect, text: str, group: str = "", tag: str = ""):
        self.rect = rect
        self.text = text
        self.group = group
        self.tag = tag or text
        self.is_hovered = False

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, is_selected: bool, theme: dict):
        if is_selected:
            bg_col = theme["hud_accent"]
            txt_col = (10, 10, 15)
            border_col = (255, 255, 255)
        elif self.is_hovered:
            bg_col = theme["hud_divider"]
            txt_col = (255, 255, 255)
            border_col = theme["hud_accent"]
        else:
            bg_col = theme["hud_bg"]
            txt_col = theme["hud_text"]
            border_col = theme["border"]

        pygame.draw.rect(screen, bg_col, self.rect, border_radius=4)
        pygame.draw.rect(screen, border_col, self.rect, 1, border_radius=4)

        surf = font.render(self.text, True, txt_col)
        sx = self.rect.x + (self.rect.width - surf.get_width()) // 2
        sy = self.rect.y + (self.rect.height - surf.get_height()) // 2
        screen.blit(surf, (sx, sy))


class LauncherGUI:
    def __init__(self):
        pygame.init()
        self.window_w = 660
        self.window_h = 560
        self.screen = pygame.display.set_mode((self.window_w, self.window_h))
        pygame.display.set_caption("MAZESolver 2.0 — Launcher Hub")
        self.clock = pygame.time.Clock()

        pygame.font.init()
        font_name = "Consolas"
        try:
            self.font_title = pygame.font.SysFont(font_name, 22, bold=True)
            self.font_subtitle = pygame.font.SysFont(font_name, 12)
            self.font_section = pygame.font.SysFont(font_name, 14, bold=True)
            self.font_btn = pygame.font.SysFont(font_name, 12, bold=True)
            self.font_launch = pygame.font.SysFont(font_name, 15, bold=True)
        except Exception:
            self.font_title = pygame.font.Font(None, 26)
            self.font_subtitle = pygame.font.Font(None, 16)
            self.font_section = pygame.font.Font(None, 18)
            self.font_btn = pygame.font.Font(None, 15)
            self.font_launch = pygame.font.Font(None, 20)

        # Selections
        self.selected_maze = "maze_20x20.txt"
        self.selected_algo = "bfs"
        self.selected_theme = "neon"
        self.selected_mode = "visual"  # "visual", "split", "compare", "edit"
        self.status_msg = "Ready. Select configuration and click LAUNCH."

        self.buttons: List[Button] = []
        self._init_buttons()

    def _init_buttons(self):
        self.buttons.clear()

        # 1. Maze Selection (Row 1 & 2)
        mazes = [
            ("10x10", "maze_10x10.txt"),
            ("20x20", "maze_20x20.txt"),
            ("40x40", "maze_40x40.txt"),
            ("50x50", "maze_50x50.txt"),
            ("100x100", "maze_100x100.txt"),
            ("Generate New", "GENERATE"),
        ]
        bw, bh = 95, 28
        start_x, start_y = 30, 95
        for idx, (lbl, tag) in enumerate(mazes):
            bx = start_x + (idx % 6) * (bw + 6)
            by = start_y
            self.buttons.append(Button(pygame.Rect(bx, by, bw, bh), lbl, group="maze", tag=tag))

        # 2. Algorithm Selection
        algos = [("BFS", "bfs"), ("DFS", "dfs"), ("DLS", "dls"), ("IDDFS", "iddfs"), ("A* (Heuristic)", "astar")]
        bw_a, bh_a = 110, 30
        start_y_a = 175
        for idx, (lbl, tag) in enumerate(algos):
            bx = start_x + idx * (bw_a + 8)
            self.buttons.append(Button(pygame.Rect(bx, start_y_a, bw_a, bh_a), lbl, group="algo", tag=tag))

        # 3. Theme Selection
        themes = [("Dark", "dark"), ("Neon", "neon"), ("Retro CRT", "retro"), ("Light", "light")]
        bw_t, bh_t = 110, 26
        start_y_t = 250
        for idx, (lbl, tag) in enumerate(themes):
            bx = start_x + idx * (bw_t + 12)
            self.buttons.append(Button(pygame.Rect(bx, start_y_t, bw_t, bh_t), lbl, group="theme", tag=tag))

        # 4. Mode Selection
        modes = [
            ("▶ Start Visualizer", "visual"),
            ("🖥️ Split-Screen (3 Panels)", "split"),
            ("📊 Compare All 5", "compare"),
            ("✏️ Maze Editor", "edit"),
        ]
        bw_m, bh_m = 140, 36
        start_y_m = 325
        for idx, (lbl, tag) in enumerate(modes):
            bx = start_x + idx * (bw_m + 8)
            self.buttons.append(Button(pygame.Rect(bx, start_y_m, bw_m, bh_m), lbl, group="mode", tag=tag))

        # 5. Launch Big Button
        launch_rect = pygame.Rect(30, 440, self.window_w - 60, 48)
        self.btn_launch = Button(launch_rect, "🚀 LAUNCH MAZESOLVER", group="action", tag="launch")

    def run(self):
        running = True
        while running:
            theme = get_theme(self.selected_theme)
            mouse_pos = pygame.mouse.get_pos()

            for btn in self.buttons + [self.btn_launch]:
                btn.is_hovered = btn.rect.collidepoint(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.buttons:
                        if btn.rect.collidepoint(event.pos):
                            if btn.group == "maze":
                                self.selected_maze = btn.tag
                            elif btn.group == "algo":
                                self.selected_algo = btn.tag
                            elif btn.group == "theme":
                                self.selected_theme = btn.tag
                            elif btn.group == "mode":
                                self.selected_mode = btn.tag

                    if self.btn_launch.rect.collidepoint(event.pos):
                        self._execute_action()

            # Drawing
            self.screen.fill(theme["bg"])

            # Header
            t_surf = self.font_title.render("🧩 MAZESolver 2.0 — Control Center", True, (255, 255, 255))
            self.screen.blit(t_surf, (30, 20))
            sub_surf = self.font_subtitle.render("Select algorithm parameters and execution mode below.", True, (160, 160, 160))
            self.screen.blit(sub_surf, (30, 48))

            # Section 1: Maze
            s1 = self.font_section.render("1. Select Maze Grid:", True, theme["hud_accent"])
            self.screen.blit(s1, (30, 72))

            # Section 2: Algorithm
            s2 = self.font_section.render("2. Select Search Algorithm:", True, theme["hud_accent"])
            self.screen.blit(s2, (30, 150))

            # Section 3: Theme
            s3 = self.font_section.render("3. Select Visual Theme:", True, theme["hud_accent"])
            self.screen.blit(s3, (30, 226))

            # Section 4: Mode
            s4 = self.font_section.render("4. Execution Mode:", True, theme["hud_accent"])
            self.screen.blit(s4, (30, 300))

            # Draw buttons
            for btn in self.buttons:
                is_sel = False
                if btn.group == "maze" and btn.tag == self.selected_maze:
                    is_sel = True
                elif btn.group == "algo" and btn.tag == self.selected_algo:
                    is_sel = True
                elif btn.group == "theme" and btn.tag == self.selected_theme:
                    is_sel = True
                elif btn.group == "mode" and btn.tag == self.selected_mode:
                    is_sel = True
                btn.draw(self.screen, self.font_btn, is_sel, theme)

            # Draw Launch Button
            self.btn_launch.draw(self.screen, self.font_launch, is_selected=True, theme=theme)

            # Status Bar at bottom
            status_surf = self.font_subtitle.render(self.status_msg, True, (180, 180, 180))
            self.screen.blit(status_surf, (30, 510))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def _execute_action(self):
        # Resolve or generate maze
        if self.selected_maze == "GENERATE":
            gen_dir = os.path.join(PROJECT_ROOT, "data", "generated")
            os.makedirs(gen_dir, exist_ok=True)
            gen_file = os.path.join(gen_dir, "launcher_gen.txt")
            gen = RecursiveBacktrackGenerator(25, 25)
            gen.generate()
            gen.save(gen_file)
            maze_path = gen_file
        else:
            maze_path = os.path.join(PROJECT_ROOT, "data", self.selected_maze)
            if not os.path.exists(maze_path):
                maze_path = os.path.join(PROJECT_ROOT, "data", "maze_20x20.txt")

        maze = Maze(maze_path)

        if self.selected_mode == "edit":
            editor = MazeEditor(rows=21, cols=21, theme_name=self.selected_theme)
            editor.run()
            # Restore launcher window after editor closes
            self.screen = pygame.display.set_mode((self.window_w, self.window_h))
            pygame.display.set_caption("MAZESolver 2.0 — Launcher Hub")
            return

        if self.selected_mode == "split":
            bfs_res = BFSSolver(maze).solve()
            dfs_res = DFSSolver(maze).solve()
            dls_res = DLSSolver(maze).solve()
            renderer = SplitRenderer(maze, {"bfs": bfs_res, "dfs": dfs_res, "dls": dls_res}, theme_name=self.selected_theme)
            renderer.run()
            self.screen = pygame.display.set_mode((self.window_w, self.window_h))
            pygame.display.set_caption("MAZESolver 2.0 — Launcher Hub")
            return

        if self.selected_mode == "compare":
            from src.main import print_comparison, append_to_log
            bfs_res = BFSSolver(maze).solve()
            dfs_res = DFSSolver(maze).solve()
            dls_res = DLSSolver(maze).solve()
            iddfs_res = IDDFSSolver(maze).solve()
            astar_res = AStarSolver(maze).solve()
            algo_names = ["BFS", "DFS", "DLS", "IDDFS", "A* (Heuristic)"]
            results = [bfs_res, dfs_res, dls_res, iddfs_res, astar_res]
            print_comparison(results, algo_names)
            for n, r in zip(algo_names, results):
                append_to_log(n, maze_path, r)
            self.status_msg = f"Comparison printed to terminal & saved to output/results_log.txt!"
            return

        # Visual mode
        algo_map = {
            "bfs": (BFSSolver, "BFS"),
            "dfs": (DFSSolver, "DFS"),
            "dls": (DLSSolver, "DLS"),
            "iddfs": (IDDFSSolver, "IDDFS"),
            "astar": (AStarSolver, "A*"),
        }
        cls, name = algo_map.get(self.selected_algo, (BFSSolver, "BFS"))
        res = cls(maze).solve()
        renderer = Renderer(maze, res, name, theme_name=self.selected_theme)
        renderer.run()
        self.screen = pygame.display.set_mode((self.window_w, self.window_h))
        pygame.display.set_caption("MAZESolver 2.0 — Launcher Hub")


if __name__ == "__main__":
    launcher = LauncherGUI()
    launcher.run()
