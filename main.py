import flet as ft
from home import *
from level import *
import time
import random

candyImages = [
    "assets/apple-fruit.png",
    "assets/papaya-fruit.png",
    "assets/orange-fruit.png",
    "assets/kiwi-fruit.png",
    "assets/watermelon-fruit.png",
    "assets/lemon-fruit.png",
]
lv = 0
level_txt = "Level"
objetive_image = ""
objetive_num = 0

def main(page: ft.Page):
    page.title = "Fruit Crush"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.window_height = 700
    page.window_width = 950
    page.window_resizable = False

    def level_start():
        global lv
        text = f"Level {lv}"
        dlg_level_start.title.value = text
        dlg_level_start.content.controls[0].src = objetive_image
        dlg_level_start.content.controls[1].value = str(objetive_num)
        page.dialog = dlg_level_start
        dlg_level_start.open = True
        page.update()
        time.sleep(1)
        dlg_level_start.open = False
        page.update()

    def level_end():
        page.dialog = dlg_level_end
        dlg_level_end.open = True
        page.update()

    def on_exit(e):
        page.window_destroy()

    def on_home(e):
        global lv
        page.clean()
        page.update()
        lv = 0
        page.add(Home(play_level))

    def on_reload(e):
        page.clean()
        page.update()
        level_text = f"Level {lv}"
        new_level = Level(
            level_text,
            objetive_image,
            objetive_num,
            level_end,
            on_home,
            on_reload,
            on_exit,
        )
        page.add(new_level)
        level_start()
        new_level.start()
        page.update()

    def play_level(e):
        global lv
        global level_text
        global objetive_image
        global objetive_num

        if dlg_level_end.open:
            dlg_level_end.open = False
            dlg_level_end.update()
        page.clean()
        page.update()
        lv += 1
        level_text = f"Level {lv}"
        objetive_image = random.choice(candyImages)
        objetive_num = random.randint(10, 25)
        new_level = Level(
            level_text,
            objetive_image,
            objetive_num,
            level_end,
            on_home,
            on_reload,
            on_exit,
        )
        page.add(new_level)
        level_start()
        new_level.start()
        page.update()

    dlg_level_start = ft.AlertDialog(
        title=ft.Text(
            "title_txt",
            size=25,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
        content=ft.Row(
            controls=[
                ft.Image(src="content_image", width=50, height=50),
                ft.Text("content_text", size=30, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    dlg_level_end = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "Level Complete!",
            size=25,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.STAR, color=ft.colors.AMBER, size=30),
                ft.Icon(name=ft.icons.STAR, color=ft.colors.AMBER, size=30),
                ft.Icon(name=ft.icons.STAR, color=ft.colors.AMBER, size=30),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        actions=[
            ft.TextButton("Next Level", on_click=play_level),
            ft.TextButton("Exit", on_click=lambda e: page.window_destroy()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.add(Home(play_level))


ft.app(target=main)
