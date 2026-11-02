# renders BFS, DFS, and DLS side by side
import datetime
import os
import pygame

from src.maze import Maze
from src.visualization.themes import get_theme, next_theme

class SplitPanel:
    def __init__(self, maze, result, algo_name, x_offset, cell_size, theme, header_height=32):
        self.maze = maze
        self.result = result
        self.algo_name = algo_name
        self.x_offset = x_offset
        self.cell_size = cell_size
        self.theme = theme
        self.header_height = header_height

        self.visited_nodes = result.get("visited", [])
        self.solution_path = result.get("path", [])
        self.found = result.get("found", False)
        self.time_taken = result.get("time_taken", 0.0)

        self.current_step = 0
        self.path_reveal_step = 0
        self.status = "SEARCHING"
        self.revealed_visited = set()

    def reset(self):
        self.current_step = 0
        self.path_reveal_step = 0
        self.revealed_visited.clear()
        self.status = "SEARCHING"

    def advance(self, steps):
        if self.status == "SEARCHING":
            if self.current_step < len(self.visited_nodes):
                target = min(len(self.visited_nodes), self.current_step + steps)
                for i in range(self.current_step, target):
                    self.revealed_visited.add(self.visited_nodes[i])
                self.current_step = target
            else:
                self.status = "REVEALING_PATH" if self.found else "NO PATH"

        elif self.status == "REVEALING_PATH":
            if self.path_reveal_step < len(self.solution_path):
                self.path_reveal_step += max(1, steps // 2)
            else:
                self.path_reveal_step = len(self.solution_path)
                self.status = "SOLVED"

    def draw(self, screen, font_title, font_stats):
        hdr_rect = pygame.Rect(self.x_offset, 0, self.maze.cols * self.cell_size, self.header_height)
        pygame.draw.rect(screen, self.theme["hud_bg"], hdr_rect)
        hdr_lbl = font_title.render(self.algo_name, True, self.theme["hud_accent"])
        screen.blit(hdr_lbl, (self.x_offset + 8, 7))

        path_set = set(self.solution_path[: self.path_reveal_step])
        frontier_pos = (
            self.visited_nodes[self.current_step - 1]
            if 0 < self.current_step <= len(self.visited_nodes)
            else None
        )

        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                pos = (r, c)
                if pos == self.maze.start:
                    col = self.theme["start"]
                elif pos == self.maze.goal:
                    col = self.theme["goal"]
                elif pos in path_set:
                    col = self.theme["path"]
                elif pos == frontier_pos and self.status == "SEARCHING":
                    col = self.theme["frontier"]
                elif pos in self.revealed_visited:
                    col = self.theme["visited_cold"]
                elif self.maze.is_wall(pos):
                    col = self.theme["wall"]
                else:
                    col = self.theme["open"]

                rect = pygame.Rect(
                    self.x_offset + c * self.cell_size,
                    self.header_height + r * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(screen, col, rect)
                if self.cell_size > 8:
                    pygame.draw.rect(screen, self.theme["border"], rect, 1)

        stat_y = self.header_height + self.maze.rows * self.cell_size + 6
        st_color = (
            self.theme["hud_success"]
            if self.status in ("SOLVED", "REVEALING_PATH")
            else (self.theme["hud_fail"] if self.status == "NO PATH" else self.theme["hud_searching"])
        )
        display_status = "SOLVED" if self.status == "REVEALING_PATH" else self.status
        stat_line = f"Explored: {min(self.current_step, len(self.visited_nodes))} | {display_status}"
        screen.blit(font_stats.render(stat_line, True, st_color), (self.x_offset + 8, stat_y))

class SplitRenderer:
    HEADER_HEIGHT = 32
    BOTTOM_BAR_HEIGHT = 70

    def __init__(self, maze, results, theme_name="dark"):
        pygame.init()
        self.maze = maze
        self.theme_name = theme_name
        self.theme = get_theme(theme_name)

        max_dim = max(maze.rows, maze.cols)
        self.cell_size = max(8, min(24, 480 // max_dim))

        self.panel_w = self.cell_size * maze.cols
        self.panel_h = self.cell_size * maze.rows + self.HEADER_HEIGHT

        self.panels_data = [
            ("BFS", results.get("bfs", {})),
            ("DFS", results.get("dfs", {})),
            ("DLS", results.get("dls", {})),
        ]

        self.window_w = self.panel_w * 3 + 6
        self.window_h = self.panel_h + self.BOTTOM_BAR_HEIGHT + 24

        pygame.display.set_caption("MAZESolver 2.0 — Split View Comparison")
        self.screen = pygame.display.set_mode((self.window_w, self.window_h))
        self.clock = pygame.time.Clock()

        pygame.font.init()
        font_name = "Consolas"
        try:
            self.font_title = pygame.font.SysFont(font_name, 14, bold=True)
            self.font_stats = pygame.font.SysFont(font_name, 11)
            self.font_bottom = pygame.font.SysFont(font_name, 12)
        except Exception:
            self.font_title = pygame.font.Font(None, 18)
            self.font_stats = pygame.font.Font(None, 14)
            self.font_bottom = pygame.font.Font(None, 16)

        self.panels = []
        for idx, (name, res) in enumerate(self.panels_data):
            offset_x = idx * (self.panel_w + 3)
            self.panels.append(
                SplitPanel(
                    maze,
                    res,
                    name,
                    offset_x,
                    self.cell_size,
                    self.theme,
                    header_height=self.HEADER_HEIGHT,
                )
            )

        self.is_paused = False
        self.is_running = True
        self.steps_per_frame = 3

    def save_screenshot(self):
        shots_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "output",
            "screenshots",
        )
        os.makedirs(shots_dir, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"splitview_{os.path.splitext(os.path.basename(self.maze.filepath))[0]}_{ts}.png"
        path = os.path.join(shots_dir, filename)
        pygame.image.save(self.screen, path)
        print(f"[Screenshot] Saved: {path}")

    def run(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                    elif event.key == pygame.K_SPACE:
                        self.is_paused = not self.is_paused
                    elif event.key == pygame.K_r:
                        for p in self.panels:
                            p.reset()
                        self.is_paused = False
                    elif event.key == pygame.K_s:
                        self.save_screenshot()
                    elif event.key == pygame.K_t:
                        self.theme_name = next_theme(self.theme_name)
                        self.theme = get_theme(self.theme_name)
                        for p in self.panels:
                            p.theme = self.theme
                    elif event.key == pygame.K_UP:
                        self.steps_per_frame = min(50, self.steps_per_frame + 2)
                    elif event.key == pygame.K_DOWN:
                        self.steps_per_frame = max(1, self.steps_per_frame - 2)

            if not self.is_paused:
                for panel in self.panels:
                    panel.advance(self.steps_per_frame)

            self.screen.fill(self.theme["bg"])

            for idx, panel in enumerate(self.panels):
                panel.draw(self.screen, self.font_title, self.font_stats)
                if idx < len(self.panels) - 1:
                    div_x = (idx + 1) * (self.panel_w + 3) - 2
                    pygame.draw.line(self.screen, self.theme["hud_divider"], (div_x, 0), (div_x, self.panel_h + 24), 2)

            # bottom summary
            bar_y = self.panel_h + 24
            bar_rect = pygame.Rect(0, bar_y, self.window_w, self.BOTTOM_BAR_HEIGHT)
            pygame.draw.rect(self.screen, self.theme["hud_bg"], bar_rect)
            pygame.draw.line(self.screen, self.theme["hud_divider"], (0, bar_y), (self.window_w, bar_y), 1)

            summaries = []
            for p in self.panels:
                p_len = str(p.result.get("path_length", 0)) if p.status == "SOLVED" else "--"
                summaries.append(f"{p.algo_name}: Path={p_len} | Exp={len(p.revealed_visited)} | {p.time_taken*1000:.1f}ms")

            summary_str = "  ||  ".join(summaries)
            self.screen.blit(self.font_bottom.render(summary_str, True, self.theme["hud_accent"]), (12, bar_y + 10))

            legend_str = "[SPACE] Pause/Resume | [R] Restart | [T] Theme | [S] Screenshot | [UP/DN] Speed | [ESC] Quit"
            self.screen.blit(self.font_stats.render(legend_str, True, (160, 160, 160)), (12, bar_y + 36))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
