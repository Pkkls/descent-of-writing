# -*- coding: utf-8 -*-
"""SVG -> PNG through the Chrome already installed on this machine.

cairosvg needs a libcairo DLL that is not present on Windows, and pulling a
rasterizer binary off the internet to render a local file is not worth it.
"""
import os, sys, subprocess, tempfile, shutil

CHROME = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
          r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]


def find_browser():
    for p in CHROME:
        if os.path.exists(p):
            return p
    raise SystemExit("no Chrome or Edge found")


def render(svg_path, png_path, width, height, scale=1, crop=None):
    """crop = (full_w, full_h, x, y, w, h): draw the SVG at full_w x full_h and
    screenshot the w x h window at (x, y). Used to check the plate at 1:1."""
    src = "file:///" + svg_path.replace("\\", "/")
    if crop:
        fw, fh, cx, cy, cw, ch = crop
        html = ('<!doctype html><meta charset="utf-8">'
                '<style>html,body{margin:0;padding:0;background:#fff;overflow:hidden}'
                'img{position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx}</style>'
                '<img src="%s">' % (-cx, -cy, fw, fh, src))
        width, height = cw, ch
    else:
        html = ('<!doctype html><meta charset="utf-8">'
                '<style>html,body{margin:0;padding:0;background:#fff}'
                'img{display:block;width:%dpx;height:%dpx}</style>'
                '<img src="%s">' % (width, height, src))
    tmp = tempfile.mkdtemp(prefix="raster_")
    hp = os.path.join(tmp, "page.html")
    open(hp, "w", encoding="utf8").write(html)
    cmd = [find_browser(), "--headless", "--disable-gpu", "--no-sandbox",
           "--hide-scrollbars", "--force-device-scale-factor=%g" % scale,
           "--virtual-time-budget=20000",
           "--window-size=%d,%d" % (width, height),
           "--screenshot=" + png_path, "file:///" + hp.replace("\\", "/")]
    r = subprocess.run(cmd, capture_output=True, timeout=600)
    shutil.rmtree(tmp, ignore_errors=True)
    if not os.path.exists(png_path):
        raise SystemExit("render failed: %s" % r.stderr.decode("utf8", "replace")[-500:])
    return os.path.getsize(png_path)


if __name__ == "__main__":
    svg, png, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    print("%s  %d bytes" % (png, render(os.path.abspath(svg), os.path.abspath(png), w, h)))
