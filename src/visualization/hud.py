# sidebar heads-up display
import os
import pygame

ALGO_EXPLANATIONS = {
    "BFS": [
        "Breadth-First Search (BFS):",
        "- Explores level-by-level in concentric rings.",
        "- Uses a FIFO Queue (First In, First Out).",
        "- Guarantees the shortest path on unweighted grids.",
        "- High memory usage: stores entire frontier ring.",
    ],
    "DFS": [
        "Depth-First Search (DFS):",
        "- Dives deeply along a branch before backtracking.",
        "- Uses a LIFO Stack (Last In, First Out).",
        "- Space-efficient: stores only current branch.",
        "- Not optimal: solution path may be meandering.",
    ],
    "DLS": [
        "Depth-Limited Search (DLS):",
        "- Explores like DFS but stops at depth limit L.",
        "- Prevents infinite recursion in deep/cyclic mazes.",
        "- Fails with 'NO PATH' if goal is deeper than L.",
        "- Foundational building block for IDDFS.",
    ],
    "IDDFS": [
        "Iterative Deepening DFS (IDDFS):",
        "- Repeatedly runs DLS with L = 0, 1, 2, ...",
        "- Optimal like BFS (finds shortest path).",
        "- Space-efficient like DFS (O(depth) memory).",
        "- Visits earlier depths repeatedly (small overhead).",
    ],
    "A*": [
        "A* Search (Informed Heuristic Search):",
        "- Evaluates f(n) = g(n) + h(n).",
        "- g(n): exact cost from start to node n.",
        "- h(n): Manhattan distance to goal.",
        "- Expands lowest f(n) first via min-priority queue.",
        "- Dramatically reduces explored search space.",
    ],
}

