"""
MAZESolver — Pygame Renderer
============================
Handles window initialization, grid rendering, animated search progression,
HUD integration, user keyboard controls, and screenshot export.
"""
import datetime
import os
import sys
import pygame
from typing import Dict, Any, Set, Tuple

from src.maze import Maze
from src.visualization.colors import (
    BG_COLOR,
    WALL_COLOR,
    OPEN_COLOR,
    START_COLOR,
    GOAL_COLOR,
    VISITED_COLOR,
    PATH_COLOR,
    FRONTIER_COLOR,
    BORDER_COLOR,
    HUD_WIDTH,
)
from src.visualization.hud import HUD


class Renderer:
    ANIMATION_FPS = 60

    def __init__(self, maze: Maze, result: Dict[str, Any], algo_name: str):
        self.maze = maze
        self.result = result
        self.algo_name = algo_name

        pygame.init()

        # Dynamic cell sizing based on grid dimensions
        max_dim = max(maze.rows, maze.cols)
        self.cell_size = max(10, min(40, 700 // max_dim))

        self.maze_width = maze.cols * self.cell_size
        self.maze_height = maze.rows * self.cell_size

        self.window_width = self.maze_width + HUD_WIDTH
        self.window_height = max(self.maze_height, 460)

        pygame.display.set_caption(f"MAZESolver — {algo_name}")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()

        self.hud = HUD(self.screen, self.maze_width, self.window_height)

        # Animation states
        self.visited_nodes = result.get("visited", [])
        self.solution_path = result.get("path", [])
        self.found = result.get("found", False)
        self.time_taken = result.get("time_taken", 0.0)

        self.steps_per_frame = max(1, len(self.visited_nodes) // 180)
        self.current_step = 0
        self.is_paused = False
        self.is_running = True
        self.status = "SEARCHING"

    def draw_cell(self, pos: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """Draws a single grid cell with a subtle border."""
        r, c = pos
        rect = pygame.Rect(
            c * self.cell_size,
            r * self.cell_size,
            self.cell_size,
            self.cell_size,
        )
        pygame.draw.rect(self.screen, color, rect)
        if self.cell_size > 8:
            pygame.draw.rect(self.screen, BORDER_COLOR, rect, 1)

    def draw_grid(self, revealed_visited: Set[Tuple[int, int]], show_path: bool) -> None:
        """
        Draws the maze grid respecting visual precedence:
        Start / Goal > Path > Frontier > Visited > Wall > Open
        """
        path_set = set(self.solution_path) if show_path else set()
        frontier_pos = (
            self.visited_nodes[self.current_step - 1]
            if 0 < self.current_step <= len(self.visited_nodes)
            else None
        )

        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                pos = (r, c)
                if pos == self.maze.start:
                    color = START_COLOR
                elif pos == self.maze.goal:
                    color = GOAL_COLOR
                elif pos in path_set:
                    color = PATH_COLOR
                elif pos == frontier_pos and self.status == "SEARCHING":
                    color = FRONTIER_COLOR
                elif pos in revealed_visited:
                    color = VISITED_COLOR
                elif self.maze.is_wall(pos):
                    color = WALL_COLOR
                else:
                    color = OPEN_COLOR

                self.draw_cell(pos, color)

    def save_screenshot(self) -> None:
        """Saves current window surface to output/screenshots/."""
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        screenshots_dir = os.path.join(project_root, "output", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        clean_algo = (
            self.algo_name.lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("=", "")
        )
        clean_maze = os.path.splitext(os.path.basename(self.maze.filepath))[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{clean_algo}_{clean_maze}_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)

        pygame.image.save(self.screen, filepath)
        print(f"[Screenshot] Saved to {filepath}")

    def run(self) -> None:
        """Main Pygame display and animation loop."""
        revealed_visited: Set[Tuple[int, int]] = set()

        while self.is_running:
            # Handle Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                    elif event.key == pygame.K_SPACE:
                        self.is_paused = not self.is_paused
                    elif event.key == pygame.K_r:
                        # Reset animation
                        self.current_step = 0
                        revealed_visited.clear()
                        self.status = "SEARCHING"
                        self.is_paused = False
                    elif event.key == pygame.K_s:
                        self.save_screenshot()
                    elif event.key == pygame.K_UP:
                        self.steps_per_frame = min(50, self.steps_per_frame + 1)
                    elif event.key == pygame.K_DOWN:
                        self.steps_per_frame = max(1, self.steps_per_frame - 1)

            # Advance animation if not paused
            if not self.is_paused and self.status == "SEARCHING":
                if self.current_step < len(self.visited_nodes):
                    target_step = min(
                        len(self.visited_nodes),
                        self.current_step + self.steps_per_frame,
                    )
                    for i in range(self.current_step, target_step):
                        revealed_visited.add(self.visited_nodes[i])
                    self.current_step = target_step
                else:
                    self.status = "SOLVED" if self.found else "NO PATH"

            # Clear background
            self.screen.fill(BG_COLOR)

            # Draw maze
            show_path = self.status == "SOLVED"
            self.draw_grid(revealed_visited, show_path)

            # Draw HUD
            explored_count = min(self.current_step, len(self.visited_nodes))
            path_length = len(self.solution_path) if self.found else 0
            self.hud.draw(
                algo_name=self.algo_name,
                maze_filename=self.maze.filepath,
                nodes_explored=explored_count,
                path_length=path_length,
                time_taken=self.time_taken,
                status=self.status,
            )

            pygame.display.flip()
            self.clock.tick(self.ANIMATION_FPS)

        pygame.quit()
