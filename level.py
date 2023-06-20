import flet as ft
import random
import threading


# Level
class Level(ft.UserControl):
    def __init__(
        self,
        level_txt,
        objetive_image,
        objetive_num,
        level_end,
        on_home,
        on_reload,
        on_exit,
    ):
        super().__init__()
        self.objetive_image = objetive_image
        self.objetive_num = objetive_num
        self.level_txt = level_txt
        self.level_end = level_end
        self.on_home = on_home
        self.on_reload = on_reload
        self.on_exit = on_exit
        self.numitems = 8
        self.imageSource = ""
        self.imageDestination = ""
        self.idSource = 0
        self.idDestination = 0
        self.candyImages = [
            "assets/apple-fruit.png",
            "assets/papaya-fruit.png",
            "assets/orange-fruit.png",
            "assets/kiwi-fruit.png",
            "assets/watermelon-fruit.png",
            "assets/lemon-fruit.png",
        ]
        self.level_display = ft.Text(self.level_txt, size=25, weight=ft.FontWeight.BOLD)
        self.avatar = ft.Image(
            src="assets/avatar.png", width=100, height=100, fit=ft.ImageFit.COVER
        )
        self.objetive_image_display = ft.Image(
            src=self.objetive_image, width=50, height=50
        )
        self.objetive_num_display = ft.Text(
            self.objetive_num, size=30, weight=ft.FontWeight.BOLD
        )
        self.squares = self.get_squares()

    def start(self):
        self.running = True
        self.th = threading.Thread(
            target=self.setInterval, args=(self.check_infinite, 0.10), daemon=True
        )
        self.th.start()

    def checkRowForThree(self):
        for i in range(62):
            rowOfThree = [i, i + 1, i + 2]
            decidedImage = self.squares.controls[i].image_src
            isBlank = True if self.squares.controls[i].image_src == "" else False
            notValid = [6, 7, 14, 15, 22, 23, 30, 31, 38, 39, 46, 47, 54, 55]
            if i in notValid:
                continue
            if all(
                [
                    (
                        self.squares.controls[index].image_src == decidedImage
                        and not isBlank
                    )
                    for index in rowOfThree
                ]
            ):
                for i in rowOfThree:
                    self.squares.controls[i].image_src = ""
                self.check_objetive(decidedImage)

        self.update()

    def checkColumnForThree(self):
        for i in range(48):
            columnForThree = [i, i + self.numitems, i + self.numitems * 2]
            decidedImage = self.squares.controls[i].image_src
            isBlank = True if self.squares.controls[i].image_src == "" else False
            if all(
                [
                    (
                        self.squares.controls[index].image_src == decidedImage
                        and not isBlank
                    )
                    for index in columnForThree
                ]
            ):
                for i in columnForThree:
                    self.squares.controls[i].image_src = ""
                self.check_objetive(decidedImage)

        self.update()

    def moveIntoSquareBelow(self):
        # drop candies once some have been cleared
        for i in range(56):
            if self.squares.controls[i + self.numitems].image_src == "":
                self.squares.controls[
                    i + self.numitems
                ].image_src = self.squares.controls[i].image_src
                self.squares.controls[i].image_src = ""
                firstRow = [0, 1, 2, 3, 4, 5, 6, 7]
                isFirstRow = True if i in firstRow else False
                if isFirstRow and self.squares.controls[i].image_src == "":
                    randomImage = random.choice(self.candyImages)
                    self.squares.controls[i].image_src = randomImage
        self.update()

    def check_infinite(self):
        while self.running:
            self.checkRowForThree()
            self.checkColumnForThree()
            self.moveIntoSquareBelow()

    def check_objetive(self, decidedImage):
        if decidedImage == self.objetive_image:
            self.objetive_num -= 3
            if self.objetive_num <= 0:
                self.objetive_num_display.value = "0"
                self.running = False
                self.level_end()
                return
            else:
                self.objetive_num_display.value = str(self.objetive_num)
        self.update()

    def setInterval(self, func, time):
        e = threading.Event()
        while not e.wait(time):
            func()

    def exchange(self):
        # Is a valid move?
        validMoves = [
            self.idSource - 1,
            self.idSource - self.numitems,
            self.idSource + 1,
            self.idSource + self.numitems,
        ]
        if self.idDestination in validMoves:  # To move
            self.squares.controls[self.idDestination].image_src = self.imageSource
            self.squares.controls[self.idSource].image_src = self.imageDestination
            self.squares.controls[self.idDestination].update()
            self.squares.controls[self.idSource].update()

        self.squares.controls[self.idSource].bgcolor = ""
        self.squares.controls[self.idDestination].bgcolor = ""
        self.imageSource = ""
        self.imageDestination = ""
        self.idSource = 0
        self.idDestination = 0
        self.update()

    def clickCandy(self, e):
        e.control.bgcolor = "black54"
        e.control.update()
        if self.imageSource == "":
            self.imageSource = e.control.image_src
            self.idSource = e.control.key
        else:
            self.imageDestination = e.control.image_src
            self.idDestination = e.control.key
            self.exchange()

    def get_squares(self):
        self.grid = ft.GridView(
            expand=None,
            runs_count=8,
            max_extent=70,
            child_aspect_ratio=1.0,
            spacing=0,
            run_spacing=0,
            width=560,
            height=560,
        )
        for i in range(self.numitems * self.numitems):
            randomImage = random.choice(self.candyImages)
            square = ft.Container(
                key=i,
                image_src=randomImage,
                width=50,
                height=50,
                border_radius=5,
                on_click=self.clickCandy,
            )
            self.grid.controls.append(square)
        return self.grid

    def build(self):
        self.level = ft.Container(
            width=950,
            height=700,
            padding=20,
            image_src="assets/background.png",
            image_fit=ft.ImageFit.COVER,
            alignment=ft.alignment.center,
            content=ft.Row(
                width=900,
                height=700,
                controls=[
                    ft.Container(
                        border=ft.border.all(3, "white54"),
                        border_radius=10,
                        width=220,
                        height=500,
                        bgcolor=ft.colors.TEAL,
                        padding=20,
                        content=ft.Column(
                            [
                                self.level_display,
                                self.avatar,
                                ft.Container(
                                    height=80,
                                    bgcolor=ft.colors.PINK,
                                    border_radius=10,
                                    margin=20,
                                    content=ft.Row(
                                        [
                                            self.objetive_image_display,
                                            self.objetive_num_display,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                ),
                                ft.Column(
                                    [
                                        ft.Container(
                                            width=50,
                                            height=50,
                                            image_src="assets/reload.png",
                                            image_fit=ft.ImageFit.CONTAIN,
                                            alignment=ft.alignment.center,
                                            on_click=self.on_reload,
                                        ),
                                        ft.Container(
                                            width=50,
                                            height=50,
                                            image_src="assets/home.png",
                                            image_fit=ft.ImageFit.CONTAIN,
                                            alignment=ft.alignment.center,
                                            on_click=self.on_home,
                                        ),
                                        ft.Container(
                                            width=50,
                                            height=50,
                                            image_src="assets/exit.png",
                                            image_fit=ft.ImageFit.CONTAIN,
                                            alignment=ft.alignment.center,
                                            on_click=self.on_exit,
                                        ),
                                    ]
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(width=60),
                    ft.Container(
                        width=580,
                        height=580,
                        border_radius=10,
                        bgcolor=ft.colors.LIGHT_BLUE_300,
                        content=self.squares,
                        alignment=ft.alignment.center,
                    ),
                ],
            ),
        )
        return self.level
