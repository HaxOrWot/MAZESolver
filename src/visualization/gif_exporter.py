"""
MAZESolver — Animated GIF Exporter
==================================
Captures Pygame display frames and encodes them into smooth animated GIFs using Pillow.
"""
import io
import os
import pygame
from PIL import Image
from typing import List


class GIFExporter:
    def __init__(self, skip_frames: int = 3, fps: int = 15):
        self.frames: List[Image.Image] = []
        self.skip_frames = max(1, skip_frames)
        self.frame_count = 0
        self.fps = fps

    def capture(self, screen: pygame.Surface) -> None:
        """Call every frame. Captures every Nth frame to avoid massive files."""
        if self.frame_count % self.skip_frames == 0:
            raw = pygame.image.tostring(screen, "RGB")
            size = screen.get_size()
            img = Image.frombytes("RGB", size, raw)
            self.frames.append(img)
        self.frame_count += 1

    def export(self, filepath: str) -> None:
        """Encodes and saves the captured frames as an animated GIF."""
        if not self.frames:
            return
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        duration = max(20, int(1000 / self.fps))
        self.frames[0].save(
            filepath,
            save_all=True,
            append_images=self.frames[1:],
            duration=duration,
            loop=0,
            optimize=True,
        )
        print(f"[GIF] Exported {len(self.frames)} frames to {filepath}")
