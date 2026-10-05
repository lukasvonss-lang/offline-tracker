import flet as ft
import sqlite3, os, time
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

DB_PATH = "/storage/emulated/0/my_tracker.db" # your tracker db from earlier
OUT_PATH = "/storage/emulated/0/Pictures/tracker_stats.jpg"

def make_stats_image():
    db = sqlite3.connect(DB_PATH)
    total_secs = db.execute("SELECT SUM(duration) FROM plays").fetchone()[0] or 0
    total_mins = total_secs / 60

    top = db.execute("SELECT artist, title, COUNT(*), SUM(duration) FROM plays GROUP BY artist, title ORDER BY SUM(duration) DESC LIMIT 5").fetchall()

    # make image
    W, H = 1080, 1350
    img = Image.new('RGB', (W, H), '#0f0f0f')
    d = ImageDraw.Draw(img)

    # use default font, no need to load ttf (works on Android)
    d.rectangle([0,0,W,200], fill='#1a1a1a')
    d.text((50, 50), f"{total_mins:.0f} MINUTES", fill="white")
    d.text((50, 110), f"{len(top)} unique tracks", fill="#888")

    y = 250
    for artist, title, plays, secs in top:
        mins = secs/60
        d.text((50, y), f"{artist} - {title}", fill="white")
        d.text((50, y+45), f"{plays} plays • {mins:.1f} min", fill="#666")
        y += 120

    img.save(OUT_PATH)
    return OUT_PATH

def main(page: ft.Page):
    page.title = "Offline Tracker"
    def on_click(e):
        path = make_stats_image()
        page.add(ft.Text(f"Saved to {path}"))

    page.add(ft.ElevatedButton("Generate stats pic", on_click=on_click))

ft.app(target=main)