class HUD:
    def __init__(self, screen, maze_area_width: int, window_height: int, hud_width: int = 280):
        self.screen = screen
        self.x = maze_area_width
        self.width = hud_width
        self.height = window_height
        self.active_tab = 1  # 1: stats, 2: frontier stack, 3: explainer
        self.explain_scroll = 0

        pygame.font.init()
        font_name = "Consolas"
        try:
            self.font_title = pygame.font.SysFont(font_name, 18, bold=True)
            self.font_tab = pygame.font.SysFont(font_name, 12, bold=True)
            self.font_label = pygame.font.SysFont(font_name, 12)
            self.font_bold = pygame.font.SysFont(font_name, 13, bold=True)
            self.font_value = pygame.font.SysFont(font_name, 18, bold=True)
            self.font_small = pygame.font.SysFont(font_name, 11)
        except Exception:
            self.font_title = pygame.font.Font(None, 22)
            self.font_tab = pygame.font.Font(None, 14)
            self.font_label = pygame.font.Font(None, 14)
            self.font_bold = pygame.font.Font(None, 16)
            self.font_value = pygame.font.Font(None, 22)
            self.font_small = pygame.font.Font(None, 13)

    def draw_divider(self, y: int, theme):
        start = (self.x + 12, y)
        end = (self.x + self.width - 12, y)
        pygame.draw.line(self.screen, theme["hud_divider"], start, end, 1)
        return y + 10

    def draw_tab_bar(self, y: int, theme):
        tabs = [("1:Stats", 1), ("2:Insp", 2), ("3:Help", 3)]
        tab_w = (self.width - 24) // 3
        for idx, (label, tab_id) in enumerate(tabs):
            tx = self.x + 12 + idx * tab_w
            rect = pygame.Rect(tx, y, tab_w - 4, 22)
            is_active = self.active_tab == tab_id
            bg_col = theme["hud_divider"] if is_active else theme["hud_bg"]
            text_col = theme["hud_accent"] if is_active else (150, 150, 150)

            pygame.draw.rect(self.screen, bg_col, rect, border_radius=3)
            if is_active:
                pygame.draw.rect(self.screen, theme["hud_accent"], rect, 1, border_radius=3)

            lbl = self.font_tab.render(label, True, text_col)
            lx = tx + (tab_w - 4 - lbl.get_width()) // 2
            self.screen.blit(lbl, (lx, y + 4))
        return y + 30

    def draw(self, algo_name, maze_filename, nodes_explored, path_length, time_taken, status, theme, theme_name, total_cells=100, frontier_snapshot=None, sound_enabled=True, steps_per_frame=1):
        panel_rect = pygame.Rect(self.x, 0, self.width, self.height)
        pygame.draw.rect(self.screen, theme["hud_bg"], panel_rect)
        pygame.draw.line(self.screen, theme["hud_divider"], (self.x, 0), (self.x, self.height), 2)

        cur_x = self.x + 14
        cur_y = 12

        title_surf = self.font_title.render("MAZESolver 2.0", True, (255, 255, 255))
        self.screen.blit(title_surf, (cur_x, cur_y))
        cur_y += 24

        cur_y = self.draw_tab_bar(cur_y, theme)
        cur_y = self.draw_divider(cur_y, theme)

        # tab 1: stats
        if self.active_tab == 1:
            lbl_algo = self.font_label.render("Algorithm:", True, (150, 150, 150))
            self.screen.blit(lbl_algo, (cur_x, cur_y))
            cur_y += 16
            val_algo = self.font_bold.render(algo_name, True, theme["hud_accent"])
            self.screen.blit(val_algo, (cur_x, cur_y))
            cur_y += 20

            lbl_maze = self.font_label.render("Maze File:", True, (150, 150, 150))
            self.screen.blit(lbl_maze, (cur_x, cur_y))
            cur_y += 16
            fname = os.path.basename(maze_filename)
            if len(fname) > 24:
                fname = fname[:21] + "..."
            val_maze = self.font_bold.render(fname, True, theme["hud_text"])
            self.screen.blit(val_maze, (cur_x, cur_y))
            cur_y += 22

            cur_y = self.draw_divider(cur_y, theme)

            if status == "SOLVED":
                st_color = theme["hud_success"]
            elif status == "NO PATH":
                st_color = theme["hud_fail"]
            else:
                st_color = theme["hud_searching"]

            pygame.draw.circle(self.screen, st_color, (cur_x + 6, cur_y + 8), 5)
            st_text = self.font_bold.render(status, True, st_color)
            self.screen.blit(st_text, (cur_x + 18, cur_y))
            cur_y += 24

            cur_y = self.draw_divider(cur_y, theme)

            lbl_nodes = self.font_label.render("Nodes Explored:", True, (150, 150, 150))
            self.screen.blit(lbl_nodes, (cur_x, cur_y))
            cur_y += 16
            val_nodes = self.font_value.render(str(nodes_explored), True, (255, 255, 255))
            self.screen.blit(val_nodes, (cur_x, cur_y))
            cur_y += 22

            # progress bar
            pct = min(1.0, nodes_explored / max(1, total_cells))
            bar_w = self.width - 28
            bar_rect_bg = pygame.Rect(cur_x, cur_y, bar_w, 8)
            pygame.draw.rect(self.screen, theme["hud_divider"], bar_rect_bg, border_radius=3)
            fill_w = int(bar_w * pct)
            if fill_w > 0:
                bar_rect_fill = pygame.Rect(cur_x, cur_y, fill_w, 8)
                pygame.draw.rect(self.screen, theme["hud_accent"], bar_rect_fill, border_radius=3)
            cur_y += 12
            cov_lbl = self.font_small.render(f"Grid Coverage: {int(pct * 100)}%", True, (160, 160, 160))
            self.screen.blit(cov_lbl, (cur_x, cur_y))
            cur_y += 18

            lbl_path = self.font_label.render("Path Length:", True, (150, 150, 150))
            self.screen.blit(lbl_path, (cur_x, cur_y))
            cur_y += 16
            p_str = f"{path_length} steps" if status == "SOLVED" else "--"
            val_path = self.font_value.render(p_str, True, (255, 255, 255))
            self.screen.blit(val_path, (cur_x, cur_y))
            cur_y += 22

            lbl_time = self.font_label.render("Compute Time:", True, (150, 150, 150))
            self.screen.blit(lbl_time, (cur_x, cur_y))
            cur_y += 16
            val_time = self.font_bold.render(f"{time_taken * 1000:.2f} ms", True, (200, 200, 200))
            self.screen.blit(val_time, (cur_x, cur_y))
            cur_y += 22

        # tab 2: frontier
        elif self.active_tab == 2:
            lbl_head = self.font_bold.render("Frontier Inspector:", True, theme["hud_accent"])
            self.screen.blit(lbl_head, (cur_x, cur_y))
            cur_y += 20

            if frontier_snapshot:
                count_lbl = self.font_small.render("Top 8 items in frontier:", True, (170, 170, 170))
                self.screen.blit(count_lbl, (cur_x, cur_y))
                cur_y += 18
                for idx, pos in enumerate(frontier_snapshot[:8]):
                    item_text = self.font_label.render(f"[{idx}] Pos: {pos}", True, theme["hud_text"])
                    self.screen.blit(item_text, (cur_x + 6, cur_y))
                    cur_y += 18
            else:
                msg = self.font_small.render("Frontier is currently empty.", True, (150, 150, 150))
                self.screen.blit(msg, (cur_x, cur_y))
                cur_y += 24

            cur_y = self.draw_divider(cur_y, theme)
            lbl_vis = self.font_label.render(f"Visited Set Size: {nodes_explored}", True, theme["hud_text"])
            self.screen.blit(lbl_vis, (cur_x, cur_y))
            cur_y += 22

        # tab 3: explainer
        elif self.active_tab == 3:
            algo_key = "BFS"
            if "DFS" in algo_name and "IDDFS" not in algo_name:
                algo_key = "DFS"
            elif "DLS" in algo_name:
                algo_key = "DLS"
            elif "IDDFS" in algo_name:
                algo_key = "IDDFS"
            elif "A*" in algo_name or "ASTAR" in algo_name.upper():
                algo_key = "A*"

            lines = ALGO_EXPLANATIONS.get(algo_key, ALGO_EXPLANATIONS["BFS"])
            for line in lines:
                is_hdr = line.endswith(":")
                f = self.font_bold if is_hdr else self.font_small
                col = theme["hud_accent"] if is_hdr else theme["hud_text"]
                surf = f.render(line, True, col)
                self.screen.blit(surf, (cur_x, cur_y))
                cur_y += 19

        # footer controls
        foot_y = self.height - 130
        self.draw_divider(foot_y, theme)
        foot_y += 6

        snd_str = "ON" if sound_enabled else "MUTED"
        info_line = f"Theme: {theme_name.upper()} | Audio: {snd_str} | Speed: {steps_per_frame}x"
        self.screen.blit(self.font_small.render(info_line, True, theme["hud_accent"]), (cur_x, foot_y))
        foot_y += 16

        controls = [("[SPACE] Pause", "[R] Reset"), ("[T] Cycle Theme", "[M] Mute Sound"), ("[S] Screenshot", "[G] Export GIF"), ("[1/2/3] Tabs", "[UP/DN] Speed")]
        for c1, c2 in controls:
            self.screen.blit(self.font_small.render(c1, True, (160, 160, 160)), (cur_x, foot_y))
            self.screen.blit(self.font_small.render(c2, True, (160, 160, 160)), (cur_x + 130, foot_y))
            foot_y += 14
