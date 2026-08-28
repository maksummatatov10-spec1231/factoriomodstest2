#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fish-furnace v2 — полностью программная генерация спрайтов (без AI-генераторов).
Форма повторяет ванильную каменную печку: трапециевидный фасад, скошенная крыша,
боковая грань, арочная топка, металлическая окантовка. Вместо кирпича — рыбья
чешуя, глаза как у рыбы, плавники по бокам и на крыше. 48 кадров пламени на
основе value-noise, аддитивное свечение, тень, останки, иконки.

Масштаб: 2x (в игре scale = 0.5), тайл = 32 px. Итог: 302x292 == ванильные 151x146*2.
"""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "mods", "fish-furnace", "graphics", "entity", "fish-furnace")
ICON = os.path.join(ROOT, "mods", "fish-furnace", "graphics", "icons")
ART = os.path.join(ROOT, "art", "fish-furnace")
os.makedirs(os.path.join(OUT, "remnants"), exist_ok=True)
os.makedirs(ICON, exist_ok=True)
os.makedirs(ART, exist_ok=True)

S = 2  # 2x resolution
W, H = 151 * S, 146 * S  # 302 x 292

# ---------------------------------------------------------------- палитра (в духе ванилы, низкая насыщенность)
TEAL       = (58, 128, 138)    # тело
TEAL_LIGHT = (110, 178, 186)
TEAL_DARK  = (28, 74, 84)
TEAL_DEEP  = (14, 42, 50)
TEAL_SHAD  = (34, 88, 96)
COPPER     = (170, 118, 62)
COPPER_DK  = (110, 72, 38)
COPPER_LT  = (222, 172, 104)
STEEL      = (94, 100, 110)
STEEL_DK   = (48, 52, 60)
STEEL_LT   = (158, 164, 174)
INK        = (18, 20, 24)
INK_SOFT   = (34, 38, 44)
BONE       = (225, 220, 206)
EYE_IRIS   = (18, 34, 52)
FIRE_CORE  = (255, 238, 160)
FIRE_MID   = (255, 150, 40)
FIRE_EDGE  = (200, 58, 16)
SEED = 20260828
rng = random.Random(SEED)

# ---------------------------------------------------------------- шум
def _hash(ix, iy, seed):
    h = (ix * 374761393 + iy * 668265263 + seed * 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFFFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFFFFFF) / 0xFFFFFFFF

def value_noise(w, h, seed, scale=8.0):
    gx = max(2, int(w / scale) + 2); gy = max(2, int(h / scale) + 2)
    grid = np.array([[_hash(ix, iy, seed) for ix in range(gx)] for iy in range(gy)], dtype=np.float64)
    xs = np.linspace(0, gx - 1, w, endpoint=False)
    ys = np.linspace(0, gy - 1, h, endpoint=False)
    x0 = np.floor(xs).astype(int); y0 = np.floor(ys).astype(int)
    fx = xs - x0; fy = ys - y0
    fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy)
    v00 = grid[np.ix_(y0 % gy, x0 % gx)]; v10 = grid[np.ix_(y0 % gy, (x0 + 1) % gx)]
    v01 = grid[np.ix_((y0 + 1) % gy, x0 % gx)]; v11 = grid[np.ix_((y0 + 1) % gy, (x0 + 1) % gx)]
    a = v00 * (1 - fx) + v10 * fx
    b = v01 * (1 - fx) + v11 * fx
    return a * (1 - fy[:, None]) + b * fy[:, None]

def fbm(w, h, seed, octaves=4, scale=10.0):
    out = np.zeros((h, w), dtype=np.float64); amp = 1.0; total = 0.0; sc = scale
    for o in range(octaves):
        out += amp * value_noise(w, h, seed + o * 97, sc)
        total += amp; amp *= 0.5; sc *= 0.55
    return out / total

def radial_light(w, h, cx, cy, rx, ry, color, inner=1.0, outer=0.0, soft=1.0):
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    a = np.clip((1.0 - d), 0, 1) ** soft
    a = inner + (outer - inner) * (1.0 - np.clip(1.0 - d, 0, 1))
    a = np.clip(a, 0, 1)
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[..., 0], arr[..., 1], arr[..., 2] = color
    arr[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")

def make_gradient(w, h, top, bottom):
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    t = np.linspace(0, 1, h)[:, None]
    for c in range(3):
        arr[..., c] = (top[c] + (bottom[c] - top[c]) * t).astype(np.uint8)
    arr[..., 3] = 255
    return Image.fromarray(arr, "RGBA")

def vgrad_paste(img, x, y, w, h, top, bottom):
    g = make_gradient(w, h, top, bottom)
    img.paste(g, (x, y))

# ---------------------------------------------------------------- маски (геометрия как у ванильной печки)
# координаты в 1x, умножаем на S
def P(pts): return [(x * S, y * S) for x, y in pts]

FRONT = P([(26, 62), (125, 62), (139, 138), (12, 138)])          # трапеция фасада
SIDE  = P([(12, 138), (26, 62), (18, 52), (4, 128)])             # левая грань
ROOF  = P([(26, 62), (125, 62), (116, 24), (35, 24)])            # крыша-трапеция
POLY_FRONT, POLY_SIDE, POLY_ROOF = FRONT, SIDE, ROOF

def poly_mask(poly, w=W, h=H):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    return np.array(m) > 0

M_FRONT = poly_mask(POLY_FRONT)
M_SIDE  = poly_mask(POLY_SIDE)
M_ROOF  = poly_mask(POLY_ROOF)

def apply_mask(img, mask, color=None):
    arr = np.array(img)
    arr[..., 3] = np.where(mask, arr[..., 3], 0)
    if color:
        arr[..., 0], arr[..., 1], arr[..., 2] = color
    return Image.fromarray(arr)

# ---------------------------------------------------------------- чешуя
def draw_scales(img, mask, x0, y0, x1, y1, r, seed=1, palette=None, outline=True,
                base_top=None, base_bottom=None):
    """Пластины чешуи в шахматном порядке. Рисуем в ОТДЕЛЬНОМ слое,
    обрезаем по маске и накладываем на img (не разрушая остальное)."""
    base_top = base_top or TEAL
    base_bottom = base_bottom or TEAL_DEEP
    w, h = x1 - x0, y1 - y0
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # базовая заливка с затенением
    vgrad_paste(layer, x0, y0, w, h, base_top, base_bottom)
    # шумовая текстура грязи
    nz = fbm(W, H, seed * 3 + 11, octaves=3, scale=12.0)
    noise_arr = np.array(layer)
    for c in range(3):
        noise_arr[..., c] = np.clip(noise_arr[..., c] * (0.80 + 0.40 * nz), 0, 255)
    layer = Image.fromarray(noise_arr).filter(ImageFilter.GaussianBlur(1.0))
    # лёгкое затенение краёв грани (объём)
    edge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ed = ImageDraw.Draw(edge)
    ed.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill=(0, 0, 0, 70))
    edge = edge.filter(ImageFilter.GaussianBlur(14))
    layer = Image.alpha_composite(layer, edge)
    layer = apply_mask(layer, mask)

    rr = random.Random(seed)
    p = palette or (TEAL, TEAL_LIGHT, TEAL_DARK, COPPER)
    # строки-«ряды» чешуи
    row_h = r * 0.88
    rows = max(1, int((y1 - y0) / row_h) + 1)
    for row in range(rows):
        y = y0 + row * row_h
        off = (r * 0.7 if row % 2 else 0)
        x = x0 - r * 0.4 + off
        while x < x1 + r:
            cx, cy = x, y
            ew, eh = int(r * 2.05), int(r * 1.75)
            # цвет пластины с вариацией
            v = rr.random()
            c = p[0] if v < 0.6 else (p[1] if v < 0.85 else p[2])
            c = tuple(min(255, int(ch * (0.92 + 0.16 * rr.random()))) for ch in c)
            # тень под пластиной
            sub = Image.new("RGBA", (ew + 10, eh + 10), (0, 0, 0, 0))
            sd = ImageDraw.Draw(sub)
            sd.ellipse([2, 2, 2 + ew, 2 + int(eh * 0.85)], fill=INK_SOFT + (255,))
            sub = sub.filter(ImageFilter.GaussianBlur(1.4))
            layer.alpha_composite(sub, (int(cx - ew / 2 - 5), int(cy - eh * 0.45 - 5)))
            # сама пластина: вертикальный градиент + тёмная нижняя кромка-«арка»
            top = tuple(min(255, int(ch * 1.22 + 18)) for ch in c)
            bot = tuple(int(ch * 0.5) for ch in c)
            g = make_gradient(ew, eh, top, bot)
            shape = Image.new("RGBA", (ew, eh), (0, 0, 0, 0))
            sh_d = ImageDraw.Draw(shape)
            sh_d.ellipse([0, -int(eh * 0.62), ew - 1, int(eh * 1.05)], fill=(255, 255, 255, 255))
            scale_img = Image.new("RGBA", (ew, eh), (0, 0, 0, 0))
            scale_img.paste(g, (0, 0), shape.split()[3])
            sc_d = ImageDraw.Draw(scale_img)
            # медная кромка нижней дуги
            sc_d.arc([1, -int(eh * 0.62), ew - 2, int(eh * 1.02)], 200, 340,
                     fill=COPPER_LT + (235,), width=3)
            sc_d.line([(6, int(eh * 0.30)), (ew - 7, int(eh * 0.30))],
                      fill=(0, 0, 0, 46), width=2)
            if outline:
                sc_d.arc([1, -int(eh * 0.62), ew - 2, int(eh * 1.02)], 180, 360,
                         fill=INK + (170,), width=2)
            # блик сверху
            hl = Image.new("RGBA", (ew, eh), (0, 0, 0, 0))
            hd = ImageDraw.Draw(hl)
            hd.ellipse([int(ew * 0.25), -int(eh * 0.18), int(ew * 0.78), int(eh * 0.34)],
                       fill=(255, 255, 255, 42))
            hl = hl.filter(ImageFilter.GaussianBlur(1.6))
            scale_img = Image.alpha_composite(scale_img, hl)
            layer.alpha_composite(scale_img, (int(cx - ew / 2), int(cy - eh / 2)))
            x += r * 1.5
    img.alpha_composite(clip_to_mask(layer, mask))
    return img

def clip_to_mask(img, mask):
    arr = np.array(img)
    arr[..., 3] = np.where(mask, arr[..., 3], 0)
    return Image.fromarray(arr)

# ---------------------------------------------------------------- детали
def draw_steel_frame(img, x0, y0, x1, y1, thick=8, rivet=36):
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x1, y1], outline=STEEL_DK + (255,), width=thick)
    d.rectangle([x0 + thick, y0 + thick, x1 - thick, y1 - thick],
                outline=STEEL + (255,), width=3)
    for y in range(y0 + thick + 6, y1 - 2, rivet):
        for xx in (x0 + thick + 2, x1 - thick - 2):
            d.ellipse([xx - 4, y - 4, xx + 4, y + 4], fill=STEEL_LT + (255,),
                      outline=INK + (255,))
    # блик по верхнему краю
    d.line([(x0 + 4, y0 + 3), (x1 - 4, y0 + 3)], fill=STEEL_LT + (120,), width=2)

def draw_eye(img, cx, cy, r, blink=False):
    e = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
    d = ImageDraw.Draw(e)
    # выпуклое «кольцо» вокруг глаза — веко из чешуи
    d.ellipse([cx - r - 7, cy - r - 7, cx + r + 7, cy + r + 7],
              fill=TEAL_DARK + (255,), outline=INK + (255,), width=4)
    d.ellipse([cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4],
              fill=TEAL_SHAD + (255,))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BONE + (255,))
    if blink:
        # веко закрыто: полоса тела
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK + (255,), width=3)
        d.chord([cx - r, cy - r * 0.5, cx + r, cy + r * 1.4], 180, 360,
                fill=TEAL_DARK + (255,))
    else:
        d.ellipse([cx - r * 0.74, cy - r * 0.68, cx + r * 0.74, cy + r * 0.68],
                  fill=EYE_IRIS + (255,))
        d.ellipse([cx - r * 0.36, cy - r * 0.32, cx + r * 0.36, cy + r * 0.32],
                  fill=(6, 10, 14, 255))
        d.ellipse([cx - r * 0.55, cy - r * 0.52, cx - r * 0.18, cy - r * 0.16],
                  fill=(255, 255, 255, 240))
        d.ellipse([cx + r * 0.34, cy + r * 0.10, cx + r * 0.56, cy + r * 0.30],
                  fill=(255, 255, 255, 130))
    img.alpha_composite(e)

def draw_fin(img, cx, cy, size, angle=0, flip=False, color=None):
    color = color or TEAL
    f = Image.new("RGBA", (int(size * 2.6), int(size * 1.9)), (0, 0, 0, 0))
    d = ImageDraw.Draw(f)
    bx, by = f.width * 0.42, f.height * 0.82
    pts = [
        (bx, by),
        (bx - size * 1.30, by - size * 0.45),
        (bx - size * 0.85, by - size * 1.05),
        (bx - size * 0.20, by - size * 0.92),
        (bx + size * 0.45, by - size * 1.18),
        (bx + size * 1.22, by - size * 0.48),
    ]
    d.polygon(pts, fill=color + (255,), outline=TEAL_DEEP + (255,))
    # лучи плавника
    for i, (px, py) in enumerate(pts[1:]):
        d.line([(bx, by), (px, py)], fill=COPPER_DK + (200,), width=2)
    # затемнение у основания
    base = Image.new("RGBA", f.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(base)
    bd.ellipse([bx - size, by - size * 0.4, bx + size, by + size * 0.5],
               fill=TEAL_DARK + (90,))
    base = base.filter(ImageFilter.GaussianBlur(3))
    f = Image.alpha_composite(f, base)
    if flip: f = f.transpose(Image.FLIP_LEFT_RIGHT)
    if angle: f = f.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(f, (int(cx - f.width / 2), int(cy - f.height / 2)))

def draw_arch(img, x0, y0, x1, y1, inner=(14, 15, 17)):
    a = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
    d = ImageDraw.Draw(a)
    w = x1 - x0
    # каменная/медная рамка арочной топки
    d.rounded_rectangle([x0 - 12, y0 - 10, x1 + 12, y1 + 10], radius=w // 2 + 6,
                        fill=COPPER_DK + (255,), outline=INK + (255,), width=4)
    d.rounded_rectangle([x0 - 8, y0 - 7, x1 + 8, y1 + 7], radius=w // 2,
                        fill=COPPER + (255,), outline=INK_SOFT + (200,), width=2)
    # нутро
    d.rounded_rectangle([x0, y0, x1, y1], radius=w // 2, fill=inner + (255,))
    # колосники
    for i in range(5):
        x = x0 + 12 + i * (x1 - x0 - 24) / 4
        d.line([(x, y1 - 10), (x, y1 - 3)], fill=(70, 54, 44, 255), width=4)
    d.line([(x0 + 8, y1 - 9), (x1 - 8, y1 - 9)], fill=(52, 40, 34, 255), width=6)
    # тёмный переход внутрь сверху
    sh = Image.new("RGBA", (x1 - x0 + 20, y1 - y0 + 20), (0, 0, 0, 0))
    sdd = ImageDraw.Draw(sh)
    sdd.rounded_rectangle([0, 0, x1 - x0 + 20, y1 - y0 + 20], radius=w // 2 + 2,
                          fill=(0, 0, 0, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    a.alpha_composite(sh, (x0 - 10, y0 - 10))
    img.alpha_composite(a)

def draw_teeth(img, x0, y0, x1, y1):
    d = ImageDraw.Draw(img)
    n = 6
    for i in range(n):
        t = (i + 0.5) / n
        cx = x0 + (x1 - x0) * t
        # вершина арки
        dx2 = (x1 - x0) / 2
        rel = (cx - (x0 + x1) / 2) / dx2
        arc_y = y0 + (1 - math.sqrt(max(0.0, 1 - rel * rel))) * dx2 * 0.9
        d.polygon([(cx - 7, arc_y + 4), (cx + 7, arc_y + 4), (cx, arc_y + 22)],
                  fill=BONE + (245,), outline=INK_SOFT + (220,))
        d.line([(cx - 7, arc_y + 4), (cx, arc_y + 22)], fill=(200, 190, 170, 200), width=2)

# ---------------------------------------------------------------- сборка печки
def draw_furnace(blink=False):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # 1) левая боковая грань (тёмная)
    side = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vgrad_paste(side, 0, 0, W, H, (36, 84, 92), (22, 52, 60))
    side = apply_mask(side, M_SIDE)
    # шум на боку
    nz = fbm(W, H, 55, octaves=3, scale=14)
    arr = np.array(side)
    for c in range(3):
        arr[..., c] = np.clip(arr[..., c] * (0.85 + 0.3 * nz), 0, 255)
    side = Image.fromarray(arr)
    img.alpha_composite(side)

    # 2) крыша (светлее, с рядами чешуи)
    roof = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vgrad_paste(roof, 0, 0, W, H, (86, 156, 162), (48, 108, 116))
    roof = apply_mask(roof, M_ROOF)
    img.alpha_composite(roof)

    # 3) фасад — чешуя поверх градиента (сразу обрезаем по маске фасада)
    img = draw_scales(img, M_FRONT, 26 * S, 62 * S, 125 * S, 138 * S, r=13,
                      seed=SEED, base_top=(64, 136, 144), base_bottom=(22, 62, 72))

    # 4) крыша — более крупная чешуя
    img = draw_scales(img, M_ROOF, 35 * S, 24 * S, 116 * S, 62 * S, r=11,
                      seed=SEED + 5, base_top=(96, 166, 172), base_bottom=(46, 102, 110))

    # 5) металлическая окантовка фасада (как у печки)
    draw_steel_frame(img, 26 * S - 4, 126 * S, 126 * S + 4, 140 * S, thick=7)
    d = ImageDraw.Draw(img)
    # вертикальные стойки по краям фасада
    for xx in (26 * S, 125 * S):
        d.rectangle([xx - 5, 62 * S + 16, xx + 3, 132 * S], fill=STEEL_DK + (255,))
        d.rectangle([xx - 3, 62 * S + 18, xx + 1, 130 * S], fill=STEEL + (200,))
    # медная полоса по верху фасада (карниз)
    d.polygon([(26 * S, 62 * S), (125 * S, 62 * S), (121 * S, 70 * S),
               (30 * S, 70 * S)], fill=COPPER_DK + (255,), outline=INK + (255,))
    d.polygon([(28 * S, 63 * S), (123 * S, 63 * S), (120 * S, 68 * S),
               (31 * S, 68 * S)], fill=COPPER + (230,))
    # заклёпки на карнизе
    for xx in range(30 * S + 12, 122 * S, 26):
        d.ellipse([xx - 3, 63 * S + 1, xx + 3, 63 * S + 7], fill=COPPER_LT + (255,),
                  outline=INK + (200,))

    # 6) арочная топка-«пасть»
    ax0, ax1 = 54 * S, 97 * S
    ay0, ay1 = 96 * S, 138 * S
    draw_arch(img, ax0, ay0, ax1, ay1)
    draw_teeth(img, ax0 + 4, ay0 + 2, ax1 - 4, ay0 + 30)
    # тусклые угли (идл)
    for i in range(6):
        ux = ax0 + 26 + (ax1 - ax0 - 52) * (i / 5)
        uy = ay1 - 18 + 4 * math.sin(i * 1.9)
        d.ellipse([ux - 6, uy - 4, ux + 6, uy + 4], fill=(110, 34, 14, 255))
        d.ellipse([ux - 2, uy - 2, ux + 2, uy + 2], fill=FIRE_MID + (160,))

    # 7) рыбий глаз (крупные, на чешуе)
    draw_eye(img, 47 * S, 82 * S, 15, blink=blink)
    draw_eye(img, 104 * S, 82 * S, 15, blink=blink)

    # 8) плавники: брюшной левый, грудной правый, спинной на крыше
    draw_fin(img, 26 * S, 112 * S, 22, angle=10, flip=False, color=TEAL_SHAD)
    draw_fin(img, 126 * S, 105 * S, 20, angle=-8, flip=True, color=(70, 148, 156))
    draw_fin(img, 75.5 * S, 24 * S, 15, angle=0, color=(76, 152, 160))

    # 9) внешняя обводка корпуса
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(out)
    od.polygon(POLY_FRONT, outline=INK + (255,), width=5)
    od.polygon(POLY_SIDE, outline=INK + (255,), width=5)
    od.polygon(POLY_ROOF, outline=INK + (255,), width=5)
    img.alpha_composite(out)

    # 10) мягкая тень у основания фасада и подсветка сверху
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.polygon([(20 * S, 136 * S), (130 * S, 136 * S), (139 * S, 146 * S),
                (10 * S, 146 * S)], fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(4))
    img.alpha_composite(shadow)
    top_light = radial_light(W, H, W / 2, 40 * S, W * 0.55, 60 * S, (255, 255, 235),
                             inner=0.10, outer=0.0, soft=2.0)
    img = Image.alpha_composite(img, top_light)
    return img

# ---------------------------------------------------------------- пламя (48 кадров)
def make_fire_frame(idx, w=82, h=200):
    """Коническая колонна пламени: широкий низ, сужение кверху, изгиб от шума,
    бело-жёлтое ядро внизу, оранжевая середина, красные языки, искры."""
    seed = SEED + 991
    n = fbm(w, h, seed + idx * 13, octaves=4, scale=7.0)
    n2 = fbm(w, h, seed + idx * 7 + 3, octaves=3, scale=23.0)
    yy, xx = np.mgrid[0:h, 0:w]
    t = np.clip(yy / h, 0, 1)                    # 0 верх, 1 низ
    # извилистая центральная ось (сильнее вверху)
    wob = (n2[0] - 0.5) * 1.35 * (1 - t)
    cx = w / 2 + wob * w * 0.30
    # профиль ширины (sigma в долях ширины кадра): низ широкий ~0.40, верх ~0.12
    sigma = 0.12 + 0.29 * t ** 1.15
    dist = np.abs(xx - cx) / w
    body = np.exp(-0.5 * (dist / sigma) ** 2)
    # рваные языки пламени (шум)
    tongues = np.clip((n - 0.44) * 3.0, 0, 1) * (0.30 + 0.95 * (1 - t))
    flame = np.clip(body * (0.45 + 0.75 * tongues), 0, 1)
    # прозрачность: низ плотный, верх тает
    fade = np.clip((t - 0.10) / 0.75, 0, 1) ** 1.35
    a = np.clip(flame * (0.55 + 0.60 * fade), 0, 1)
    # температура по высоте: низ жарче
    heat = np.clip(1.10 - t * 1.0, 0, 1)           # 1 внизу
    # базовый цвет
    r = 255 * np.clip(0.80 + 0.20 * heat, 0, 1)
    g = 255 * np.clip(0.42 + 0.58 * heat ** 1.2, 0, 1)
    b = 255 * np.clip(0.10 + 0.60 * heat ** 2.4, 0, 1)
    # бело-жёлтое ядро
    core_amt = np.exp(-0.5 * (dist / (sigma * 0.45)) ** 2) * heat ** 1.3
    r = r + (255 - r) * core_amt
    g = g + (250 - g) * core_amt
    b = b + (215 - b) * core_amt
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[..., 0] = np.clip(r, 0, 255)
    arr[..., 1] = np.clip(g, 0, 255)
    arr[..., 2] = np.clip(b, 0, 255)
    arr[..., 3] = np.clip(a * 255, 0, 255)
    im = Image.fromarray(arr, "RGBA").filter(ImageFilter.GaussianBlur(1.0))
    # искры
    im2 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im2)
    rr = random.Random(seed + idx)
    for _ in range(6):
        sx = rr.uniform(w * 0.30, w * 0.70)
        sy = rr.uniform(h * 0.02, h * 0.50)
        sr = rr.randint(1, 3)
        col = (255, 205, 110, 230) if rr.random() < 0.7 else (255, 150, 60, 220)
        dd.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=col)
    return Image.alpha_composite(im, im2)

def make_glow_frame(idx, w=212, h=288):
    k = 0.78 + 0.22 * math.sin(idx * 0.55 + math.sin(idx * 0.21) * 2.4)
    return radial_light(w, h, w / 2, h * 0.60, w * 0.34, h * 0.34, FIRE_MID,
                        inner=0.9 * k, outer=0.0, soft=1.5)

# ---------------------------------------------------------------- останки
def make_remnant():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # рваная нижняя часть корпуса
    jag = [P(26, 62)] if False else None
    jag = [(26 * S, 138 * S), (30 * S, 112 * S), (44 * S, 120 * S), (58 * S, 106 * S),
           (72 * S, 122 * S), (86 * S, 108 * S), (100 * S, 120 * S),
           (114 * S, 106 * S), (125 * S, 114 * S), (139 * S, 138 * S)]
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(base)
    bd.polygon(jag, fill=(40, 42, 46, 255))
    img.alpha_composite(base)
    # обугленная чешуя на обломках
    sc = draw_scales(img, poly_mask(P([(26, 62), (125, 62), (139, 138), (12, 138)]) & 0,
                                    ) if False else M_FRONT, 26 * S, 106 * S,
                     125 * S, 138 * S, r=13, seed=SEED + 99,
                     palette=(TEAL_DARK, (44, 50, 54), (28, 32, 36), (66, 52, 40)),
                     base_top=(36, 42, 46), base_bottom=(16, 20, 24))
    # обрезаем только до jag — просто положим с маской низа
    low = Image.new("L", (W, H), 0)
    ImageDraw.Draw(low).polygon(jag, fill=255)
    sc = clip_to_mask(sc, np.array(low) > 0)
    img.alpha_composite(sc)
    # пустая пасть + глазницы (в пределах обломков)
    draw_arch(img, 54 * S, 112 * S, 97 * S, 140 * S, inner=(8, 8, 10))
    for cx in (47 * S, 104 * S):
        cy = 122 * S
        d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(10, 10, 12, 255),
                  outline=INK + (255,), width=3)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(26, 30, 36, 255))
    # трещины
    rr = random.Random(777)
    for _ in range(10):
        x = rr.randint(30 * S, 128 * S); y = rr.randint(112 * S, 136 * S)
        pts = [(x, y)]
        for _ in range(3):
            x += rr.randint(-20, 20); y += rr.randint(4, 14)
            pts.append((x, y))
        d.line(pts, fill=INK + (200,), width=2)
    # осколки чешуи и куски вокруг
    for i in range(22):
        ang = rr.random() * math.tau
        rad = rr.uniform(70, 150)
        px = int(75 * S + math.cos(ang) * rad)
        py = int(132 * S + math.sin(ang) * rad * 0.5)
        s = rr.randint(5, 14)
        c = (30, 66, 74) if rr.random() < 0.65 else (52, 46, 40)
        d.ellipse([px - s, py - s // 2, px + s, py + s // 2], fill=c + (235,),
                  outline=INK + (150,))
    for i in range(6):
        px = rr.randint(40 * S, 110 * S); py = rr.randint(120 * S, 140 * S)
        s = rr.randint(12, 26)
        d.polygon([(px, py), (px + s, py - s // 2), (px + s * 1.6, py), (px + s, py + s // 2)],
                  fill=(48, 52, 58, 255), outline=INK + (200,))
    d.line(jag, fill=INK + (255,), width=4)
    return img

# ---------------------------------------------------------------- тень/отражение
def make_shadow():
    w, h = 328, 148
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = [(34, 78), (98, 30), (262, 38), (300, 84), (232, 128), (60, 124)]
    d.polygon(pts, fill=(0, 0, 0, 130))
    img = img.filter(ImageFilter.GaussianBlur(8))
    d = ImageDraw.Draw(img)
    d.polygon([(56, 76), (108, 44), (252, 50), (272, 82), (210, 112), (70, 108)],
              fill=(0, 0, 0, 80))
    return img.filter(ImageFilter.GaussianBlur(6))

def make_reflection():
    im = radial_light(32, 32, 16, 16, 16, 10, (46, 120, 130), inner=0.5, outer=0.05)
    return im.resize((16, 16), Image.LANCZOS)

# ---------------------------------------------------------------- иконки
def make_icon(src):
    bbox = src.getbbox()
    crop = src.crop(bbox)
    scale = 120 / max(crop.size)
    crop = crop.resize((int(crop.width * scale), int(crop.height * scale)), Image.LANCZOS)
    ic = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    ic.paste(crop, (64 - crop.width // 2, 64 - crop.height // 2), crop)
    return ic

def main():
    print("== fish-furnace graphics v2 (полностью код) ==")
    a = draw_furnace(blink=False)
    a.save(os.path.join(OUT, "fish-furnace.png"))
    print("  body single frame", a.size)

    make_shadow().save(os.path.join(OUT, "fish-furnace-shadow.png"))
    fw, fh = 82, 200
    FCOL, FROW = 8, 6
    fire = Image.new("RGBA", (fw * FCOL, fh * FROW), (0, 0, 0, 0))
    glow = Image.new("RGBA", (212 * FCOL, 288 * FROW), (0, 0, 0, 0))
    for i in range(48):
        fr = make_fire_frame(i, fw, fh)
        fire.paste(fr, ((i % FCOL) * fw, (i // FCOL) * fh), fr)
        gf = make_glow_frame(i)
        glow.paste(gf, ((i % FCOL) * 212, (i // FCOL) * 288), gf)
    fire.save(os.path.join(OUT, "fish-furnace-fire.png"))
    glow.save(os.path.join(OUT, "fish-furnace-light.png"))
    print("  fire", fire.size, "glow", glow.size)

    make_glow_frame(0, 232, 220).save(os.path.join(OUT, "fish-furnace-ground-light.png"))
    make_remnant().save(os.path.join(OUT, "remnants", "fish-furnace-remnants.png"))
    make_reflection().save(os.path.join(OUT, "fish-furnace-reflection.png"))
    ic = make_icon(a)
    ic.save(os.path.join(ICON, "fish-furnace.png"))
    ic.save(os.path.join(ICON, "fish-furnace-tech.png"))
    print("  icons ok")

    # превью-анимация (gif) в art/
    frames = []
    gs = 0.5
    for i in range(24):
        fr = make_fire_frame(i * 2, fw, fh)
        base = a.copy()
        # вставляем пламя за топку (по центру)
        base.alpha_composite(fr, (75 * S - fw // 2, 96 * S - fh + 10))
        gl = make_glow_frame(i * 2, 212, 288)
        base.alpha_composite(gl, (int(W / 2 - 106), int(138 * S - 150)))
        base = base.resize((W // 2, H // 2), Image.LANCZOS)
        base.thumbnail((320, 320), Image.LANCZOS)
        bg = Image.new("RGB", (320, 320), (58, 62, 70))
        bg.paste(base, (160 - base.width // 2, 160 - base.height // 2), base)
        frames.append(bg)
    frames[0].save(os.path.join(ART, "preview.gif"), save_all=True,
                   append_images=frames[1:], duration=80, loop=0, optimize=True)
    print("  preview.gif saved")
    print("Готово.")

if __name__ == "__main__":
    main()
