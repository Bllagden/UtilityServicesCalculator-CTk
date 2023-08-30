def center_window(window, win_width, win_height):
    """Places the window in the center of the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (win_width // 2)
    y = (screen_height // 2) - (win_height // 2)
    window.geometry(f"{win_width}x{win_height}+{x}+{y}")
