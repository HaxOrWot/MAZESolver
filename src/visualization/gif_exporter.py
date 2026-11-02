import os
import pygame
from PIL import Image

class GIFExporter:
    def __init__(self, skip_frames=3, fps=15):
        self.frames = []
        self.skip_frames = max(1, skip_frames)
        self.frame_count = 0
        self.fps = fps

    def capture(self, screen):
        # captures frame every N ticks so the gif file isn't huge
        if self.frame_count % self.skip_frames == 0:
            raw = pygame.image.tostring(screen, "RGB")
            size = screen.get_size()
            img = Image.frombytes("RGB", size, raw)
            self.frames.append(img)
        self.frame_count += 1

    def export(self, filepath: str):
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
        print(f"[GIF] Saved animated GIF ({len(self.frames)} frames) -> {filepath}")
