"""
Tests for Config singleton (src/config.py)
"""
from src.config import Config


def test_config_loads_defaults():
    cfg = Config.get()
    assert cfg.theme in ["dark", "neon", "retro", "light"]
    assert cfg.animation_fps > 0
    assert cfg.steps_per_frame > 0
    assert cfg.hud_width >= 200


def test_config_set_and_get():
    cfg = Config.get()
    old_theme = cfg.theme
    cfg.set("theme", "neon")
    assert cfg.theme == "neon"
    cfg.set("theme", old_theme)
