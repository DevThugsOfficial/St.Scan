import flet as ft

# Light theme colors for signup UI
BG_LIGHT = "#FAFAFA"
CARD_BG = "#FFFFFF"
TEXT_DARK = "#121212"
MAROON = "#7B0C0C"

# Enhanced visibility colors
LIGHT_BORDER = "#D1D1D1"
INPUT_BORDER = "#E3E3E3"
SHADOW_SOFT = "#00000026"
WHITE = "#FFFFFF"
BLUE = "#1976D2"

def signup_card(page: ft.Page, *, on_create_account, on_login_redirect) -> ft.Container:
    """
    Returns a reusable signup card Container.
    on_create_account(e, username, password, confirm_password)
    """

    username = ft.TextField(
        hint_text="username",
        bgcolor=BG_LIGHT,
        border_radius=12,
        border_color=INPUT_BORDER,
        content_padding=12,
        width=260,
        text_style=ft.TextStyle(
            font_family="Port Lligat Slab",
            color=TEXT_DARK
        ),
        hint_style=ft.TextStyle(
            font_family="Port Lligat Slab",
            color="#99000000"
        ),
    )

    password = ft.TextField(
        hint_text="password",
        password=True,
        can_reveal_password=True,
        bgcolor=BG_LIGHT,
        border_radius=12,
        border_color=INPUT_BORDER,
        content_padding=12,
        width=260,
        text_style=ft.TextStyle(
            font_family="Port Lligat Slab",
            color=TEXT_DARK
        ),
        hint_style=ft.TextStyle(
            font_family="Port Lligat Slab",
            color="#99000000"
        ),
    )

    confirm_password = ft.TextField(
        hint_text="confirm password",
        password=True,
        can_reveal_password=True,
        bgcolor=BG_LIGHT,
        border_radius=12,
        border_color=INPUT_BORDER,
        content_padding=12,
        width=260,
        text_style=ft.TextStyle(
            font_family="Port Lligat Slab",
            color=TEXT_DARK
        ),
        hint_style=ft.TextStyle(
            font_family="Port Lligat Slab",
            color="#99000000"
        ),
    )

    return ft.Container(
        width=360,
        padding=30,
        bgcolor=CARD_BG,
        border_radius=16,
        border=ft.border.all(1, LIGHT_BORDER),
        shadow=ft.BoxShadow(
            blur_radius=28,
            color=SHADOW_SOFT,
            offset=ft.Offset(0, 8),
        ),
        content=ft.Column(
            [
                ft.Image(src="stc.png", width=200, height=200),

                ft.Text(
                    "Sign Up",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_DARK,
                    font_family="Port Lligat Slab",
                ),

                ft.Container(height=10),
                username,

                ft.Container(height=10),
                password,

                ft.Container(height=10),
                confirm_password,

                ft.Container(height=20),

                ft.ElevatedButton(
                    text="Create Account",
                    width=180,
                    height=45,
                    bgcolor=MAROON,
                    color=WHITE,
                    on_click=lambda e: on_create_account(
                        e, username, password, confirm_password
                    ),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=22)
                    ),
                ),

                ft.Container(height=15),

                # FIXED: no ButtonStyle(text_style)
                ft.TextButton(
                    content=ft.Text(
                        "Already have an account?",
                        size=15,
                        font_family="Port Lligat Slab",
                        color=BLUE,
                    ),
                    on_click=on_login_redirect,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
    )
