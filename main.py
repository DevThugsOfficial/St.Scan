from pathlib import Path
import sys
import subprocess
import flet as ft
import router


# Determine the project root
if getattr(sys, "frozen", False):
    # Running inside PyInstaller bundle
    project_root = Path(sys._MEIPASS)
else:
    # Running normally
    project_root = Path(__file__).resolve().parent


def _start_models_process(project_root: Path) -> None:
    """
    Start database/models.py as a separate Python process so the serial loop
    does not block the GUI. Non-fatal: failures are printed but do not stop the app.
    """
    try:
        models_py = project_root / "database" / "models.py"
        if not models_py.exists():
            return

        # Use the same Python executable
        subprocess.Popen([sys.executable, str(models_py)], cwd=str(project_root))
    except Exception as e:
        print(f"Failed to start models process: {e}")


def main(page: ft.Page):
    # Set global page defaults
    page.title = "RecordSync"
    page.window_width = 900
    page.window_height = 700
    page.padding = 0
    page.bgcolor = "#F2F2F2"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Bind router
    page.on_route_change = router.route_handler(page)

    # Navigate to the current route
    page.go(page.route or "/")


if __name__ == "__main__":
    # Start background models process
    _start_models_process(project_root)

    # Launch Flet app in a native window
    ft.app(
        target=main,
        assets_dir=str(project_root / "assets")
    )
