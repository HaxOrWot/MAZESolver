"""
MAZESolver — HUD (Heads-Up Display)
===================================
Renders the side statistics and control panel for the Pygame visualizer.
"""
import os
import pygame
from src.visualization.colors import (
    HUD_BG,
    HUD_TEXT,
    HUD_ACCENT,
    HUD_DIVIDER,
    HUD_SUCCESS,
    HUD_FAIL,
    HUD_SEARCHING,
    HUD_WIDTH,
)


class HUD:
    def __init__(self, screen: pygame.Surface, maze_area_width: int, window_height: int):
        self.screen = screen
        self.x = maze_area_width
        self.width = HUD_WIDTH
        self.height = window_height

        pygame.font.init()
        font_name = "Consolas"
        try:
            self.font_title = pygame.font.SysFont(font_name, 20, bold=True)
            self.font_label = pygame.font.SysFont(font_name, 13)
            self.font_bold = pygame.font.SysFont(font_name, 14, bold=True)
            self.font_value = pygame.font.SysFont(font_name, 20, bold=True)
            self.font_small = pygame.font.SysFont(font_name, 12)
        except Exception:
            self.font_title = pygame.font.Font(None, 24)
            self.font_label = pygame.font.Font(None, 16)
            self.font_bold = pygame.font.Font(None, 18)
            self.font_value = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 14)

    def draw_divider(self, y: int) -> int:
        """Draws a horizontal divider line and returns next y coordinate."""
        start = (self.x + 12, y)
        end = (self.x + self.width - 12, y)
        pygame.draw.line(self.screen, HUD_DIVIDER, start, end, 1)
        return y + 12

    def draw(
        self,
        algo_name: str,
        maze_filename: str,
        nodes_explored: int,
        path_length: int,
        time_taken: float,
        status: str,
    ) -> None:
        """
        Renders HUD background, title, algorithm name, stats, and legend.
        status: "SEARCHING", "SOLVED", or "NO PATH"
        """
        # Draw background panel
        panel_rect = pygame.Rect(self.x, 0, self.width, self.height)
        pygame.draw.rect(self.screen, HUD_BG, panel_rect)

        # Draw left border line
        pygame.draw.line(self.screen, HUD_DIVIDER, (self.x, 0), (self.x, self.height), 2)

        cur_x = self.x + 16
        cur_y = 18

        # Title
        title_surf = self.font_title.render("MAZESolver", True, (255, 255, 255))
        self.screen.blit(title_surf, (cur_x, cur_y))
        cur_y += 30

        cur_y = self.draw_divider(cur_y)

        # Algorithm & Maze Info
        lbl_algo = self.font_label.render("Algorithm:", True, (160, 160, 160))
        self.screen.blit(lbl_algo, (cur_x, cur_y))
        cur_y += 18
        val_algo = self.font_bold.render(algo_name, True, HUD_ACCENT)
        self.screen.blit(val_algo, (cur_x, cur_y))
        cur_y += 24

        lbl_maze = self.font_label.render("Maze File:", True, (160, 160, 160))
        self.screen.blit(lbl_maze, (cur_x, cur_y))
        cur_y += 18
        short_maze = os.path.basename(maze_filename)
        if len(short_maze) > 22:
            short_maze = short_maze[:19] + "..."
        val_maze = self.font_bold.render(short_maze, True, HUD_TEXT)
        self.screen.blit(val_maze, (cur_x, cur_y))
        cur_y += 28

        cur_y = self.draw_divider(cur_y)

        # Status Badge
        lbl_status = self.font_label.render("Status:", True, (160, 160, 160))
        self.screen.blit(lbl_status, (cur_x, cur_y))
        cur_y += 20

        if status == "SOLVED":
            status_color = HUD_SUCCESS
        elif status == "NO PATH":
            status_color = HUD_FAIL
        else:
            status_color = HUD_SEARCHING

        pygame.draw.circle(self.screen, status_color, (cur_x + 6, cur_y + 8), 5)
        status_surf = self.font_bold.render(status, True, status_color)
        self.screen.blit(status_surf, (cur_x + 18, cur_y))
        cur_y += 30

        cur_y = self.draw_divider(cur_y)

        # Stats
        lbl_nodes = self.font_label.render("Nodes Explored:", True, (160, 160, 160))
        self.screen.blit(lbl_nodes, (cur_x, cur_y))
        cur_y += 18
        val_nodes = self.font_value.render(str(nodes_explored), True, (255, 255, 255))
        self.screen.blit(val_nodes, (cur_x, cur_y))
        cur_y += 26

        lbl_path = self.font_label.render("Path Length:", True, (160, 160, 160))
        self.screen.blit(lbl_path, (cur_x, cur_y))
        cur_y += 18
        path_str = str(path_length) if status == "SOLVED" else "--"
        val_path = self.font_value.render(path_str, True, (255, 255, 255))
        self.screen.blit(val_path, (cur_x, cur_y))
        cur_y += 26

        lbl_time = self.font_label.render("Time Taken:", True, (160, 160, 160))
        self.screen.blit(lbl_time, (cur_x, cur_y))
        cur_y += 18
        time_text = f"{time_taken * 1000:.2f} ms"
        val_time = self.font_bold.render(time_text, True, (200, 200, 200))
        self.screen.blit(val_time, (cur_x, cur_y))
        cur_y += 32

        cur_y = self.draw_divider(cur_y)

        # Controls Legend
        controls = [
            ("[SPACE]", "Pause / Resume"),
            ("[R]", "Restart"),
            ("[S]", "Save Screenshot"),
            ("[ESC]", "Quit"),
        ]
        for key, desc in controls:
            k_surf = self.font_small.render(key, True, HUD_ACCENT)
            d_surf = self.font_small.render(desc, True, (160, 160, 160))
            self.screen.blit(k_surf, (cur_x, cur_y))
            self.screen.blit(d_surf, (cur_x + 55, cur_y))
            cur_y += 18
