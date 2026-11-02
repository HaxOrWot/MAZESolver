# desktop launcher GUI for MAZESolver
import os
import sys
import pygame

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.maze import Maze
from src.config import Config
from src.algorithms.bfs import BFSSolver
from src.algorithms.dfs import DFSSolver
from src.algorithms.dls import DLSSolver
from src.algorithms.iddfs import IDDFSSolver
from src.algorithms.astar import AStarSolver
from src.generator.recursive_backtrack import RecursiveBacktrackGenerator
from src.generator.prims import PrimsGenerator
from src.visualization.themes import get_theme
from src.visualization.renderer import Renderer
from src.visualization.split_view import SplitRenderer
from src.editor.maze_editor import MazeEditor

def render_fitted_text(font, text, max_width, color):
    """safely renders text clipping with ellipsis if wider than max_width"""
    if font.size(text)[0] <= max_width:
        return font.render(text, True, color)
    for i in range(len(text) - 1, 0, -1):
        trunc = text[:i] + "..."
        if font.size(trunc)[0] <= max_width:
            return font.render(trunc, True, color)
    return font.render("...", True, color)

class CardButton:
    def __init__(self, rect, title, subtitle="", group="", tag="", dot_color=None):
        self.rect = pygame.Rect(rect)
        self.title = title
        self.subtitle = subtitle
        self.group = group
        self.tag = tag or title
        self.dot_color = dot_color
        self.is_hovered = False

    def draw(self, screen, font_title, font_sub, is_selected, palette):
        if is_selected:
            bg_col = palette["btn_sel_bg"]
            border_col = palette["accent"]
            title_col = palette["accent_text"]
            sub_col = palette["accent_sub"]
        elif self.is_hovered:
            bg_col = palette["btn_hover_bg"]
            border_col = palette["border_hover"]
            title_col = palette["text_primary"]
            sub_col = palette["text_muted"]
        else:
            bg_col = palette["card_bg"]
            border_col = palette["border"]
            title_col = palette["text_primary"]
            sub_col = palette["text_muted"]

        pygame.draw.rect(screen, bg_col, self.rect, border_radius=6)
        pygame.draw.rect(screen, border_col, self.rect, 1 if not is_selected else 2, border_radius=6)

        offset_x = 10
        if self.dot_color:
            dot_y = self.rect.y + self.rect.height // 2
            pygame.draw.circle(screen, self.dot_color, (self.rect.x + 12, dot_y), 4)
            offset_x = 22

        avail_w = self.rect.width - offset_x - 8
        if self.subtitle:
            t_surf = render_fitted_text(font_title, self.title, avail_w, title_col)
            s_surf = render_fitted_text(font_sub, self.subtitle, avail_w, sub_col)
            screen.blit(t_surf, (self.rect.x + offset_x, self.rect.y + 7))
            screen.blit(s_surf, (self.rect.x + offset_x, self.rect.y + 25))
        else:
            t_surf = render_fitted_text(font_title, self.title, avail_w, title_col)
            tx = self.rect.x + (self.rect.width - t_surf.get_width()) // 2
            ty = self.rect.y + (self.rect.height - t_surf.get_height()) // 2
            screen.blit(t_surf, (tx, ty))

