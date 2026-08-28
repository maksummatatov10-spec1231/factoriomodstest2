#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерирует thumbnail.png (512x512) для мода fish-furnace: тёмный фон с
текстурой, печка по центру, лёгкое свечение. Полностью кодом."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

ROOT = "/home/user/factoriomodstest2"
MOD = os.path.join(ROOT, "mods", "fish-furnace")
icon = Image.open(os.path.join(MOD, "graphics", "icons", "fish-furnace.png")).convert("RGBA")

SIZE = 512
# фон: вертикальный градиент тёмно-серый + шум
w, h = SIZE, SIZE
arr = np.zeros((h, w, 3), dtype=np.uint8)
t = np.linspace(0, 1, h)[:, None]
top = np.array([46, 52, 62]); bot = np.array([24, 28, 34])
for c in range(3):
    arr[..., c] = (top[c] + (bot[c] - top[c]) * t).astype(np.uint8)
# мягкий шум
rng = np.random.default_rng(7)
noise = rng.normal(0, 6, (h, w, 1))
arr = np.clip(arr.astype(np.float64) + noise, 0, 255).astype(np.uint8)
bg = Image.fromarray(arr, "RGB").convert("RGBA")

# виньетка
yy, xx = np.mgrid[0:h, 0:w]
d = np.sqrt(((xx - w / 2) / (w * 0.55)) ** 2 + ((yy - h / 2) / (h * 0.55)) ** 2)
vin = np.clip(1 - d, 0, 1) ** 1.4
dark = Image.new("RGBA", (w, h), (0, 0, 0, 0))
dark_arr = np.zeros((h, w, 4), dtype=np.uint8)
dark_arr[..., 3] = ((1 - vin) * 120).astype(np.uint8)
dark = Image.fromarray(dark_arr, "RGBA")
bg = Image.alpha_composite(bg, dark)

# печка — крупная версия: реконструируем из body sheet
body = Image.open(os.path.join(MOD, "graphics", "entity", "fish-furnace", "fish-furnace.png"))
frame = body.crop((0, 0, 302, 292))
scale = 1.35
frame = frame.resize((int(302 * scale), int(292 * scale)), Image.LANCZOS)

# лёгкое свечение снизу
glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([w * 0.28, h * 0.55, w * 0.72, h * 0.92], fill=(255, 140, 40, 90))
glow = glow.filter(ImageFilter.GaussianBlur(40))
bg = Image.alpha_composite(bg, glow)

frame = ImageEnhance.Brightness(frame).enhance(1.02)
bg.alpha_composite(frame, (w // 2 - frame.width // 2, h // 2 - frame.height // 2 - 8))
bg.convert("RGB").save(os.path.join(MOD, "thumbnails", "thumbnail.png"))
print("thumbnail ok")
