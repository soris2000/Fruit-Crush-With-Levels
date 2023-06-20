import flet as ft
import time

#Func play game start in level 1
class Home(ft.UserControl):
    def __init__(self, func):
        super().__init__()
        self.on_play= func
        self.running=True
        self.c=ft.Container(
                                on_hover=self.on_hover,
                                on_click=self.on_play,
                                width=80,
                                height=50,
                                bgcolor=ft.colors.PINK_ACCENT,
                                border_radius=15,
                                scale=ft.transform.Scale(scale=1),
                                animate_scale=ft.animation.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
                                content=ft.Text(
                                    "Play",
                                    color=ft.colors.WHITE,
                                    size=25,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                alignment=ft.alignment.center,
                            )
 
    def did_mount(self):
        while self.running:
            if self.c.scale==1:
                self.c.scale=1.1
            else:
                self.c.scale=1
            self.update()
            time.sleep(1)

    def on_hover(self, e):
        e.control.bgcolor = "blue" if e.data == "true" else "pinkaccent"
        e.control.update()

    def build(self):
        self.home = ft.Stack(
            width=950,
            height=700,
            controls=[
                ft.Container(image_src="assets/background.png", image_fit=ft.ImageFit.COVER),
                ft.Container(
                    width=300,
                    height=300,
                    bgcolor=ft.colors.TEAL_300,
                    border_radius=15,
                    content=ft.Column(
                        [
                            ft.Text(
                                "Fruit Crush",
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE70,
                            ),
                            ft.Image(src="assets/avatar.png", width=100, height=100),
                           self.c,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    top=200,
                    left=300,
                ),
            ],
        )
        return self.home

"""
def main(page: ft.Page):
    page.padding = 0
    page.window_height = 700
    page.window_width = 950
    page.window_resizable = False

    def play_game(e):
        print("go Game")
        
    page.add(Home(play_game))

ft.app(target=main)

"""





