# pygame visualization engine
import datetime
import math
import os
import pygame

from src.maze import Maze
from src.config import Config
from src.visualization.themes import get_theme, next_theme
from src.visualization.hud import HUD
from src.visualization.particles import Particle
from src.visualization.sound_manager import SoundManager
from src.visualization.gif_exporter import GIFExporter

def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )

class Renderer:
    def __init__(self, maze, result, algo_name, theme_name=None, export_gif=False):
        self.maze = maze
        self.result = result
        self.algo_name = algo_name
        self.cfg = Config.get()

        pygame.init()

        self.theme_name = theme_name if theme_name else self.cfg.get_val("theme", "dark")
        self.theme = get_theme(self.theme_name)

        # Consistent, fixed window dimensions across all maze sizes
        self.window_width = 1020
        self.window_height = 700
        self.hud_width = self.cfg.get_val("hud_width", 280)
        self.maze_area_w = self.window_width - self.hud_width

        # Viewport for maze canvas
        pad_x = 16
        pad_y = 16
        avail_w = self.maze_area_w - pad_x * 2
        avail_h = self.window_height - pad_y * 2

        # Auto-scale cells to fit within the viewport
        cell_w = avail_w // max(1, maze.cols)
        cell_h = avail_h // max(1, maze.rows)
        self.cell_size = max(1, min(36, min(cell_w, cell_h)))

        self.maze_width = maze.cols * self.cell_size
        self.maze_height = maze.rows * self.cell_size

        # Center maze within left area
        self.offset_x = pad_x + (avail_w - self.maze_width) // 2
        self.offset_y = pad_y + (avail_h - self.maze_height) // 2

        pygame.display.set_caption(f"MAZESolver 2.0 — {algo_name}")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()

        self.hud = HUD(self.screen, self.maze_area_w, self.window_height, hud_width=self.hud_width)
        self.sound = SoundManager(
            enabled=self.cfg.get_val("sound_enabled", True),
            volume=self.cfg.get_val("sound_volume", 0.3),
        )

        self.visited_nodes = result.get("visited", [])
        self.solution_path = result.get("path", [])
        self.frontier_history = result.get("frontier_history", [])
        self.found = result.get("found", False)
        self.time_taken = result.get("time_taken", 0.0)

        self.visited_colors = {}
        self._recompute_heatmap()

        self.fade_progress = {}
        self.fade_frames = self.cfg.get_val("fade_frames", 8)
        self.revealed_visited = set()

        self.particles = []
        self.goal_burst_triggered = False

        self.path_reveal_step = 0
        self.steps_per_frame = max(
            1,
            self.cfg.get_val("steps_per_frame", 3)
            if len(self.visited_nodes) < 100
            else len(self.visited_nodes) // 100,
        )
        self.current_step = 0
        self.is_paused = False
        self.is_running = True
        self.status = "SEARCHING"

        self.export_gif_flag = export_gif
        self.gif_exporter = None
        if export_gif:
            self.gif_exporter = GIFExporter(
                skip_frames=self.cfg.get_val("gif_skip_frames", 3),
                fps=self.cfg.get_val("gif_fps", 15),
            )

    def _recompute_heatmap(self):
        total = max(1, len(self.visited_nodes))
        cold = self.theme["visited_cold"]
        hot = self.theme["visited_hot"]
        self.visited_colors.clear()
        for idx, pos in enumerate(self.visited_nodes):
            t = idx / (total - 1) if total > 1 else 0.0
            self.visited_colors[pos] = lerp_color(cold, hot, t)

    def draw_glow(self, pos, glow_color, radius=4):
        r, c = pos
        cx = self.offset_x + c * self.cell_size + self.cell_size // 2
        cy = self.offset_y + r * self.cell_size + self.cell_size // 2
        glow_size = self.cell_size + radius * 2
        glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)

        for i in range(radius, 0, -1):
            alpha = int(45 * (1.0 - i / (radius + 1)))
            pygame.draw.rect(
                glow_surf,
                (*glow_color, alpha),
                (radius - i, radius - i, self.cell_size + i * 2, self.cell_size + i * 2),
                border_radius=4,
            )
        self.screen.blit(glow_surf, (cx - glow_size // 2, cy - glow_size // 2))

    def draw_cell(self, pos, color, size_offset=0):
        r, c = pos
        x = self.offset_x + c * self.cell_size - size_offset // 2
        y = self.offset_y + r * self.cell_size - size_offset // 2
        sz = self.cell_size + size_offset
        rect = pygame.Rect(x, y, sz, sz)
        pygame.draw.rect(self.screen, color, rect)
        if self.cell_size > 7 and size_offset == 0:
            pygame.draw.rect(self.screen, self.theme["border"], rect, 1)

    def draw_maze(self):
        ticks = pygame.time.get_ticks()
        pulse = int(math.sin(ticks * 0.004) * 3)

        revealed_path_set = set(self.solution_path[: self.path_reveal_step])
        frontier_pos = (
            self.visited_nodes[self.current_step - 1]
            if 0 < self.current_step <= len(self.visited_nodes)
            else None
        )

        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                pos = (r, c)
                if pos == self.maze.start:
                    self.draw_cell(pos, self.theme["start"], size_offset=pulse)
                elif pos == self.maze.goal:
                    self.draw_cell(pos, self.theme["goal"], size_offset=pulse)
                elif pos in revealed_path_set:
                    is_head = (
                        self.path_reveal_step > 0
                        and pos == self.solution_path[self.path_reveal_step - 1]
                        and self.path_reveal_step < len(self.solution_path)
                    )
                    path_color = (255, 255, 255) if is_head else self.theme["path"]
                    self.draw_cell(pos, path_color)
                elif pos in self.revealed_visited:
                    prog = self.fade_progress.get(pos, self.fade_frames)
                    ratio = min(1.0, prog / max(1, self.fade_frames))
                    target_color = self.visited_colors.get(pos, self.theme["visited_cold"])
                    rendered_color = lerp_color(self.theme["open"], target_color, ratio)
                    self.draw_cell(pos, rendered_color)
                elif self.maze.is_wall(pos):
                    self.draw_cell(pos, self.theme["wall"])
                else:
                    self.draw_cell(pos, self.theme["open"])

        if frontier_pos and self.status == "SEARCHING":
            self.draw_glow(
                frontier_pos,
                self.theme["glow"],
                radius=self.cfg.get_val("glow_radius", 4),
            )
            self.draw_cell(frontier_pos, self.theme["frontier"])

    def trigger_goal_burst(self):
        if not self.goal_burst_triggered and self.maze.goal:
            self.goal_burst_triggered = True
            gr, gc = self.maze.goal
            px = self.offset_x + gc * self.cell_size + self.cell_size / 2.0
            py = self.offset_y + gr * self.cell_size + self.cell_size / 2.0
            count = self.cfg.get_val("particle_count", 40)
            for _ in range(count):
                self.particles.append(Particle(px, py, self.theme["goal"]))
            self.sound.play_goal()

    def save_screenshot(self):
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        shots_dir = os.path.join(root, "output", "screenshots")
        os.makedirs(shots_dir, exist_ok=True)

        clean_algo = (
            self.algo_name.lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("=", "")
            .replace("*", "star")
        )
        clean_maze = os.path.splitext(os.path.basename(self.maze.filepath))[0]
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{clean_algo}_{clean_maze}_{ts}.png"
        filepath = os.path.join(shots_dir, filename)

        pygame.image.save(self.screen, filepath)
        print(f"[Screenshot] Saved: {filepath}")
        return filepath

    def export_gif(self):
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        gifs_dir = os.path.join(root, "output", "gifs")
        os.makedirs(gifs_dir, exist_ok=True)

        clean_algo = (
            self.algo_name.lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("=", "")
            .replace("*", "star")
        )
        clean_maze = os.path.splitext(os.path.basename(self.maze.filepath))[0]
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{clean_algo}_{clean_maze}_{ts}.gif"
        filepath = os.path.join(gifs_dir, filename)

        if not self.gif_exporter:
            self.gif_exporter = GIFExporter(skip_frames=3, fps=15)
            self.gif_exporter.capture(self.screen)

        self.gif_exporter.export(filepath)
        return filepath

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
                        self.current_step = 0
                        self.path_reveal_step = 0
                        self.revealed_visited.clear()
                        self.fade_progress.clear()
                        self.particles.clear()
                        self.goal_burst_triggered = False
                        self.status = "SEARCHING"
                        self.is_paused = False
                    elif event.key == pygame.K_s:
                        self.save_screenshot()
                    elif event.key == pygame.K_g:
                        self.export_gif()
                    elif event.key == pygame.K_t:
                        self.theme_name = next_theme(self.theme_name)
                        self.theme = get_theme(self.theme_name)
                        self._recompute_heatmap()
                    elif event.key == pygame.K_m:
                        self.sound.toggle_mute()
                    elif event.key == pygame.K_1:
                        self.hud.active_tab = 1
                    elif event.key == pygame.K_2:
                        self.hud.active_tab = 2
                    elif event.key == pygame.K_3:
                        self.hud.active_tab = 3
                    elif event.key == pygame.K_UP:
                        self.steps_per_frame = min(100, self.steps_per_frame + 2)
                    elif event.key == pygame.K_DOWN:
                        self.steps_per_frame = max(1, self.steps_per_frame - 2)

            if not self.is_paused:
                for pos in list(self.fade_progress.keys()):
                    if self.fade_progress[pos] < self.fade_frames:
                        self.fade_progress[pos] += 1

                if self.status == "SEARCHING":
                    if self.current_step < len(self.visited_nodes):
                        target = min(
                            len(self.visited_nodes),
                            self.current_step + self.steps_per_frame,
                        )
                        for i in range(self.current_step, target):
                            node_pos = self.visited_nodes[i]
                            self.revealed_visited.add(node_pos)
                            self.fade_progress[node_pos] = 0

                        if self.current_step % 4 == 0:
                            self.sound.play_tick()

                        self.current_step = target
                    else:
                        if self.found:
                            self.status = "REVEALING_PATH"
                        else:
                            self.status = "NO PATH"

                elif self.status == "REVEALING_PATH":
                    if self.path_reveal_step < len(self.solution_path):
                        self.path_reveal_step += max(1, self.steps_per_frame // 2)
                    else:
                        self.path_reveal_step = len(self.solution_path)
                        self.status = "SOLVED"
                        self.trigger_goal_burst()

            for p in self.particles:
                p.update()
            self.particles = [p for p in self.particles if p.is_alive]

            self.screen.fill(self.theme["bg"])
            self.draw_maze()

            for p in self.particles:
                p.draw(self.screen)

            frontier_snap = (
                self.frontier_history[self.current_step - 1]
                if 0 < self.current_step <= len(self.frontier_history)
                else None
            )
            explored_count = min(self.current_step, len(self.visited_nodes))
            path_len = len(self.solution_path) if self.found else 0

            self.hud.draw(
                algo_name=self.algo_name,
                maze_filename=self.maze.filepath,
                nodes_explored=explored_count,
                path_length=path_len,
                time_taken=self.time_taken,
                status="SOLVED" if self.status == "REVEALING_PATH" else self.status,
                theme=self.theme,
                theme_name=self.theme_name,
                total_cells=self.maze.rows * self.maze.cols,
                frontier_snapshot=frontier_snap,
                sound_enabled=self.sound.enabled,
                steps_per_frame=self.steps_per_frame,
            )

            if self.gif_exporter:
                self.gif_exporter.capture(self.screen)
                if (
                    self.status in ("SOLVED", "NO PATH")
                    and len(self.particles) == 0
                    and self.export_gif_flag
                ):
                    self.export_gif()
                    self.is_running = False

            pygame.display.flip()
            self.clock.tick(self.cfg.get_val("animation_fps", 60))

        # note: do not call pygame.quit() here so parent GUI launcher stays alive
