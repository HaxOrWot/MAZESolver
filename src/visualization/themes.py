# theme color palettes for pygame

THEMES = {
    "dark": {
        "bg": (18, 18, 18),
        "wall": (40, 40, 40),
        "open": (230, 230, 230),
        "start": (0, 200, 83),
        "goal": (213, 0, 0),
        "visited_cold": (30, 100, 200),
        "visited_hot": (255, 100, 0),
        "path": (255, 214, 0),
        "frontier": (255, 100, 0),
        "glow": (255, 214, 0),
        "hud_bg": (12, 12, 12),
        "hud_text": (210, 210, 210),
        "hud_accent": (100, 181, 246),
        "hud_divider": (50, 50, 50),
        "hud_success": (0, 200, 83),
        "hud_fail": (213, 0, 0),
        "hud_searching": (255, 214, 0),
        "border": (60, 60, 60),
    },
    "neon": {
        "bg": (5, 5, 15),
        "wall": (20, 20, 40),
        "open": (15, 15, 35),
        "start": (0, 255, 150),
        "goal": (255, 0, 100),
        "visited_cold": (0, 120, 255),
        "visited_hot": (200, 0, 255),
        "path": (0, 255, 200),
        "frontier": (255, 255, 0),
        "glow": (100, 0, 255),
        "hud_bg": (3, 3, 10),
        "hud_text": (200, 200, 255),
        "hud_accent": (0, 255, 200),
        "hud_divider": (30, 30, 70),
        "hud_success": (0, 255, 150),
        "hud_fail": (255, 0, 100),
        "hud_searching": (255, 255, 0),
        "border": (40, 40, 100),
    },
    "retro": {
        "bg": (10, 20, 5),
        "wall": (0, 60, 0),
        "open": (0, 180, 0),
        "start": (255, 255, 0),
        "goal": (255, 80, 0),
        "visited_cold": (0, 100, 0),
        "visited_hot": (100, 255, 0),
        "path": (255, 200, 0),
        "frontier": (200, 255, 0),
        "glow": (0, 255, 0),
        "hud_bg": (5, 10, 3),
        "hud_text": (0, 200, 0),
        "hud_accent": (0, 255, 0),
        "hud_divider": (0, 50, 0),
        "hud_success": (0, 255, 0),
        "hud_fail": (255, 80, 0),
        "hud_searching": (100, 255, 0),
        "border": (0, 80, 0),
    },
    "light": {
        "bg": (245, 245, 245),
        "wall": (60, 60, 60),
        "open": (255, 255, 255),
        "start": (0, 150, 60),
        "goal": (180, 0, 0),
        "visited_cold": (150, 200, 255),
        "visited_hot": (255, 150, 80),
        "path": (255, 200, 0),
        "frontier": (255, 120, 0),
        "glow": (255, 200, 0),
        "hud_bg": (235, 235, 235),
        "hud_text": (30, 30, 30),
        "hud_accent": (30, 100, 200),
        "hud_divider": (200, 200, 200),
        "hud_success": (0, 150, 60),
        "hud_fail": (180, 0, 0),
        "hud_searching": (200, 120, 0),
        "border": (180, 180, 180),
    },
}

THEME_ORDER = ["dark", "neon", "retro", "light"]

def get_theme(name: str):
    return THEMES.get(name.lower(), THEMES["dark"])

def next_theme(current: str):
    cur = current.lower()
    idx = THEME_ORDER.index(cur) if cur in THEME_ORDER else 0
    return THEME_ORDER[(idx + 1) % len(THEME_ORDER)]
