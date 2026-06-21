#!/usr/bin/env python3
# Genere icon-192.png et icon-512.png (PWA, maskable) sans dependance externe.
import zlib, struct, math, os

OUT = os.path.dirname(os.path.abspath(__file__))

def make_icon(N, path):
    buf = bytearray()
    cx = cy = N / 2.0
    head_r = 0.30 * N
    eye_r  = 0.055 * N
    eye_dx = 0.115 * N
    eye_dy = 0.06 * N

    def incirc(x, y, ox, oy, r):
        return (x - ox) ** 2 + (y - oy) ** 2 <= r * r

    for y in range(N):
        buf.append(0)  # filter type 0 par scanline
        for x in range(N):
            t = y / N
            r = int(15 + 12 * t); g = int(20 + 14 * t); b = int(40 + 22 * t)  # fond degrade
            d = math.hypot(x - cx, y - cy)
            if d <= head_r:                                   # tete zombie
                r, g, b = 124, 252, 77
                if d > head_r * 0.84:                          # contour
                    r, g, b = 86, 196, 52
                if incirc(x, y, cx - eye_dx, cy - eye_dy, eye_r) or \
                   incirc(x, y, cx + eye_dx, cy - eye_dy, eye_r):   # yeux
                    r, g, b = 16, 24, 15
                if abs(y - (cy + 0.13 * N)) < 0.018 * N and abs(x - cx) < 0.16 * N:  # bouche
                    r, g, b = 16, 24, 15
                for sx in (-0.09, 0.0, 0.09):                  # points de suture
                    if abs(x - (cx + sx * N)) < 0.012 * N and abs(y - (cy + 0.13 * N)) < 0.05 * N:
                        r, g, b = 16, 24, 15
            buf.extend((r, g, b, 255))

    raw = bytes(buf)
    comp = zlib.compress(raw, 9)

    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data +
                struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", N, N, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    print("ecrit", path, len(png), "octets")

make_icon(192, os.path.join(OUT, "icon-192.png"))
make_icon(512, os.path.join(OUT, "icon-512.png"))