class LauncherGUI:
    def __init__(self):
        pygame.init()
        self.window_w = 900
        self.window_h = 640
        try:
            icon_p = os.path.join(PROJECT_ROOT, "assets", "icons", "app_icon.png")
            if os.path.exists(icon_p):
                pygame.display.set_icon(pygame.image.load(icon_p))
        except Exception:
            pass
        self.screen = pygame.display.set_mode((self.window_w, self.window_h))
        pygame.display.set_caption("MAZESolver 2.0 — Control Center")
        self.clock = pygame.time.Clock()

        self.palette = {
            "bg": (13, 17, 23),
            "card_bg": (22, 27, 34),
            "card_inner": (17, 21, 28),
            "border": (48, 54, 61),
            "border_hover": (88, 166, 255),
            "btn_hover_bg": (33, 38, 45),
            "btn_sel_bg": (20, 35, 60),
            "accent": (56, 189, 248),
            "accent_text": (125, 211, 252),
            "accent_sub": (56, 189, 248),
            "text_primary": (240, 246, 252),
            "text_muted": (139, 148, 158),
            "text_dark": (10, 15, 20),
            "badge_green": (46, 160, 67),
            "badge_amber": (210, 153, 34),
            "badge_blue": (31, 111, 235),
            "action_bg": (35, 134, 54),
            "action_hover": (46, 160, 67),
        }

        self._init_fonts()

        # runtime state
        self.selected_mode = "visual"
        self.selected_maze = "maze_20x20.txt"
        self.selected_algo = "bfs"
        self.selected_theme = "neon"
        self.anim_speed = 3
        self.sound_enabled = True
        self.dls_limit = 40
        self.gen_algo = "recursive_backtrack"
        self.gen_size = 25
        self.status_msg = "Ready. Configure parameters and launch."

        # cache for preview maze thumbnail
        self.cached_maze_path = None
        self.cached_maze_obj = None
        self.cached_preview_surf = None

        self.buttons = []
        self._init_layout()
        self._update_preview()

    def _init_fonts(self):
        pygame.font.init()
        def get_best_font(size, bold=False):
            for name in ["segoeui", "arial", "consolas"]:
                try:
                    return pygame.font.SysFont(name, size, bold=bold)
                except Exception:
                    pass
            return pygame.font.Font(None, size)

        self.font_logo = get_best_font(20, bold=True)
        self.font_h2 = get_best_font(12, bold=True)
        self.font_title = get_best_font(12, bold=True)
        self.font_body = get_best_font(11, bold=False)
        self.font_small = get_best_font(10, bold=False)
        self.font_action = get_best_font(14, bold=True)
        self.font_mono = pygame.font.SysFont("consolas", 11)

    def _init_layout(self):
        self.buttons.clear()

        # 1. Mode selector cards (top of left panel)
        modes = [
            ("Visual Solver", "Interactive step solve", "visual"),
            ("Split-View", "Synchronized 3-way", "split"),
            ("Benchmark", "5-Algorithm matrix", "compare"),
            ("Maze Editor", "Draw & solve canvas", "edit"),
        ]
        start_x, start_y = 24, 68
        card_w, card_h = 130, 48
        for i, (tit, sub, tag) in enumerate(modes):
            r = (start_x + i * (card_w + 8), start_y, card_w, card_h)
            self.buttons.append(CardButton(r, tit, sub, group="mode", tag=tag))

        # 2. Maze Selection Pills (two rows)
        all_mazes = [
            "maze_5x5.txt", "maze_10x10.txt", "maze_20x20.txt", "maze_30x30.txt",
            "maze_40x40.txt", "maze_50x50.txt", "maze_60x60.txt", "maze_70x70.txt",
            "maze_80x80.txt", "maze_90x90.txt", "maze_100x100.txt", "GENERATE",
        ]
        maze_y = 145
        mw, mh = 84, 28
        for i, m_tag in enumerate(all_mazes):
            col = i % 6
            row = i // 6
            bx = start_x + col * (mw + 8)
            by = maze_y + row * (mh + 6)
            label = "Procedural" if m_tag == "GENERATE" else m_tag.replace("maze_", "").replace(".txt", "")
            self.buttons.append(CardButton((bx, by, mw, mh), label, "", group="maze", tag=m_tag))

        # 3. Algorithm cards
        algos = [
            ("BFS", "Shortest Path • Queue", "bfs"),
            ("DFS", "Deep Branch • Stack", "dfs"),
            ("DLS", "Bounded Depth Limit", "dls"),
            ("IDDFS", "Progressive Deepening", "iddfs"),
            ("A*", "Manhattan Heuristic", "astar"),
        ]
        algo_y = 240
        aw, ah = 102, 48
        for i, (tit, sub, tag) in enumerate(algos):
            bx = start_x + i * (aw + 9)
            self.buttons.append(CardButton((bx, algo_y, aw, ah), tit, sub, group="algo", tag=tag))

        # 4. Themes
        themes = [
            ("Dark", "neon dark", "dark", (100, 181, 246)),
            ("Neon", "cyberpunk", "neon", (0, 255, 200)),
            ("Retro", "phosphor crt", "retro", (0, 255, 0)),
            ("Light", "clean paper", "light", (220, 100, 50)),
        ]
        theme_y = 318
        tw, th = 130, 32
        for i, (tit, sub, tag, dot) in enumerate(themes):
            bx = start_x + i * (tw + 8)
            self.buttons.append(CardButton((bx, theme_y, tw, th), tit, "", group="theme", tag=tag, dot_color=dot))

        # 5. Speed presets
        speeds = [("1x", 1), ("3x", 3), ("5x", 5), ("Max", 20)]
        speed_y = 385
        sp_w, sp_h = 58, 26
        for i, (lbl, val) in enumerate(speeds):
            bx = start_x + 90 + i * (sp_w + 6)
            self.buttons.append(CardButton((bx, speed_y, sp_w, sp_h), lbl, "", group="speed", tag=val))

        # Sound toggle
        self.btn_sound = CardButton((start_x + 380, speed_y, 164, 26), "Audio FX: ON", "", group="sound", tag="toggle")
        self.buttons.append(self.btn_sound)

        # Generator & DLS stepper buttons
        param_y = 445
        self.btn_dls_minus = CardButton((start_x + 126, param_y, 30, 26), "-", "", group="dls", tag="minus")
        self.btn_dls_plus = CardButton((start_x + 204, param_y, 30, 26), "+", "", group="dls", tag="plus")
        self.btn_gen_toggle = CardButton((start_x + 336, param_y, 208, 26), "Gen: Backtracking", "", group="gen_algo", tag="toggle")

        self.buttons.extend([self.btn_dls_minus, self.btn_dls_plus, self.btn_gen_toggle])

        # Launch Action button in bottom bar
        self.action_rect = pygame.Rect(self.window_w - 290, self.window_h - 58, 266, 44)

    def _update_preview(self):
        # loads the maze and pre-draws a miniature 170x170 preview surface
        if self.selected_maze == "GENERATE":
            gen_dir = os.path.join(PROJECT_ROOT, "data", "generated")
            os.makedirs(gen_dir, exist_ok=True)
            gen_file = os.path.join(gen_dir, "_launcher_preview.txt")
            if self.gen_algo == "prims":
                gen = PrimsGenerator(self.gen_size, self.gen_size)
            else:
                gen = RecursiveBacktrackGenerator(self.gen_size, self.gen_size)
            gen.generate()
            gen.save(gen_file)
            maze_path = gen_file
        else:
            maze_path = os.path.join(PROJECT_ROOT, "data", self.selected_maze)
            if not os.path.exists(maze_path):
                maze_path = os.path.join(PROJECT_ROOT, "data", "maze_20x20.txt")

        try:
            maze = Maze(maze_path)
            self.cached_maze_path = maze_path
            self.cached_maze_obj = maze

            pv_size = 170
            surf = pygame.Surface((pv_size, pv_size))
            surf.fill(self.palette["card_inner"])

            cell_w = pv_size / max(1, maze.cols)
            cell_h = pv_size / max(1, maze.rows)

            theme_colors = get_theme(self.selected_theme)

            for r in range(maze.rows):
                for c in range(maze.cols):
                    pos = (r, c)
                    if pos == maze.start:
                        col = theme_colors["start"]
                    elif pos == maze.goal:
                        col = theme_colors["goal"]
                    elif maze.is_wall(pos):
                        col = theme_colors["wall"]
                    else:
                        col = theme_colors["open"]

                    rect = pygame.Rect(
                        int(c * cell_w),
                        int(r * cell_h),
                        max(1, int(cell_w) + 1),
                        max(1, int(cell_h) + 1),
                    )
                    pygame.draw.rect(surf, col, rect)

            self.cached_preview_surf = surf
        except Exception:
            self.cached_preview_surf = None

    def _restore_display(self):
        self.screen = pygame.display.set_mode((self.window_w, self.window_h))
        pygame.display.set_caption("MAZESolver 2.0 — Control Center")
        self._init_fonts()
        self._update_preview()

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            # update hover states
            for btn in self.buttons:
                btn.is_hovered = btn.rect.collidepoint(mouse_pos)
            action_hovered = self.action_rect.collidepoint(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self._execute_action()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.buttons:
                        if btn.rect.collidepoint(event.pos):
                            if btn.group == "mode":
                                self.selected_mode = btn.tag
                            elif btn.group == "maze":
                                self.selected_maze = btn.tag
                                self._update_preview()
                            elif btn.group == "algo":
                                self.selected_algo = btn.tag
                            elif btn.group == "theme":
                                self.selected_theme = btn.tag
                                self._update_preview()
                            elif btn.group == "speed":
                                self.anim_speed = btn.tag
                            elif btn.group == "sound":
                                self.sound_enabled = not self.sound_enabled
                                self.btn_sound.title = f"Audio FX: {'ON' if self.sound_enabled else 'OFF'}"
                            elif btn.group == "dls":
                                if btn.tag == "minus":
                                    self.dls_limit = max(5, self.dls_limit - 5)
                                elif btn.tag == "plus":
                                    self.dls_limit = min(300, self.dls_limit + 5)
                            elif btn.group == "gen_algo":
                                self.gen_algo = "prims" if self.gen_algo == "recursive_backtrack" else "recursive_backtrack"
                                self.btn_gen_toggle.title = f"Gen: {'Prim' if self.gen_algo == 'prims' else 'Backtracking'}"
                                if self.selected_maze == "GENERATE":
                                    self._update_preview()

                    if self.action_rect.collidepoint(event.pos):
                        self._execute_action()

            # draw background
            self.screen.fill(self.palette["bg"])

            # 1. Top Header Bar
            header_rect = pygame.Rect(0, 0, self.window_w, 54)
            pygame.draw.rect(self.screen, self.palette["card_bg"], header_rect)
            pygame.draw.line(self.screen, self.palette["border"], (0, 54), (self.window_w, 54), 1)

            logo_surf = self.font_logo.render("MAZESOLVER", True, self.palette["text_primary"])
            self.screen.blit(logo_surf, (24, 15))

            v_badge = self.font_small.render("v2.0", True, self.palette["accent_text"])
            badge_r = pygame.Rect(174, 18, 38, 18)
            pygame.draw.rect(self.screen, self.palette["btn_sel_bg"], badge_r, border_radius=4)
            pygame.draw.rect(self.screen, self.palette["accent"], badge_r, 1, border_radius=4)
            self.screen.blit(v_badge, (181, 20))

            sub_txt = self.font_body.render("AI Search Studio & Benchmark Environment", True, self.palette["text_muted"])
            self.screen.blit(sub_txt, (224, 20))

            pill_rect = pygame.Rect(self.window_w - 180, 15, 156, 24)
            pygame.draw.rect(self.screen, self.palette["card_inner"], pill_rect, border_radius=12)
            pygame.draw.rect(self.screen, self.palette["border"], pill_rect, 1, border_radius=12)
            pygame.draw.circle(self.screen, self.palette["badge_green"], (self.window_w - 166, 27), 4)
            ready_lbl = self.font_mono.render("System Ready", True, self.palette["text_muted"])
            self.screen.blit(ready_lbl, (self.window_w - 152, 20))

            # 2. Section Headings (Left Panel)
            lbl_mode = self.font_h2.render("EXECUTION MODE", True, self.palette["accent"])
            self.screen.blit(lbl_mode, (24, 55))

            lbl_maze = self.font_h2.render("MAZE GRID ARCHIVE", True, self.palette["accent"])
            self.screen.blit(lbl_maze, (24, 128))

            lbl_algo = self.font_h2.render("SEARCH ALGORITHM", True, self.palette["accent"])
            self.screen.blit(lbl_algo, (24, 222))

            lbl_theme = self.font_h2.render("VISUAL THEME", True, self.palette["accent"])
            self.screen.blit(lbl_theme, (24, 300))

            lbl_opts = self.font_h2.render("RUNTIME PARAMETERS", True, self.palette["accent"])
            self.screen.blit(lbl_opts, (24, 365))

            # Speed label
            sp_label = self.font_body.render("Speed:", True, self.palette["text_muted"])
            self.screen.blit(sp_label, (24, 390))

            # DLS label and value
            dls_label = self.font_body.render("DLS Depth Limit:", True, self.palette["text_muted"])
            self.screen.blit(dls_label, (24, 450))
            val_dls = self.font_mono.render(f"{self.dls_limit:3d}", True, self.palette["accent_text"])
            self.screen.blit(val_dls, (24 + 162, 450))

            # Draw buttons
            for btn in self.buttons:
                is_sel = False
                if btn.group == "mode" and btn.tag == self.selected_mode:
                    is_sel = True
                elif btn.group == "maze" and btn.tag == self.selected_maze:
                    is_sel = True
                elif btn.group == "algo" and btn.tag == self.selected_algo:
                    is_sel = True
                elif btn.group == "theme" and btn.tag == self.selected_theme:
                    is_sel = True
                elif btn.group == "speed" and btn.tag == self.anim_speed:
                    is_sel = True
                elif btn.group == "sound":
                    is_sel = self.sound_enabled

                btn.draw(self.screen, self.font_title, self.font_small, is_sel, self.palette)

            # 3. Right Inspector Card (Thumbnail + Info)
            card_x = self.window_w - 306
            card_y = 68
            card_w = 282
            card_h = 492
            insp_rect = pygame.Rect(card_x, card_y, card_w, card_h)
            pygame.draw.rect(self.screen, self.palette["card_bg"], insp_rect, border_radius=8)
            pygame.draw.rect(self.screen, self.palette["border"], insp_rect, 1, border_radius=8)

            insp_head = self.font_h2.render("GRID & ALGORITHM INSPECTOR", True, self.palette["accent"])
            self.screen.blit(insp_head, (card_x + 14, card_y + 12))

            pv_box = pygame.Rect(card_x + 14, card_y + 34, card_w - 28, 178)
            pygame.draw.rect(self.screen, self.palette["card_inner"], pv_box, border_radius=6)
            pygame.draw.rect(self.screen, self.palette["border"], pv_box, 1, border_radius=6)

            if self.cached_preview_surf:
                px = pv_box.x + (pv_box.width - self.cached_preview_surf.get_width()) // 2
                py = pv_box.y + (pv_box.height - self.cached_preview_surf.get_height()) // 2
                self.screen.blit(self.cached_preview_surf, (px, py))

            # Maze metadata
            cur_y = card_y + 222
            m = self.cached_maze_obj
            if m:
                info_lines = [
                    ("Maze File:", os.path.basename(self.cached_maze_path)),
                    ("Dimensions:", f"{m.rows} x {m.cols} cells"),
                    ("Start Node:", f"Row {m.start[0]}, Col {m.start[1]}" if m.start else "None"),
                    ("Goal Node:", f"Row {m.goal[0]}, Col {m.goal[1]}" if m.goal else "None"),
                ]
                for lbl, val in info_lines:
                    l_surf = self.font_body.render(lbl, True, self.palette["text_muted"])
                    v_surf = render_fitted_text(self.font_mono, val, 140, self.palette["text_primary"])
                    self.screen.blit(l_surf, (card_x + 14, cur_y))
                    self.screen.blit(v_surf, (card_x + 110, cur_y))
                    cur_y += 20

            pygame.draw.line(self.screen, self.palette["border"], (card_x + 14, cur_y + 4), (card_x + card_w - 14, cur_y + 4), 1)
            cur_y += 12

            algo_info = {
                "bfs": ("Breadth-First Search", "Uninformed", "O(b^d)", "Guaranteed"),
                "dfs": ("Depth-First Search", "Uninformed", "O(b*m)", "Not Shortest"),
                "dls": ("Depth-Limited Search", "Bounded", "O(b*L)", "Pruned at L"),
                "iddfs": ("Iterative Deepening", "Optimal", "O(b*d)", "Guaranteed"),
                "astar": ("A* (Heuristic)", "Informed", "O(b^d)", "Guaranteed"),
            }
            aname, atype, amem, aopt = algo_info.get(self.selected_algo, ("Search", "--", "--", "--"))

            prop_lines = [
                ("Algorithm:", aname),
                ("Search Type:", atype),
                ("Memory / Space:", amem),
                ("Optimality:", aopt),
            ]
            for lbl, val in prop_lines:
                l_surf = self.font_body.render(lbl, True, self.palette["text_muted"])
                v_surf = render_fitted_text(self.font_mono, val, 140, self.palette["accent_text"])
                self.screen.blit(l_surf, (card_x + 14, cur_y))
                self.screen.blit(v_surf, (card_x + 110, cur_y))
                cur_y += 20

            # 4. Bottom Action Footer Bar
            footer_rect = pygame.Rect(0, self.window_h - 70, self.window_w, 70)
            pygame.draw.rect(self.screen, self.palette["card_bg"], footer_rect)
            pygame.draw.line(self.screen, self.palette["border"], (0, self.window_h - 70), (self.window_w, self.window_h - 70), 1)

            stat_lbl = self.font_small.render("STATUS", True, self.palette["accent"])
            self.screen.blit(stat_lbl, (24, self.window_h - 52))

            msg_surf = render_fitted_text(self.font_body, self.status_msg, self.window_w - 340, self.palette["text_primary"])
            self.screen.blit(msg_surf, (24, self.window_h - 34))

            # Action Launch Button
            act_col = self.palette["action_hover"] if action_hovered else self.palette["action_bg"]
            pygame.draw.rect(self.screen, act_col, self.action_rect, border_radius=6)

            action_labels = {
                "visual": "START VISUAL SOLVER",
                "split": "LAUNCH SPLIT-VIEW",
                "compare": "RUN 5-WAY BENCHMARK",
                "edit": "OPEN MAZE EDITOR",
            }
            btn_txt = action_labels.get(self.selected_mode, "LAUNCH")
            act_surf = self.font_action.render(btn_txt, True, (255, 255, 255))
            ax = self.action_rect.x + (self.action_rect.width - act_surf.get_width()) // 2
            ay = self.action_rect.y + (self.action_rect.height - act_surf.get_height()) // 2
            self.screen.blit(act_surf, (ax, ay))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def _execute_action(self):
        try:
            cfg = Config.get()
            cfg.set("sound_enabled", self.sound_enabled)
            cfg.set("steps_per_frame", self.anim_speed)

            # resolve maze path
            if self.selected_maze == "GENERATE":
                gen_dir = os.path.join(PROJECT_ROOT, "data", "generated")
                os.makedirs(gen_dir, exist_ok=True)
                gen_file = os.path.join(gen_dir, f"procedural_{self.gen_algo}_{self.gen_size}x{self.gen_size}.txt")
                if self.gen_algo == "prims":
                    gen = PrimsGenerator(self.gen_size, self.gen_size)
                else:
                    gen = RecursiveBacktrackGenerator(self.gen_size, self.gen_size)
                gen.generate()
                gen.save(gen_file)
                maze_path = gen_file
            else:
                maze_path = os.path.join(PROJECT_ROOT, "data", self.selected_maze)
                if not os.path.exists(maze_path):
                    maze_path = os.path.join(PROJECT_ROOT, "data", "maze_20x20.txt")

            maze = Maze(maze_path)

            if self.selected_mode == "edit":
                editor = MazeEditor(rows=maze.rows, cols=maze.cols, theme_name=self.selected_theme)
                editor.run()
                self._restore_display()
                return

            if self.selected_mode == "split":
                bfs_res = BFSSolver(maze).solve()
                dfs_res = DFSSolver(maze).solve()
                dls_res = DLSSolver(maze, limit=self.dls_limit).solve()
                renderer = SplitRenderer(
                    maze,
                    {"bfs": bfs_res, "dfs": dfs_res, "dls": dls_res},
                    theme_name=self.selected_theme,
                )
                renderer.run()
                self._restore_display()
                return

            if self.selected_mode == "compare":
                from src.main import print_comparison, append_to_log
                bfs_res = BFSSolver(maze).solve()
                dfs_res = DFSSolver(maze).solve()
                dls_res = DLSSolver(maze, limit=self.dls_limit).solve()
                iddfs_res = IDDFSSolver(maze).solve()
                astar_res = AStarSolver(maze).solve()

                algo_names = ["BFS", "DFS", f"DLS (L={self.dls_limit})", "IDDFS", "A* (Heuristic)"]
                results = [bfs_res, dfs_res, dls_res, iddfs_res, astar_res]
                print_comparison(results, algo_names)
                for n, r in zip(algo_names, results):
                    append_to_log(n, maze_path, r)
                self.status_msg = f"Benchmark complete! Metrics logged to output/results_log.txt"
                return

            # Visual mode
            if self.selected_algo == "dls":
                solver = DLSSolver(maze, limit=self.dls_limit)
                name = f"DLS (L={self.dls_limit})"
            elif self.selected_algo == "dfs":
                solver = DFSSolver(maze)
                name = "DFS"
            elif self.selected_algo == "iddfs":
                solver = IDDFSSolver(maze)
                name = "IDDFS"
            elif self.selected_algo == "astar":
                solver = AStarSolver(maze)
                name = "A*"
            else:
                solver = BFSSolver(maze)
                name = "BFS"

            res = solver.solve()
            self.status_msg = f"Solved {os.path.basename(maze_path)}: Path={res['path_length']} steps | Explored={res['nodes_explored']} nodes ({res['time_taken']*1000:.2f}ms)"

            renderer = Renderer(maze, res, name, theme_name=self.selected_theme)
            renderer.run()
            self._restore_display()
        except Exception as e:
            self.status_msg = f"Runtime error: {e}"
            self._restore_display()

if __name__ == "__main__":
    launcher = LauncherGUI()
    launcher.run()
