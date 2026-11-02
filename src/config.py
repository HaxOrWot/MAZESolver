import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")

# configuration manager
class Config:
    _instance = None

    def __init__(self):
        if not os.path.exists(CONFIG_PATH):
            self._data = {
                "theme": "dark",
                "animation_fps": 60,
                "steps_per_frame": 3,
                "sound_enabled": True,
                "sound_volume": 0.3,
                "cell_size_override": None,
                "hud_width": 280,
                "hud_default_tab": 1,
                "gif_fps": 15,
                "gif_skip_frames": 3,
                "default_dls_limit_multiplier": 1.5,
                "particle_count": 40,
                "particle_gravity": 0.15,
                "glow_radius": 3,
                "fade_frames": 8,
            }
            self.save()
        else:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                self._data = json.load(f)

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = Config()
        return cls._instance

    def __getattr__(self, key):
        return self._data.get(key)

    def get_val(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value

    def save(self):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)
