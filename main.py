import flet as ft
import sqlite3, os
from PIL import Image, ImageDraw

DB_PATH = "/storage/emulated/0/my_tracker.db"
OUT_PATH = "/storage/emulated/0/Pictures/tracker_stats.jpg"

def make_stats_image():
    #... your same function...
    W, H = 1080, 1350
    img = Image.new('RGB', (W, H), '#0f0f0f')
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,W,200], fill='#1a1a1a')
    d.text((50, 50), f"TEST", fill="white")
    img.save(OUT_PATH)
    return OUT_PATH

def main(page: ft.Page):
    page.title = "Offline Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    status = ft.Text("Ready")
    def on_click(e):
        path = make_stats_image()
        status.value = f"Saved to {path}"
        page.update()
    page.add(
        ft.Column([
            ft.Button("Generate stats pic", on_click=on_click, width=300, height=50),
            status
        ])
    )

ft.run(main) # NOT ft.app
