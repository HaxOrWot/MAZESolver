import os
import pygame

import sys

if getattr(sys, "frozen", False):
    PROJECT_ROOT = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
else:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SoundManager:
    def __init__(self, enabled=True, volume=0.3):
        self.enabled = enabled
        self.volume = volume
        self.tick_sound = None
        self.goal_sound = None

        if self.enabled:
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                self._load_sounds()
                self.set_volume(self.volume)
            except Exception:
                self.enabled = False

    def _load_sounds(self):
        sounds_dir = os.path.join(PROJECT_ROOT, "assets", "sounds")
        tick_file = os.path.join(sounds_dir, "tick.wav")
        goal_file = os.path.join(sounds_dir, "goal.wav")

        try:
            if os.path.exists(tick_file):
                self.tick_sound = pygame.mixer.Sound(tick_file)
            if os.path.exists(goal_file):
                self.goal_sound = pygame.mixer.Sound(goal_file)
        except Exception:
            pass

    def set_volume(self, vol: float):
        self.volume = max(0.0, min(1.0, vol))
        if self.tick_sound:
            self.tick_sound.set_volume(self.volume * 0.4)
        if self.goal_sound:
            self.goal_sound.set_volume(self.volume)

    def toggle_mute(self):
        self.enabled = not self.enabled
        return self.enabled

    def play_tick(self):
        if self.enabled and self.tick_sound:
            try:
                self.tick_sound.play()
            except Exception:
                pass

    def play_goal(self):
        if self.enabled and self.goal_sound:
            try:
                self.goal_sound.play()
            except Exception:
                pass
