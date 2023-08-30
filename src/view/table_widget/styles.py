from tkinter import ttk


class TableStyles:
    """The class has styles for tables. To apply a style to a table,
    you need to call a method that will create a style and return its name.
    The name must be passed to the 'style' table parameter."""

    def __init__(self):
        self._style = ttk.Style()

    def main_style(self):
        self._style.theme_use("default")

        self._style.configure("Main.Treeview",
                              borderwidth=0,
                              background="#242424",
                              fieldbackground="#242424",
                              foreground="white",
                              rowheight=45)

        self._style.map("Main.Treeview",
                        background=[("selected", "#1F6AA5")],
                        foreground=[("selected", "white")])

        self._style.configure("Main.Treeview.Heading",
                              background="#4A4A4A",
                              foreground="white",
                              relief="ridge")

        self._style.map("Main.Treeview.Heading",
                        background=[("active", "#696969")])
        return "Main.Treeview"

    def years_style(self):
        self._style.theme_use("default")

        self._style.configure("Years.Treeview",
                              borderwidth=0,
                              background="#2B2B2B",
                              fieldbackground="#2B2B2B",
                              foreground="white",
                              rowheight=45)

        self._style.map("Years.Treeview",
                        background=[("selected", "#1F6AA5")],
                        foreground=[("selected", "white")])

        self._style.configure("Years.Treeview.Heading",
                              background="#4A4A4A",
                              foreground="white",
                              relief="ridge")

        self._style.map("Years.Treeview.Heading",
                        background=[("active", "#696969")])
        return "Years.Treeview"

    def calc_style(self):
        self._style.theme_use("default")

        self._style.configure("Calc.Treeview", font=("CTkDefaultFont", 10))
        self._style.configure("Calc.Treeview.Heading",
                              font=("CTkDefaultFont", 10))

        self._style.configure("Calc.Treeview",
                              borderwidth=0,
                              background="#343638",
                              fieldbackground="#343638",
                              foreground="white",
                              rowheight=28)

        self._style.map("Calc.Treeview",
                        background=[("selected", "#1F6AA5")],
                        foreground=[("selected", "white")])

        self._style.configure("Calc.Treeview.Heading",
                              background="#4A4A4A",
                              foreground="white",
                              relief="ridge")

        self._style.map("Calc.Treeview.Heading",
                        background=[("active", "#4A4A4A")])
        return "Calc.Treeview"
