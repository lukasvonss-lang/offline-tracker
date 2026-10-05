import flet as ft
import sqlite3, os, time
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

DB_PATH = "/storage/emulated/0/my_tracker.db"
OUT_PATH = "/storage/emulated/0/Pictures/tracker_stats.jpg"

def make_stats_image():
    try:
        db = sqlite3.connect(DB_PATH)
        total_secs = db.execute("SELECT SUM(duration) FROM plays").fetchone()[0] or 0
        total_mins = total_secs / 60
        top = db.execute("SELECT artist, title, COUNT(*), SUM(duration) FROM plays GROUP BY artist, title ORDER BY SUM(duration) DESC LIMIT 5").fetchall()
        db.close()
    except Exception as e:
        # if DB doesn't exist yet, fake data so app doesn't crash
        total_mins = 0
        top = [("No data yet", "Play some music", 0, 0)]

    W, H = 1080, 1350
    img = Image.new('RGB', (W, H), '#0f0f0f')
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,W,200], fill='#1a1a1a')
    d.text((50, 50), f"{total_mins:.0f} MINUTES", fill="white")
    d.text((50, 110), f"{len(top)} unique tracks", fill="#888")

    y = 250
    for artist, title, plays, secs in top:
        mins = (secs or 0)/60
        d.text((50, y), f"{artist} - {title}"[:40], fill="white")
        d.text((50, y+45), f"{plays} plays • {mins:.1f} min", fill="#666")
        y += 120

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    img.save(OUT_PATH)
    return OUT_PATH

def main(page: ft.Page):
    page.title = "Offline Tracker"
    page.theme_mode = ft.ThemeMode.DARK

    status = ft.Text("Ready", color="#888")

    def on_click(e):
        try:
            path = make_stats_image()
            status.value = f"Saved to {path} ✅"
        except Exception as ex:
            status.value = f"Error: {ex}"
        page.update()

    page.add(
        ft.Column([
            ft.Text("Offline Tracker", size=30, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Generate stats pic", on_click=on_click, width=300, height=50),
            status
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

# FIXED FOR FLET 1.0.3
ft.run(main)
