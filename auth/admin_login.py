from pathlib import Path
import flet as ft

def main(page: ft.Page):
    # -------------------- PAGE SETTINGS --------------------
    page.title = "Login Page"
    page.window_width = 600
    page.window_height = 600
    page.padding = 0
    page.bgcolor = "#F2F2F2"

    # -------------------- COLORS --------------------
    MAROON = "#7B0C0C"
    BLACK = "#D5C9C9"
    WHITE = "#FFFFFF"
    BLUE = "#000DFC"
    BLACK1 = "#000000"

    # -------------------- INPUTS --------------------
    username = ft.TextField(
        hint_text="username",
        bgcolor=BLACK,
        border_radius=10,
        border_color="transparent",
        content_padding=12,
        width=260,
        text_style=ft.TextStyle(font_family="Port Lligat Slab", color=WHITE),
        hint_style=ft.TextStyle(font_family="Port Lligat Slab",  color="#99000000")  # <-- set hint text color
    )

    password = ft.TextField(
        hint_text="password",
        password=True,
        can_reveal_password=True,
        bgcolor=BLACK,
        border_radius=10,
        border_color="transparent",
        content_padding=12,
        width=260,
        color=BLACK1,  # text color when typing
        text_style=ft.TextStyle(font_family="Port Lligat Slab", color=BLACK1),
        hint_style=ft.TextStyle(
            font_family="Port Lligat Slab",
            color="#99000000"  # black with 60% opacity
        )
)



    # -------------------- CLICK HANDLERS --------------------
    def forgot_password_clicked(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Forgot Password", font_family="Port Lligat Slab"),
            content=ft.Text("Redirect to forgot password page here.", font_family="Port Lligat Slab"),
            actions=[ft.TextButton("Close", on_click=lambda e: page.dialog.close())],
        )
        page.dialog.open = True
        page.update()

    def signup_clicked(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Sign Up", font_family="Port Lligat Slab"),
            content=ft.Text("Redirect to sign up page here.", font_family="Port Lligat Slab"),
            actions=[ft.TextButton("Close", on_click=lambda e: page.dialog.close())],
        )
        page.dialog.open = True
        page.update()

    # -------------------- LOGIN CARD --------------------
    login_card = ft.Container(
        width=360,
        padding=30,
        height=530,
        bgcolor=WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color="#00000020",
            offset=ft.Offset(0, 6),
        ),
        content=ft.Column(
            [
                ft.Image(
                    src="stc.png",
                    width=100,
                    height=100,
                ),

                ft.Text(
                    "Sign in",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=BLACK1,
                    font_family="Port Lligat Slab"
                ),

                ft.Container(height=10),

                username,
                ft.Container(height=10),
                password,

                ft.Container(
                    ft.TextButton(
                        "forgot password?",
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(size=15, font_family="Port Lligat Slab", color=BLUE),
                        ),
                        on_click=forgot_password_clicked,
                    ),
                    alignment=ft.alignment.center_right,
                    width=260,
                ),

                ft.Container(height=15),

                ft.ElevatedButton(
                    text="Log in",
                    width=160,
                    height=42,
                    bgcolor=MAROON,
                    color=WHITE,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(font_family="Port Lligat Slab"),
                        shape=ft.RoundedRectangleBorder(radius=20)
                    ),
                ),

                ft.Container(height=15),

                ft.TextButton(
                    "Don't have an account?",
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=15, font_family="Port Lligat Slab", color=BLUE)
                    ),
                    on_click=signup_clicked,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # -------------------- PAGE LAYOUT --------------------
    page.add(
        ft.Column(
            [
                ft.Container(height=40, bgcolor=MAROON),  # TOP BAR

                ft.Container(
                    content=login_card,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    ft.app(
        target=main,
        view=ft.WEB_BROWSER,
        assets_dir=str(project_root / "assets")  # point to assets folder
    )